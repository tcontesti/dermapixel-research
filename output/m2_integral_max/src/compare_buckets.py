#!/usr/bin/env python3
"""Paired head-to-head on bucket A (canonical ISIC2018 test, n=1000).
Re-evaluates every available model per-image on the SAME images, then runs
Wilcoxon signed-rank for each pair. Auto-skips models whose best.pt is absent
(so it works for F2-vs-F3 and later the F2/F3/F3b triple).
"""
import sys, os, json, argparse, itertools
import numpy as np, torch, torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import pandas as pd
from scipy.stats import wilcoxon
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_metrics as M

DEVICE = 'cuda'; IMG = 1024
MEAN = np.array([0.485, 0.456, 0.406], np.float32); STD = np.array([0.229, 0.224, 0.225], np.float32)
OUT = os.path.expanduser('~/panderm/output/m2_integral_max/outputs')


class DS(Dataset):
    def __init__(self, df): self.df = df.reset_index(drop=True)
    def __len__(self): return len(self.df)
    def __getitem__(self, i):
        r = self.df.iloc[i]
        img = np.array(Image.open(r.image_path).convert('RGB').resize((IMG, IMG), Image.BILINEAR), np.float32) / 255.
        mask = (np.array(Image.open(r.mask_path).convert('L').resize((IMG, IMG), Image.NEAREST), np.float32) > 127.5).astype(np.float32)
        img = (img - MEAN) / STD
        ys, xs = np.where(mask > 0.5)
        bb = np.array([0, 0, IMG, IMG], np.float32) if len(ys) == 0 else np.array([xs.min(), ys.min(), xs.max(), ys.max()], np.float32)
        return torch.from_numpy(img).permute(2, 0, 1).float(), torch.from_numpy(mask)[None].float(), bb


def fwd(model, images, bboxes):
    bs = images.size(0); bb = model.forward_image(images)
    _, vf, _, fs = model._prepare_backbone_features(bb)
    if model.directly_add_no_mem_embed: vf[-1] = vf[-1] + model.no_mem_embed
    feats = [f.permute(1, 2, 0).view(bs, -1, *s) for f, s in zip(vf[::-1], fs[::-1])][::-1]
    out = []
    for i in range(bs):
        fi = [f[i:i + 1] for f in feats]
        box = torch.as_tensor(bboxes[i:i + 1], dtype=torch.float32, device=images.device)
        se, de = model.sam_prompt_encoder(points=None, boxes=box, masks=None)
        low, _, _, _ = model.sam_mask_decoder(image_embeddings=fi[-1], image_pe=model.sam_prompt_encoder.get_dense_pe(),
                                              sparse_prompt_embeddings=se, dense_prompt_embeddings=de,
                                              multimask_output=False, repeat_image=False, high_res_features=fi[:-1])
        out.append(F.interpolate(low, (IMG, IMG), mode='bilinear', align_corners=False)[:, 0:1])
    return torch.cat(out, 0)


def build(model_id, init_ckpt, best_pt):
    from sam2.build_sam import build_sam2_hf
    m = build_sam2_hf(model_id).to(DEVICE)
    if init_ckpt:
        ck = torch.load(init_ckpt, map_location=DEVICE, weights_only=False)
        sd = ck['model'] if (isinstance(ck, dict) and 'model' in ck) else ck
        m.load_state_dict(sd, strict=False)
    bp = torch.load(best_pt, map_location=DEVICE, weights_only=False)
    m.load_state_dict(bp['state'], strict=False)
    m.eval(); return m


@torch.no_grad()
def perimg_dice(model, df):
    dl = DataLoader(DS(df), batch_size=4, num_workers=4)
    out = []
    for imgs, masks, bb in dl:
        imgs = imgs.to(DEVICE); bb = bb.to(DEVICE)
        with torch.amp.autocast('cuda', dtype=torch.bfloat16):
            lg = fwd(model, imgs, bb)
        pred = (torch.sigmoid(lg) > 0.5).float().cpu().numpy(); gt = masks.numpy()
        for j in range(pred.shape[0]):
            out.append(M.dice_iou(pred[j, 0], gt[j, 0])[0])
    return np.array(out)


def latency_of(resdir):
    try:
        return json.load(open(f'{OUT}/{resdir}/results.json'))['latency_ms_1024']
    except Exception:
        return None


ap = argparse.ArgumentParser()
ap.add_argument('--manifest', default=os.path.expanduser('~/panderm/output/m2_integral_max/manifests/m2_integral_max_v1c_local.parquet'))
ap.add_argument('--medsam2', required=True)
a = ap.parse_args()

# label, model_id, init_ckpt, output_subdir
SPECS = [
    ('F2_SAM2.1-L_SA1B',  'facebook/sam2.1-hiera-large', '',         'M2_v1_sam21_fullft'),
    ('F3_MedSAM2-T_med',  'facebook/sam2.1-hiera-tiny',  a.medsam2,  'M2_v2_medsam2'),
    ('F3b_SAM2.1-T_SA1B', 'facebook/sam2.1-hiera-tiny',  '',         'M2_v2b_sam21tiny'),
]
df = pd.read_parquet(a.manifest)
A = df[df.split == 'test_canonical'].sort_values('image_path').reset_index(drop=True)
print('bucket A n =', len(A), flush=True)

dices, summary = {}, {}
for label, mid, init, sub in SPECS:
    bp = f'{OUT}/{sub}/best.pt'
    if not os.path.isfile(bp):
        print(f'skip {label}: no {bp}', flush=True); continue
    m = build(mid, init, bp)
    d = perimg_dice(m, A); dices[label] = d
    summary[label] = {'dice_mean': float(d.mean()), 'dice_std': float(d.std()),
                      'latency_ms': latency_of(sub)}
    print(f'{label:20s} Dice {d.mean():.4f} +/- {d.std():.4f}  latency {summary[label]["latency_ms"]}', flush=True)
    del m; torch.cuda.empty_cache()

pairs = {}
for x, y in itertools.combinations(dices.keys(), 2):
    stat, p = wilcoxon(dices[x], dices[y])
    delta = 100 * (dices[y].mean() - dices[x].mean())
    pairs[f'{x}_vs_{y}'] = {'delta_pp_y_minus_x': float(delta), 'wilcoxon_stat': float(stat), 'wilcoxon_p': float(p)}
    print(f'{x} vs {y}: delta={delta:+.2f}pp  Wilcoxon p={p:.4g}', flush=True)

json.dump({'n': len(A), 'baseline_M2_v0': 0.9473, 'models': summary, 'pairwise': pairs},
          open(f'{OUT}/comparison_bucketA.json', 'w'), indent=2)
print('saved', f'{OUT}/comparison_bucketA.json', flush=True)
