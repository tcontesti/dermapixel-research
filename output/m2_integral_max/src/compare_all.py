#!/usr/bin/env python3
"""Unified paired comparison of all 5 models on bucket A (n=1000).
Handles 3 architecture families (SAM2, transformers SamModel, SAM-Med2D adapter),
computes per-image Dice on the SAME images, then pairwise Wilcoxon signed-rank.
"""
import sys, os, json, itertools
import numpy as np, torch, torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import pandas as pd
from scipy.stats import wilcoxon
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_metrics as M

DEVICE = 'cuda'
OUT = os.path.expanduser('~/panderm/output/m2_integral_max/outputs')
MAN = os.path.expanduser('~/panderm/output/m2_integral_max/manifests/m2_integral_max_v1c_local.parquet')
MEDSAM2 = __import__('huggingface_hub').hf_hub_download('wanglab/MedSAM2', 'MedSAM2_latest.pt')
SAMMED_REPO = os.path.expanduser('~/panderm/datasets/SAM-Med2D_repo')
SAMMED_CKPT = os.path.expanduser('~/panderm/datasets/SAM-Med2D_repo/sam-med2d_b.pth')
IMNET_MEAN = np.array([0.485, 0.456, 0.406], np.float32); IMNET_STD = np.array([0.229, 0.224, 0.225], np.float32)
SAM_MEAN = np.array([123.675, 116.28, 103.53], np.float32); SAM_STD = np.array([58.395, 57.12, 57.375], np.float32)


def load_items(df, isz):
    """Return list of (img_tensor[isz], gt_mask_1024, bbox_in_isz) for a family."""
    items = []
    for _, r in df.iterrows():
        items.append((r.image_path, r.mask_path, isz))
    return items


class DS(Dataset):
    def __init__(self, df, isz, norm, gt_size=1024):
        self.df = df.reset_index(drop=True); self.isz = isz; self.norm = norm; self.gsz = gt_size
    def __len__(self): return len(self.df)
    def __getitem__(self, i):
        r = self.df.iloc[i]
        pim = Image.open(r.image_path).convert('RGB'); pmk = Image.open(r.mask_path).convert('L')
        img = np.array(pim.resize((self.isz, self.isz), Image.BILINEAR), np.float32)
        m_in = (np.array(pmk.resize((self.isz, self.isz), Image.NEAREST), np.float32) > 127.5).astype(np.float32)
        gt = (np.array(pmk.resize((self.gsz, self.gsz), Image.NEAREST), np.float32) > 127.5).astype(np.float32)
        if self.norm == 'imnet': img = (img / 255. - IMNET_MEAN) / IMNET_STD
        else: img = (img - SAM_MEAN) / SAM_STD
        ys, xs = np.where(m_in > 0.5)
        bb = np.array([0, 0, self.isz, self.isz], np.float32) if len(ys) == 0 else np.array([xs.min(), ys.min(), xs.max(), ys.max()], np.float32)
        return torch.from_numpy(img).permute(2, 0, 1).float(), torch.from_numpy(gt)[None].float(), bb


# ---- SAM2 (F2/F3/F3b) ----
def sam2_perimg(model_id, init_ckpt, best_pt, df):
    from sam2.build_sam import build_sam2_hf
    m = build_sam2_hf(model_id).to(DEVICE)
    if init_ckpt:
        ck = torch.load(init_ckpt, map_location=DEVICE, weights_only=False)
        m.load_state_dict(ck['model'] if isinstance(ck, dict) and 'model' in ck else ck, strict=False)
    m.load_state_dict(torch.load(best_pt, map_location=DEVICE, weights_only=False)['state'], strict=False)
    m.eval()
    dl = DataLoader(DS(df, 1024, 'imnet'), batch_size=4, num_workers=4)
    out = []
    with torch.no_grad():
        for imgs, gts, bb in dl:
            imgs = imgs.to(DEVICE)
            bbn = bb.to(DEVICE)
            backbone = m.forward_image(imgs); _, vf, _, fs = m._prepare_backbone_features(backbone)
            if m.directly_add_no_mem_embed: vf[-1] = vf[-1] + m.no_mem_embed
            feats = [f.permute(1, 2, 0).view(imgs.size(0), -1, *s) for f, s in zip(vf[::-1], fs[::-1])][::-1]
            for i in range(imgs.size(0)):
                fi = [f[i:i+1] for f in feats]
                se, de = m.sam_prompt_encoder(points=None, boxes=bbn[i:i+1], masks=None)
                low, _, _, _ = m.sam_mask_decoder(image_embeddings=fi[-1], image_pe=m.sam_prompt_encoder.get_dense_pe(),
                                                  sparse_prompt_embeddings=se, dense_prompt_embeddings=de,
                                                  multimask_output=False, repeat_image=False, high_res_features=fi[:-1])
                pr = F.interpolate(low, (1024, 1024), mode='bilinear', align_corners=False)
                out.append(M.dice_iou((torch.sigmoid(pr[0, 0]) > 0.5).cpu().numpy(), gts[i, 0].numpy())[0])
    del m; torch.cuda.empty_cache(); return np.array(out)


# ---- transformers SamModel (F5 MedSAM v1) ----
def samv1_perimg(model_id, best_pt, df):
    from transformers import SamModel
    m = SamModel.from_pretrained(model_id).to(DEVICE)
    m.load_state_dict(torch.load(best_pt, map_location=DEVICE, weights_only=False)['state'], strict=False)
    m.eval()
    dl = DataLoader(DS(df, 1024, 'sam'), batch_size=4, num_workers=4)
    out = []
    with torch.no_grad():
        for imgs, gts, bb in dl:
            imgs = imgs.to(DEVICE)
            o = m(pixel_values=imgs, input_boxes=bb.to(DEVICE).unsqueeze(1), multimask_output=False)
            pr = F.interpolate(o.pred_masks[:, 0], (1024, 1024), mode='bilinear', align_corners=False)
            for i in range(imgs.size(0)):
                out.append(M.dice_iou((torch.sigmoid(pr[i, 0]) > 0.5).cpu().numpy(), gts[i, 0].numpy())[0])
    del m; torch.cuda.empty_cache(); return np.array(out)


# ---- SAM-Med2D (F4) ----
def sammed2d_perimg(best_pt, df):
    sys.path.insert(0, SAMMED_REPO)
    from segment_anything import sam_model_registry
    from argparse import Namespace
    m = sam_model_registry['vit_b'](Namespace(image_size=256, sam_checkpoint=None, encoder_adapter=True)).to(DEVICE)
    m.load_state_dict(torch.load(SAMMED_CKPT, map_location=DEVICE, weights_only=False)['model'], strict=False)
    m.load_state_dict(torch.load(best_pt, map_location=DEVICE, weights_only=False)['state'], strict=False)
    m.eval()
    dl = DataLoader(DS(df, 256, 'sam'), batch_size=4, num_workers=4)
    out = []
    with torch.no_grad():
        for imgs, gts, bb in dl:
            imgs = imgs.to(DEVICE)
            emb = m.image_encoder(imgs)
            se, de = m.prompt_encoder(points=None, boxes=bb.to(DEVICE).unsqueeze(1), masks=None)
            lr, _ = m.mask_decoder(image_embeddings=emb, image_pe=m.prompt_encoder.get_dense_pe(),
                                   sparse_prompt_embeddings=se, dense_prompt_embeddings=de, multimask_output=False)
            pr = F.interpolate(lr, (1024, 1024), mode='bilinear', align_corners=False)
            for i in range(imgs.size(0)):
                out.append(M.dice_iou((torch.sigmoid(pr[i, 0]) > 0.5).cpu().numpy(), gts[i, 0].numpy())[0])
    del m; torch.cuda.empty_cache(); return np.array(out)


df = pd.read_parquet(MAN)
A = df[df.split == 'test_canonical'].sort_values('image_path').reset_index(drop=True)
print('bucket A n =', len(A), flush=True)

D = {}
D['F2_SAM2.1L_gen']   = sam2_perimg('facebook/sam2.1-hiera-large', '', f'{OUT}/M2_v1_sam21_fullft/best.pt', A); print('F2 done', flush=True)
D['F3_MedSAM2T_med']  = sam2_perimg('facebook/sam2.1-hiera-tiny', MEDSAM2, f'{OUT}/M2_v2_medsam2/best.pt', A); print('F3 done', flush=True)
D['F3b_SAM2.1T_gen']  = sam2_perimg('facebook/sam2.1-hiera-tiny', '', f'{OUT}/M2_v2b_sam21tiny/best.pt', A); print('F3b done', flush=True)
D['F5_MedSAMv1_med']  = samv1_perimg('wanglab/medsam-vit-base', f'{OUT}/M2_v4_medsamv1/best.pt', A); print('F5 done', flush=True)
D['F4_SAMMed2D_med']  = sammed2d_perimg(f'{OUT}/M2_v3_sammed2d/best.pt', A); print('F4 done', flush=True)

means = {k: float(v.mean()) for k, v in D.items()}
for k in sorted(means, key=lambda x: -means[x]):
    print(f'{k:22s} Dice {means[k]:.4f}', flush=True)
pairs = {}
for x, y in itertools.combinations(D.keys(), 2):
    st, p = wilcoxon(D[x], D[y])
    pairs[f'{x}__vs__{y}'] = {'mean_x': means[x], 'mean_y': means[y], 'delta_pp': float(100*(means[y]-means[x])), 'wilcoxon_p': float(p)}
json.dump({'n': len(A), 'means': means, 'pairwise': pairs}, open(f'{OUT}/comparison_all5_bucketA.json', 'w'), indent=2)
print('=== key pairs ===', flush=True)
for key in ['F2_SAM2.1L_gen__vs__F3_MedSAM2T_med', 'F3_MedSAM2T_med__vs__F5_MedSAMv1_med',
            'F3_MedSAM2T_med__vs__F4_SAMMed2D_med', 'F5_MedSAMv1_med__vs__F4_SAMMed2D_med',
            'F3b_SAM2.1T_gen__vs__F5_MedSAMv1_med']:
    if key in pairs:
        print(f'{key}: delta={pairs[key]["delta_pp"]:+.2f}pp p={pairs[key]["wilcoxon_p"]:.3g}', flush=True)
print('saved comparison_all5_bucketA.json', flush=True)
