#!/usr/bin/env python3
"""F8 analyses bundle (MedSAM2-tiny, box-prompted GT) on bucket A / bucket B.

Components:
  A) TTA           : 4-view (id/hflip/vflip/both) prob-averaging on bucket A.
  B) ENSEMBLE      : mean of the 5 F7 full_ft fold models on bucket A.
  C) FAIRNESS ITA  : pseudo-Fitzpatrick via Individual Typology Angle on the
                     peri-lesional (non-lesion) skin; Dice per ITA group + gap.
  D) CROSS-DATASET : per-dataset_origin Dice on bucket B (HAM/ISIC17/ISIC18/PH2).
  E) CALIBRATION   : pixel-probability ECE (15 bins) + Brier on bucket A.
All eval-only. Base model = F3 M2_v2_medsam2/best.pt (the M2 winner).
"""
import os, sys, json, argparse
import numpy as np, torch, torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import pandas as pd
from skimage.color import rgb2lab
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_metrics as M

P = argparse.ArgumentParser()
P.add_argument('--manifest', default=os.path.expanduser('~/panderm/output/m2_integral_max/manifests/m2_integral_max_v1c_local.parquet'))
P.add_argument('--best_pt', default=os.path.expanduser('~/panderm/output/m2_integral_max/outputs/M2_v2_medsam2/best.pt'))
P.add_argument('--fold_dir', default=os.path.expanduser('~/panderm/output/m2_integral_max/outputs/M2_v6_f7_cv'))
P.add_argument('--model_id', default='facebook/sam2.1-hiera-tiny')
P.add_argument('--init_ckpt', default='/home/husll-spark-01/.cache/huggingface/hub/models--wanglab--MedSAM2/snapshots/e4a6f35edd7e091619cbc0750f462f1574e23955/MedSAM2_latest.pt')
P.add_argument('--out', default=os.path.expanduser('~/panderm/output/m2_integral_max/outputs/M2_v8_f8_analyses'))
P.add_argument('--img_size', type=int, default=1024)
P.add_argument('--smoke', action='store_true')
args = P.parse_args()
DEVICE = torch.device('cuda')
IMNET_MEAN = np.array([0.485, 0.456, 0.406], np.float32); IMNET_STD = np.array([0.229, 0.224, 0.225], np.float32)


class DS(Dataset):
    def __init__(self, df, isz):
        self.df = df.reset_index(drop=True); self.isz = isz
    def __len__(self): return len(self.df)
    def __getitem__(self, i):
        r = self.df.iloc[i]
        raw = np.array(Image.open(r.image_path).convert('RGB').resize((self.isz, self.isz), Image.BILINEAR), np.float32)
        gt = (np.array(Image.open(r.mask_path).convert('L').resize((self.isz, self.isz), Image.NEAREST), np.float32) > 127.5).astype(np.float32)
        ys, xs = np.where(gt > 0.5)
        box = np.array([0, 0, self.isz, self.isz], np.float32) if len(ys) == 0 else np.array([xs.min(), ys.min(), xs.max(), ys.max()], np.float32)
        img = (raw / 255. - IMNET_MEAN) / IMNET_STD
        return (torch.from_numpy(img).permute(2, 0, 1).float(), torch.from_numpy(gt)[None].float(),
                box, torch.from_numpy(raw).float(), r.dataset_origin)


def forward_sam2_batch(model, images, bboxes, img_size):
    bs = images.size(0)
    bb = model.forward_image(images)
    _, vision_feats, _, feat_sizes = model._prepare_backbone_features(bb)
    if model.directly_add_no_mem_embed:
        vision_feats[-1] = vision_feats[-1] + model.no_mem_embed
    feats = [f.permute(1, 2, 0).view(bs, -1, *fs) for f, fs in zip(vision_feats[::-1], feat_sizes[::-1])][::-1]
    out = []
    for i in range(bs):
        fi = [f[i:i + 1] for f in feats]
        box = torch.as_tensor(bboxes[i:i + 1], dtype=torch.float32, device=images.device)
        se, de = model.sam_prompt_encoder(points=None, boxes=box, masks=None)
        low, _, _, _ = model.sam_mask_decoder(image_embeddings=fi[-1], image_pe=model.sam_prompt_encoder.get_dense_pe(),
                                              sparse_prompt_embeddings=se, dense_prompt_embeddings=de,
                                              multimask_output=False, repeat_image=False, high_res_features=fi[:-1])
        out.append(F.interpolate(low, (img_size, img_size), mode='bilinear', align_corners=False)[:, 0:1])
    return torch.cat(out, 0)


def build(best_pt):
    from sam2.build_sam import build_sam2_hf
    m = build_sam2_hf(args.model_id).to(DEVICE)
    ck = torch.load(args.init_ckpt, map_location=DEVICE, weights_only=False)
    m.load_state_dict(ck['model'] if (isinstance(ck, dict) and 'model' in ck) else ck, strict=False)
    best = torch.load(best_pt, map_location=DEVICE, weights_only=False)
    m.load_state_dict(best['state'], strict=False); m.eval()
    return m


def ita_of(raw_img, gt_mask):
    """ITA (deg) from peri-lesional skin: non-lesion, non-vignette pixels."""
    skin = (gt_mask < 0.5)
    bright = raw_img.sum(-1) > 60            # drop near-black dermoscope vignette
    sel = skin & bright
    if sel.sum() < 200: sel = bright
    if sel.sum() < 50: return np.nan
    lab = rgb2lab((raw_img / 255.0)[None])[0]   # HxWx3
    Lp = lab[..., 0][sel]; bp = lab[..., 2][sel]
    Lm, bm = np.median(Lp), np.median(bp)
    return float(np.degrees(np.arctan2(Lm - 50.0, bm + 1e-6)))


def ita_group(ita):
    if np.isnan(ita): return 'unknown'
    if ita > 55: return 'I_verylight'
    if ita > 41: return 'II_light'
    if ita > 28: return 'III_intermediate'
    if ita > 10: return 'IV_tan'
    return 'V-VI_brown_dark'


@torch.no_grad()
def base_pass(model, df):
    """Single-model pass: per-image Dice, ITA, dataset; + ECE/Brier accumulation."""
    dl = DataLoader(DS(df, args.img_size), batch_size=4, shuffle=False, num_workers=4, pin_memory=True)
    NB = 15; conf_sum = np.zeros(NB); acc_sum = np.zeros(NB); cnt = np.zeros(NB)
    brier_sum = 0.0; brier_n = 0
    rows = []
    for imgs, gts, boxes, raws, dsos in dl:
        imgs = imgs.to(DEVICE)
        with torch.amp.autocast('cuda', dtype=torch.bfloat16):
            lg = forward_sam2_batch(model, imgs, boxes.to(DEVICE), args.img_size)
        prob = torch.sigmoid(lg.float()).cpu().numpy()  # B,1,H,W
        gt = gts.numpy()
        for j in range(prob.shape[0]):
            p = prob[j, 0]; g = gt[j, 0]
            rows.append({'dice': M.all_metrics((p > 0.5).astype(np.float32), g)['dice'],
                         'ita': ita_of(raws[j].numpy(), g), 'dataset': dsos[j]})
            # ECE/Brier on a 4x-subsampled grid (memory)
            ps = p[::4, ::4].ravel(); gs = g[::4, ::4].ravel()
            brier_sum += float(np.mean((ps - gs) ** 2)); brier_n += 1
            bins = np.clip((ps * NB).astype(int), 0, NB - 1)
            for b in range(NB):
                m_ = bins == b
                if m_.any():
                    conf_sum[b] += ps[m_].sum(); acc_sum[b] += gs[m_].sum(); cnt[b] += m_.sum()
    ece = float(np.sum(cnt / cnt.sum() * np.abs(acc_sum / np.maximum(cnt, 1) - conf_sum / np.maximum(cnt, 1))))
    return rows, {'ece_15bin': ece, 'brier': brier_sum / max(1, brier_n)}


@torch.no_grad()
def tta_pass(model, df):
    dl = DataLoader(DS(df, args.img_size), batch_size=4, shuffle=False, num_workers=4, pin_memory=True)
    S = args.img_size; per = []
    for imgs, gts, boxes, raws, _ in dl:
        imgs = imgs.to(DEVICE); boxes = boxes.numpy(); B = imgs.size(0)
        acc = np.zeros((B, S, S), np.float32)
        for view in ['id', 'h', 'v', 'hv']:
            im = imgs.clone(); bx = boxes.copy()
            if view in ('h', 'hv'):
                im = torch.flip(im, dims=[3]); bx = bx.copy(); bx[:, 0], bx[:, 2] = S - 1 - boxes[:, 2], S - 1 - boxes[:, 0]
            if view in ('v', 'hv'):
                im = torch.flip(im, dims=[2]); b2 = bx.copy(); bx[:, 1], bx[:, 3] = S - 1 - b2[:, 3], S - 1 - b2[:, 1]
            with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                lg = forward_sam2_batch(model, im, torch.from_numpy(bx).float().to(DEVICE), S)
            pr = torch.sigmoid(lg.float())
            if view in ('h', 'hv'): pr = torch.flip(pr, dims=[3])
            if view in ('v', 'hv'): pr = torch.flip(pr, dims=[2])
            acc += pr[:, 0].cpu().numpy()
        acc /= 4.0; gt = gts.numpy()
        for j in range(B): per.append(M.all_metrics((acc[j] > 0.5).astype(np.float32), gt[j, 0]))
    return M.aggregate(per)


@torch.no_grad()
def ensemble_pass(models, df):
    dl = DataLoader(DS(df, args.img_size), batch_size=4, shuffle=False, num_workers=4, pin_memory=True)
    per = []
    for imgs, gts, boxes, raws, _ in dl:
        imgs = imgs.to(DEVICE); bx = boxes.to(DEVICE); B = imgs.size(0)
        acc = np.zeros((B, args.img_size, args.img_size), np.float32)
        for m in models:
            with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                lg = forward_sam2_batch(m, imgs, bx, args.img_size)
            acc += torch.sigmoid(lg.float())[:, 0].cpu().numpy()
        acc /= len(models); gt = gts.numpy()
        for j in range(B): per.append(M.all_metrics((acc[j] > 0.5).astype(np.float32), gt[j, 0]))
    return M.aggregate(per)


def main():
    os.makedirs(args.out, exist_ok=True)
    df = pd.read_parquet(args.manifest)
    A = df[df.split == 'test_canonical'].reset_index(drop=True)
    B = df[df.split == 'holdout_combined'].reset_index(drop=True)
    if args.smoke: A = A.head(24); B = B.head(24)
    print(f"bucketA {len(A)} bucketB {len(B)}", flush=True)
    base = build(args.best_pt)
    out = {'model': 'MedSAM2-tiny', 'bucketA_n': int(len(A))}

    # base pass (Dice, ITA, dataset, calibration)
    rowsA, calibA = base_pass(base, A)
    dicesA = np.array([r['dice'] for r in rowsA])
    out['E_calibration_bucketA'] = calibA
    out['base_bucketA_dice'] = float(dicesA.mean())
    print(f"[base] bucketA Dice {dicesA.mean():.4f} | ECE {calibA['ece_15bin']:.4f} Brier {calibA['brier']:.4f}", flush=True)

    # C) fairness ITA
    groups = {}
    for r in rowsA:
        g = ita_group(r['ita']); groups.setdefault(g, []).append(r['dice'])
    order = ['I_verylight', 'II_light', 'III_intermediate', 'IV_tan', 'V-VI_brown_dark', 'unknown']
    fair = {g: {'n': len(groups[g]), 'dice_mean': float(np.mean(groups[g])), 'dice_std': float(np.std(groups[g]))}
            for g in order if g in groups}
    known = [g for g in fair if g != 'unknown']
    if known:
        ms = [fair[g]['dice_mean'] for g in known]
        fair['_gap_pp'] = round((max(ms) - min(ms)) * 100, 2)
    out['C_fairness_ITA_bucketA'] = fair
    print(f"[fairness] groups: " + ", ".join(f"{g}:{fair[g]['n']}({fair[g]['dice_mean']:.3f})" for g in known), flush=True)
    print(f"[fairness] gap {fair.get('_gap_pp')} pp", flush=True)

    # D) cross-dataset per dataset_origin on bucket B
    rowsB, _ = base_pass(base, B)
    byd = {}
    for r in rowsB: byd.setdefault(r['dataset'], []).append(r['dice'])
    out['D_cross_dataset_bucketB'] = {d: {'n': len(byd[d]), 'dice_mean': float(np.mean(byd[d]))} for d in sorted(byd)}
    print("[cross-dataset] " + ", ".join(f"{d}:{out['D_cross_dataset_bucketB'][d]['dice_mean']:.4f}(n{out['D_cross_dataset_bucketB'][d]['n']})" for d in out['D_cross_dataset_bucketB']), flush=True)

    # A) TTA
    tta = tta_pass(base, A)
    out['A_tta_bucketA'] = {'dice_mean': tta['dice']['mean'], 'dice_std': tta['dice']['std'],
                            'hd95_mean': tta['hd95']['mean'], 'delta_vs_base_pp': round((tta['dice']['mean'] - dicesA.mean()) * 100, 2)}
    print(f"[TTA] bucketA Dice {tta['dice']['mean']:.4f} ({out['A_tta_bucketA']['delta_vs_base_pp']:+.2f}pp)", flush=True)
    json.dump(out, open(os.path.join(args.out, 'f8_analyses.json'), 'w'), indent=2)

    # B) ensemble of 5 folds
    fold_pts = [os.path.join(args.fold_dir, f'fullft_fold{f}', 'best.pt') for f in range(5)]
    fold_pts = [p for p in fold_pts if os.path.exists(p)]
    models = [build(p) for p in fold_pts]
    ens = ensemble_pass(models, A)
    out['B_ensemble5fold_bucketA'] = {'n_models': len(models), 'dice_mean': ens['dice']['mean'], 'dice_std': ens['dice']['std'],
                                      'hd95_mean': ens['hd95']['mean'], 'delta_vs_base_pp': round((ens['dice']['mean'] - dicesA.mean()) * 100, 2)}
    print(f"[ensemble] {len(models)} folds bucketA Dice {ens['dice']['mean']:.4f} ({out['B_ensemble5fold_bucketA']['delta_vs_base_pp']:+.2f}pp)", flush=True)
    json.dump(out, open(os.path.join(args.out, 'f8_analyses.json'), 'w'), indent=2)
    print("\n=== F8 ANALYSES DONE ===", flush=True)


if __name__ == '__main__':
    main()
