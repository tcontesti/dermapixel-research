#!/usr/bin/env python3
"""F5 - MedSAM v1 (SAM ViT-B) segmentation on v1c via transformers SamModel.
Same regime as F2/F3 (frozen vision encoder, FT mask_decoder + prompt_encoder,
GT-bbox prompt, Dice+BCE, eval bucket A/B, HD95) but SAM-v1 architecture/API.
SAM-v1 normalization (0-255 mean/std), not the SAM2/ImageNet 0-1 norm.
"""
import os, sys, time, json, random, argparse
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import pandas as pd
from transformers import SamModel
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_metrics as M

P = argparse.ArgumentParser()
P.add_argument('--model_id', default='wanglab/medsam-vit-base')
P.add_argument('--manifest', default=os.path.expanduser('~/panderm/output/m2_integral_max/manifests/m2_integral_max_v1c_local.parquet'))
P.add_argument('--out', required=True)
P.add_argument('--epochs', type=int, default=30)
P.add_argument('--lr', type=float, default=1e-4)
P.add_argument('--batch_size', type=int, default=4)
P.add_argument('--grad_accum', type=int, default=4)
P.add_argument('--img_size', type=int, default=1024)
P.add_argument('--warmup', type=int, default=200)
P.add_argument('--patience', type=int, default=5)
P.add_argument('--seed', type=int, default=42)
P.add_argument('--smoke', action='store_true')
args = P.parse_args()
random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed); torch.cuda.manual_seed_all(args.seed)
DEVICE = torch.device('cuda')
# SAM-v1 normalization (applied on 0-255 pixel values)
MEAN = np.array([123.675, 116.28, 103.53], np.float32); STD = np.array([58.395, 57.12, 57.375], np.float32)


class ManifestSeg(Dataset):
    def __init__(self, df, img_size, train=False, smoke=False):
        if smoke: df = df.groupby('dataset_origin', group_keys=False).head(8)
        self.df = df.reset_index(drop=True); self.img_size = img_size; self.train = train

    def __len__(self): return len(self.df)

    def _bbox(self, mask, jitter=20):
        ys, xs = np.where(mask > 0.5)
        if len(ys) == 0: return np.array([0, 0, self.img_size, self.img_size], np.float32)
        x1, y1, x2, y2 = xs.min(), ys.min(), xs.max(), ys.max()
        if self.train and jitter > 0:
            x1 = max(0, x1 - random.randint(0, jitter)); y1 = max(0, y1 - random.randint(0, jitter))
            x2 = min(self.img_size - 1, x2 + random.randint(0, jitter)); y2 = min(self.img_size - 1, y2 + random.randint(0, jitter))
        return np.array([x1, y1, x2, y2], np.float32)

    def __getitem__(self, i):
        r = self.df.iloc[i]
        img = np.array(Image.open(r.image_path).convert('RGB').resize((self.img_size, self.img_size), Image.BILINEAR), np.float32)
        mask = (np.array(Image.open(r.mask_path).convert('L').resize((self.img_size, self.img_size), Image.NEAREST), np.float32) > 127.5).astype(np.float32)
        if self.train:
            if random.random() < 0.5: img = img[:, ::-1].copy(); mask = mask[:, ::-1].copy()
            if random.random() < 0.5: img = img[::-1].copy(); mask = mask[::-1].copy()
            k = random.randint(0, 3)
            if k: img = np.rot90(img, k).copy(); mask = np.rot90(mask, k).copy()
            if random.random() < 0.5: img = np.clip(img * (1 + (random.random() - 0.5) * 0.2) + (random.random() - 0.5) * 25, 0, 255)
        img = (img - MEAN) / STD
        return (torch.from_numpy(img).permute(2, 0, 1).float(),
                torch.from_numpy(mask).unsqueeze(0).float(),
                self._bbox(mask), r.dataset_origin, r.image_path)


def dice_loss(pred, tgt, smooth=1.0):
    pred = torch.sigmoid(pred); pf = pred.view(pred.size(0), -1); tf = tgt.view(tgt.size(0), -1)
    inter = (pf * tf).sum(1)
    return 1 - ((2 * inter + smooth) / (pf.sum(1) + tf.sum(1) + smooth)).mean()


def combined_loss(pred, tgt):
    return 0.5 * F.binary_cross_entropy_with_logits(pred, tgt) + 0.5 * dice_loss(pred, tgt)


def forward_samv1(model, pixel_values, bboxes, img_size):
    # input_boxes shape (B, nb_boxes, 4) in input-image (1024) coords
    ib = bboxes.unsqueeze(1)  # [B,1,4]
    out = model(pixel_values=pixel_values, input_boxes=ib, multimask_output=False)
    low = out.pred_masks  # [B, nb_boxes, num_masks, h, w]
    low = low[:, 0]        # [B, num_masks, h, w] -> num_masks=1
    return F.interpolate(low, (img_size, img_size), mode='bilinear', align_corners=False)  # [B,1,1024,1024]


def build():
    m = SamModel.from_pretrained(args.model_id).to(DEVICE)
    for p in m.vision_encoder.parameters(): p.requires_grad = False
    for p in m.prompt_encoder.parameters(): p.requires_grad = True
    for p in m.mask_decoder.parameters(): p.requires_grad = True
    tr = sum(p.numel() for p in m.parameters() if p.requires_grad)
    tot = sum(p.numel() for p in m.parameters())
    # quick sanity: vision encoder param checksum (confirms medical weights, not random)
    probe = next(m.vision_encoder.parameters()).detach().float().abs().mean().item()
    print(f"[{args.model_id}] trainable {tr/1e6:.3f}M / {tot/1e6:.1f}M  enc_probe={probe:.4f}", flush=True)
    return m, tr


@torch.no_grad()
def evaluate(model, df, by_dataset=False):
    model.eval(); ds = ManifestSeg(df, args.img_size, train=False)
    dl = DataLoader(ds, batch_size=4, shuffle=False, num_workers=4, pin_memory=True)
    per, origins = [], []
    for imgs, masks, bb, dso, _ in dl:
        imgs = imgs.to(DEVICE); bb = bb.to(DEVICE)
        with torch.amp.autocast('cuda', dtype=torch.bfloat16):
            lg = forward_samv1(model, imgs, bb, args.img_size)
        pred = (torch.sigmoid(lg) > 0.5).float().cpu().numpy(); gt = masks.numpy()
        for j in range(pred.shape[0]):
            per.append(M.all_metrics(pred[j, 0], gt[j, 0])); origins.append(dso[j])
    res = {"overall": M.aggregate(per), "n": len(per)}
    if by_dataset:
        origins = np.array(origins)
        res["per_dataset"] = {o: M.aggregate([per[k] for k in range(len(per)) if origins[k] == o]) for o in sorted(set(origins))}
    return res


def measure_latency(model, df, n=50):
    model.eval(); ds = ManifestSeg(df.head(n), args.img_size); dl = DataLoader(ds, batch_size=1, num_workers=2)
    torch.cuda.synchronize(); ts = []
    with torch.no_grad():
        for imgs, _, bb, _, _ in dl:
            imgs = imgs.to(DEVICE); bb = bb.to(DEVICE); torch.cuda.synchronize(); t0 = time.time()
            with torch.amp.autocast('cuda', dtype=torch.bfloat16): forward_samv1(model, imgs, bb, args.img_size)
            torch.cuda.synchronize(); ts.append((time.time() - t0) * 1000)
    return float(np.median(ts[2:]))


def save_sanity(model, df, outdir, n=5):
    os.makedirs(outdir, exist_ok=True); sub = df.sample(min(n, len(df)), random_state=args.seed)
    ds = ManifestSeg(sub, args.img_size); model.eval()
    for k in range(len(ds)):
        imgs, masks, bb, _, path = ds[k]
        with torch.no_grad(), torch.amp.autocast('cuda', dtype=torch.bfloat16):
            lg = forward_samv1(model, imgs.unsqueeze(0).to(DEVICE), torch.as_tensor(bb, dtype=torch.float32)[None].to(DEVICE), args.img_size)
        pred = (torch.sigmoid(lg)[0, 0] > 0.5).cpu().numpy().astype(np.uint8) * 255
        gt = (masks[0].numpy() * 255).astype(np.uint8)
        raw = np.array(Image.open(path).convert('RGB').resize((args.img_size, args.img_size)))
        Image.fromarray(np.concatenate([raw, np.stack([gt] * 3, -1), np.stack([pred] * 3, -1)], 1)).save(os.path.join(outdir, f"sanity_{k}.png"))


def main():
    df = pd.read_parquet(args.manifest)
    os.makedirs(args.out, exist_ok=True)
    print("manifest:", len(df), df.split.value_counts().to_dict(), flush=True)
    model, n_tr = build()
    tr_df = df[df.split == 'train']; va_df = df[df.split == 'val']
    tr = ManifestSeg(tr_df, args.img_size, train=True, smoke=args.smoke)
    va_eval = (va_df.groupby('dataset_origin', group_keys=False).head(8) if args.smoke else va_df)
    tl = DataLoader(tr, batch_size=args.batch_size, shuffle=True, num_workers=4, pin_memory=True, drop_last=True)
    print(f"train {len(tr)} val {len(va_eval)}", flush=True)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=args.lr, weight_decay=0.01)
    epochs = 1 if args.smoke else args.epochs
    total = max(1, (len(tl) // args.grad_accum) * epochs); warm = min(args.warmup, max(1, total - 1))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (s + 1) / warm if s < warm else 0.5 * (1 + np.cos(np.pi * (s - warm) / max(1, total - warm))))
    best, best_ep, since = 0.0, 0, 0
    for ep in range(1, epochs + 1):
        model.train(); model.vision_encoder.eval(); t0 = time.time(); opt.zero_grad(); run = 0.0
        for bi, (imgs, masks, bb, _, _) in enumerate(tl):
            imgs = imgs.to(DEVICE); masks = masks.to(DEVICE); bb = bb.to(DEVICE)
            with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                lg = forward_samv1(model, imgs, bb, args.img_size); loss = combined_loss(lg, masks) / args.grad_accum
            loss.backward(); run += loss.item() * args.grad_accum
            if (bi + 1) % args.grad_accum == 0:
                torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
                opt.step(); opt.zero_grad(); sched.step()
        vd = evaluate(model, va_eval)['overall']['dice']['mean']
        print(f"ep {ep} loss {run/max(1,len(tl)):.4f} valDice {vd:.4f} lr {sched.get_last_lr()[0]:.2e} {time.time()-t0:.0f}s", flush=True)
        if vd > best:
            best, best_ep, since = vd, ep, 0
            slim = {k: v for k, v in model.state_dict().items() if 'mask_decoder' in k or 'prompt_encoder' in k}
            torch.save({'epoch': ep, 'val_dice': vd, 'state': slim}, os.path.join(args.out, 'best.pt'))
        else:
            since += 1
            if since >= args.patience and not args.smoke: print(f"early stop @ ep {ep}", flush=True); break
    ck = torch.load(os.path.join(args.out, 'best.pt'), map_location=DEVICE, weights_only=False)
    model.load_state_dict(ck['state'], strict=False); model.eval()
    print(f"best valDice {best:.4f} @ ep {best_ep}", flush=True)
    bA = df[df.split == 'test_canonical']; bB = df[df.split == 'holdout_combined']
    if args.smoke: bA = bA.head(16); bB = bB.head(16)
    results = {'model_id': args.model_id, 'trainable_params': int(n_tr), 'best_val_dice': best, 'best_epoch': best_ep,
               'baseline_M2_v0_dice_isic2018': 0.9473,
               'bucketA_canonical_isic2018_test': evaluate(model, bA),
               'bucketB_combined_holdout': evaluate(model, bB, by_dataset=True),
               'latency_ms_1024': measure_latency(model, bA)}
    da = results['bucketA_canonical_isic2018_test']['overall']['dice']['mean']
    results['vs_baseline_pp'] = round((da - 0.9473) * 100, 2)
    json.dump(results, open(os.path.join(args.out, 'results.json'), 'w'), indent=2)
    save_sanity(model, bB, os.path.join(args.out, 'sanity_check'))
    print(f"=== DONE  bucketA Dice {da:.4f} (vs 0.9473 -> {results['vs_baseline_pp']:+.2f} pp) | latency {results['latency_ms_1024']:.0f} ms ===", flush=True)


if __name__ == '__main__':
    main()
