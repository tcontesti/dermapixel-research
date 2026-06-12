#!/usr/bin/env python3
"""F8 (priority) - Box-prompt ROBUSTNESS curve for MedSAM2-tiny on bucket A.

Estimates the quality of dermapixel.eu's AUTOMATIC mode (detector -> box ->
MedSAM2-tiny), where the box is imperfect, vs the INTERACTIVE-mode ceiling
(clinician draws the box ~= GT box -> Dice ~0.956).

Eval-only (no training): load the M2 winner MedSAM2-tiny (F3 best.pt), evaluate
bucket A (1000 ISIC2018 canonical, LOCKED) feeding DEGRADED boxes instead of the
tight GT box, and report Dice vs box error.

Perturbations (on the tight GT box at 1024x1024):
  * GT (baseline, error 0)
  * jitter +/- {5,10,20} px : each of the 4 corners += U(-J,J), per-image seeded
  * scale {0.8,0.9,1.1,1.2}  : box scaled about its center (shrink / expand)
x-axis quantified by mean box-IoU(perturbed, GT). Dice via eval_metrics.
Deterministic: per-image rng seed = 1000*cfg_id + image_index.
"""
import os, sys, json, argparse
import numpy as np, torch, torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_metrics as M

P = argparse.ArgumentParser()
P.add_argument('--manifest', default=os.path.expanduser('~/panderm/output/m2_integral_max/manifests/m2_integral_max_v1c_local.parquet'))
P.add_argument('--best_pt', default=os.path.expanduser('~/panderm/output/m2_integral_max/outputs/M2_v2_medsam2/best.pt'))
P.add_argument('--model_id', default='facebook/sam2.1-hiera-tiny')
P.add_argument('--init_ckpt', default='/home/husll-spark-01/.cache/huggingface/hub/models--wanglab--MedSAM2/snapshots/e4a6f35edd7e091619cbc0750f462f1574e23955/MedSAM2_latest.pt')
P.add_argument('--out', default=os.path.expanduser('~/panderm/output/m2_integral_max/outputs/M2_v7_f8_box_robustness'))
P.add_argument('--img_size', type=int, default=1024)
P.add_argument('--smoke', action='store_true')
args = P.parse_args()
DEVICE = torch.device('cuda')
IMNET_MEAN = np.array([0.485, 0.456, 0.406], np.float32); IMNET_STD = np.array([0.229, 0.224, 0.225], np.float32)

# (name, kind, value)  kind in {'gt','jitter','scale'}
CONFIGS = [
    ('gt', 'gt', 0.0),
    ('jitter5', 'jitter', 5), ('jitter10', 'jitter', 10), ('jitter20', 'jitter', 20),
    ('scale0.8', 'scale', 0.8), ('scale0.9', 'scale', 0.9),
    ('scale1.1', 'scale', 1.1), ('scale1.2', 'scale', 1.2),
]


class DS(Dataset):
    def __init__(self, df, isz):
        self.df = df.reset_index(drop=True); self.isz = isz
    def __len__(self): return len(self.df)
    def __getitem__(self, i):
        r = self.df.iloc[i]
        img = np.array(Image.open(r.image_path).convert('RGB').resize((self.isz, self.isz), Image.BILINEAR), np.float32) / 255.
        gt = (np.array(Image.open(r.mask_path).convert('L').resize((self.isz, self.isz), Image.NEAREST), np.float32) > 127.5).astype(np.float32)
        ys, xs = np.where(gt > 0.5)
        box = np.array([0, 0, self.isz, self.isz], np.float32) if len(ys) == 0 else np.array([xs.min(), ys.min(), xs.max(), ys.max()], np.float32)
        img = (img - IMNET_MEAN) / IMNET_STD
        return torch.from_numpy(img).permute(2, 0, 1).float(), torch.from_numpy(gt)[None].float(), box, i


def perturb(box, kind, val, idx, cfg_id, S):
    x1, y1, x2, y2 = box.astype(np.float64)
    if kind == 'gt':
        nb = np.array([x1, y1, x2, y2])
    elif kind == 'jitter':
        rng = np.random.default_rng(1000 * cfg_id + int(idx))
        d = rng.uniform(-val, val, size=4)
        nb = np.array([x1 + d[0], y1 + d[1], x2 + d[2], y2 + d[3]])
    else:  # scale about center
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2; w, h = (x2 - x1) * val, (y2 - y1) * val
        nb = np.array([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2])
    nb = np.clip(nb, 0, S - 1)
    if nb[2] <= nb[0] + 1: nb[2] = min(S - 1, nb[0] + 2)
    if nb[3] <= nb[1] + 1: nb[3] = min(S - 1, nb[1] + 2)
    return nb.astype(np.float32)


def box_iou(a, b):
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1]); ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1); inter = iw * ih
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return float(inter / ua) if ua > 0 else 0.0


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


def build():
    from sam2.build_sam import build_sam2_hf
    m = build_sam2_hf(args.model_id).to(DEVICE)
    ck = torch.load(args.init_ckpt, map_location=DEVICE, weights_only=False)
    sd = ck['model'] if (isinstance(ck, dict) and 'model' in ck) else ck
    m.load_state_dict(sd, strict=False)
    best = torch.load(args.best_pt, map_location=DEVICE, weights_only=False)
    m.load_state_dict(best['state'], strict=False)
    m.eval()
    print(f"[build] MedSAM2-tiny loaded (best.pt val_dice={best.get('val_dice')})", flush=True)
    return m


@torch.no_grad()
def eval_config(model, df, cfg_id, name, kind, val):
    dl = DataLoader(DS(df, args.img_size), batch_size=4, shuffle=False, num_workers=4, pin_memory=True)
    per, ious = [], []
    for imgs, gts, boxes, idxs in dl:
        boxes = boxes.numpy(); idxs = idxs.numpy()
        pboxes = np.stack([perturb(boxes[j], kind, val, idxs[j], cfg_id, args.img_size) for j in range(len(idxs))])
        for j in range(len(idxs)): ious.append(box_iou(pboxes[j], boxes[j]))
        imgs = imgs.to(DEVICE)
        with torch.amp.autocast('cuda', dtype=torch.bfloat16):
            lg = forward_sam2_batch(model, imgs, torch.from_numpy(pboxes).to(DEVICE), args.img_size)
        pred = (torch.sigmoid(lg) > 0.5).float().cpu().numpy(); gt = gts.numpy()
        for j in range(pred.shape[0]): per.append(M.all_metrics(pred[j, 0], gt[j, 0]))
    agg = M.aggregate(per)
    return {'name': name, 'kind': kind, 'value': val, 'mean_box_iou_vs_gt': float(np.mean(ious)),
            'dice_mean': agg['dice']['mean'], 'dice_std': agg['dice']['std'],
            'iou_mean': agg['iou']['mean'], 'hd95_mean': agg['hd95']['mean'], 'n': len(per)}


def main():
    os.makedirs(args.out, exist_ok=True)
    df = pd.read_parquet(args.manifest)
    A = df[df.split == 'test_canonical'].reset_index(drop=True)
    if args.smoke: A = A.head(24)
    print(f"bucket A n={len(A)}", flush=True)
    model = build()
    results = {'model': 'MedSAM2-tiny', 'best_pt': args.best_pt, 'bucketA_n': int(len(A)), 'curve': {}}
    for cid, (name, kind, val) in enumerate(CONFIGS):
        r = eval_config(model, A, cid, name, kind, val)
        results['curve'][name] = r
        print(f"  {name:10s} boxIoU={r['mean_box_iou_vs_gt']:.3f}  Dice={r['dice_mean']:.4f}+-{r['dice_std']:.3f}  HD95={r['hd95_mean']:.1f}", flush=True)
        json.dump(results, open(os.path.join(args.out, 'box_robustness.json'), 'w'), indent=2)
    gt = results['curve']['gt']['dice_mean']
    for name in results['curve']:
        results['curve'][name]['delta_vs_gt_pp'] = round((results['curve'][name]['dice_mean'] - gt) * 100, 2)
    json.dump(results, open(os.path.join(args.out, 'box_robustness.json'), 'w'), indent=2)
    print(f"\n=== BOX ROBUSTNESS DONE (ceiling GT Dice {gt:.4f}) ===", flush=True)
    for name in results['curve']:
        c = results['curve'][name]
        print(f"  {name:10s} boxIoU {c['mean_box_iou_vs_gt']:.3f} -> Dice {c['dice_mean']:.4f} ({c['delta_vs_gt_pp']:+.2f}pp)", flush=True)


if __name__ == '__main__':
    main()
