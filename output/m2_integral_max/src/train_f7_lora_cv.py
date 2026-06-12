#!/usr/bin/env python3
"""F7 - LoRA ablation + 5-fold CV on MedSAM2-tiny (the M2 winner, 0.9556).

Box-prompted, high-ceiling regime -> LoRA deltas are expected to be small.
The VALUE of this experiment is the 5-fold CV confidence interval on the
headline number (0.9556 was full_ft MedSAM2-tiny).

Design (user-approved 2026-06-11, option B):
  * full_ft MedSAM2-tiny  x 5-fold CV  -> 95% CI of bucket-A Dice (the 0.9556).
  * LoRA r=4/8/16/32       x 1 fold (fold 0) -> rank ablation deltas vs full_ft fold 0.
  = 9 trainings total, ~20 h.

CV protocol: pool the train+val splits (12541 imgs), StratifiedKFold(5) by
dataset_origin (seed 42). For fold f: that fold = val (early stop), other 4 =
train. bucket A (1000 ISIC2018 canonical, LOCKED) and bucket B (660 holdout)
are EXCLUDED from every fold and stay the fixed evaluation sets, identical to
F2-F6 -> CV numbers are directly comparable to the 0.9556 / 0.9562 headline.

Recipe identical to F3 MedSAM2 (config_f2.json): AdamW lr1e-4 wd0.01, batch 4
grad_accum 4 (eff 16), warmup 200 + cosine, 30 ep, patience 5, bf16, 1024x1024,
Dice+BCE, aug HFlip/VFlip/Rot90/ColorJitter, GT-bbox prompt (train jitter 20).

Resumable: a run whose results.json already exists is skipped. Each run writes
results immediately; F7_summary.json is (re)written after every run.
"""
import os, sys, time, json, random, argparse
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import pandas as pd
from sklearn.model_selection import StratifiedKFold
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_metrics as M

P = argparse.ArgumentParser()
P.add_argument('--manifest', default=os.path.expanduser('~/panderm/output/m2_integral_max/manifests/m2_integral_max_v1c_local.parquet'))
P.add_argument('--out', default=os.path.expanduser('~/panderm/output/m2_integral_max/outputs/M2_v6_f7_cv'))
P.add_argument('--model_id', default='facebook/sam2.1-hiera-tiny')
P.add_argument('--init_ckpt', default='/home/husll-spark-01/.cache/huggingface/hub/models--wanglab--MedSAM2/snapshots/e4a6f35edd7e091619cbc0750f462f1574e23955/MedSAM2_latest.pt')
P.add_argument('--init_ckpt_key', default='model')
P.add_argument('--epochs', type=int, default=30)
P.add_argument('--lr', type=float, default=1e-4)
P.add_argument('--batch_size', type=int, default=4)
P.add_argument('--grad_accum', type=int, default=4)
P.add_argument('--img_size', type=int, default=1024)
P.add_argument('--warmup', type=int, default=200)
P.add_argument('--patience', type=int, default=5)
P.add_argument('--n_folds', type=int, default=5)
P.add_argument('--seed', type=int, default=42)
P.add_argument('--smoke', action='store_true')
args = P.parse_args()
random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed); torch.cuda.manual_seed_all(args.seed)
DEVICE = torch.device('cuda')
SAM_MEAN = np.array([0.485, 0.456, 0.406], np.float32); SAM_STD = np.array([0.229, 0.224, 0.225], np.float32)
T_0975 = {4: 2.776445}  # Student-t 97.5% pct, df=n_folds-1=4


class ManifestSeg(Dataset):
    def __init__(self, df, img_size, train=False):
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
        img = np.array(Image.open(r.image_path).convert('RGB').resize((self.img_size, self.img_size), Image.BILINEAR), np.float32) / 255.0
        mask = (np.array(Image.open(r.mask_path).convert('L').resize((self.img_size, self.img_size), Image.NEAREST), np.float32) > 127.5).astype(np.float32)
        if self.train:
            if random.random() < 0.5: img = img[:, ::-1].copy(); mask = mask[:, ::-1].copy()
            if random.random() < 0.5: img = img[::-1].copy(); mask = mask[::-1].copy()
            k = random.randint(0, 3)
            if k: img = np.rot90(img, k).copy(); mask = np.rot90(mask, k).copy()
            if random.random() < 0.5: img = np.clip(img * (1 + (random.random() - 0.5) * 0.2) + (random.random() - 0.5) * 0.1, 0, 1)
        img = (img - SAM_MEAN) / SAM_STD
        return (torch.from_numpy(img).permute(2, 0, 1).float(),
                torch.from_numpy(mask).unsqueeze(0).float(), self._bbox(mask), r.dataset_origin, r.image_path)


def dice_loss(pred, tgt, smooth=1.0):
    pred = torch.sigmoid(pred); pf = pred.view(pred.size(0), -1); tf = tgt.view(tgt.size(0), -1)
    inter = (pf * tf).sum(1)
    return 1 - ((2 * inter + smooth) / (pf.sum(1) + tf.sum(1) + smooth)).mean()


def combined_loss(pred, tgt):
    return 0.5 * F.binary_cross_entropy_with_logits(pred, tgt) + 0.5 * dice_loss(pred, tgt)


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
        low, _, _, _ = model.sam_mask_decoder(
            image_embeddings=fi[-1], image_pe=model.sam_prompt_encoder.get_dense_pe(),
            sparse_prompt_embeddings=se, dense_prompt_embeddings=de,
            multimask_output=False, repeat_image=False, high_res_features=fi[:-1])
        out.append(F.interpolate(low, (img_size, img_size), mode='bilinear', align_corners=False)[:, 0:1])
    return torch.cat(out, 0)


def build_model(mode, lora_r, lora_alpha):
    from sam2.build_sam import build_sam2_hf
    m = build_sam2_hf(args.model_id).to(DEVICE)
    ck = torch.load(args.init_ckpt, map_location=DEVICE, weights_only=False)
    sd = ck[args.init_ckpt_key] if (isinstance(ck, dict) and args.init_ckpt_key in ck) else ck
    probe = 'image_encoder.trunk.patch_embed.proj.weight'
    before = m.state_dict()[probe].detach().float().clone()
    m.load_state_dict(sd, strict=False)
    after = m.state_dict()[probe].detach().float()
    assert (not torch.allclose(before, after)) and torch.allclose(after, sd[probe].to(DEVICE).float()), \
        "INIT CKPT LOADER BUG: image encoder did not load MedSAM2 weights"
    for p in m.image_encoder.parameters(): p.requires_grad = False
    for p in m.sam_prompt_encoder.parameters(): p.requires_grad = True
    if mode == 'full_ft':
        for p in m.sam_mask_decoder.parameters(): p.requires_grad = True
    else:
        from peft import LoraConfig, get_peft_model
        cfg = LoraConfig(r=lora_r, lora_alpha=lora_alpha, lora_dropout=0.1,
                         target_modules=['q_proj', 'k_proj', 'v_proj', 'out_proj'], bias='none')
        m.sam_mask_decoder = get_peft_model(m.sam_mask_decoder, cfg)
    tr = sum(p.numel() for p in m.parameters() if p.requires_grad)
    tot = sum(p.numel() for p in m.parameters())
    print(f"[{mode} r{lora_r}] trainable {tr/1e6:.3f}M / {tot/1e6:.1f}M", flush=True)
    return m, tr


@torch.no_grad()
def evaluate(model, df, by_dataset=False):
    model.eval(); dl = DataLoader(ManifestSeg(df, args.img_size, False), batch_size=4, shuffle=False, num_workers=4, pin_memory=True)
    per, origins = [], []
    for imgs, masks, bb, dso, _ in dl:
        imgs = imgs.to(DEVICE); bb = bb.to(DEVICE)
        with torch.amp.autocast('cuda', dtype=torch.bfloat16):
            lg = forward_sam2_batch(model, imgs, bb, args.img_size)
        pred = (torch.sigmoid(lg) > 0.5).float().cpu().numpy(); gt = masks.numpy()
        for j in range(pred.shape[0]): per.append(M.all_metrics(pred[j, 0], gt[j, 0])); origins.append(dso[j])
    res = {"overall": M.aggregate(per), "n": len(per)}
    if by_dataset:
        origins = np.array(origins)
        res["per_dataset"] = {o: M.aggregate([per[k] for k in range(len(per)) if origins[k] == o]) for o in sorted(set(origins))}
    return res


def measure_latency(model, df, n=50):
    model.eval(); dl = DataLoader(ManifestSeg(df.head(n), args.img_size, False), batch_size=1, num_workers=2)
    torch.cuda.synchronize(); ts = []
    with torch.no_grad():
        for imgs, _, bb, _, _ in dl:
            imgs = imgs.to(DEVICE); bb = bb.to(DEVICE); torch.cuda.synchronize(); t0 = time.time()
            with torch.amp.autocast('cuda', dtype=torch.bfloat16): forward_sam2_batch(model, imgs, bb, args.img_size)
            torch.cuda.synchronize(); ts.append((time.time() - t0) * 1000)
    return float(np.median(ts[2:]))


def train_run(tag, mode, lora_r, lora_alpha, tr_df, va_df, bA, bB, outdir):
    os.makedirs(outdir, exist_ok=True)
    rp = os.path.join(outdir, 'results.json')
    if os.path.exists(rp):
        print(f"[SKIP] {tag} (results.json exists)", flush=True)
        return json.load(open(rp))
    if args.smoke:
        tr_df = tr_df.groupby('dataset_origin', group_keys=False).head(8)
        va_df = va_df.groupby('dataset_origin', group_keys=False).head(8)
    print(f"\n===== RUN {tag}  mode={mode} r={lora_r} train={len(tr_df)} val={len(va_df)} =====", flush=True)
    model, n_tr = build_model(mode, lora_r, lora_alpha)
    tl = DataLoader(ManifestSeg(tr_df, args.img_size, True), batch_size=args.batch_size, shuffle=True, num_workers=4, pin_memory=True, drop_last=True)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=args.lr, weight_decay=0.01)
    epochs = 1 if args.smoke else args.epochs
    total = max(1, (len(tl) // args.grad_accum) * epochs); warm = min(args.warmup, max(1, total - 1))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (s + 1) / warm if s < warm else 0.5 * (1 + np.cos(np.pi * (s - warm) / max(1, total - warm))))
    best, best_ep, since = 0.0, 0, 0
    for ep in range(1, epochs + 1):
        model.train(); model.image_encoder.eval(); t0 = time.time(); opt.zero_grad(); run = 0.0
        for bi, (imgs, masks, bb, _, _) in enumerate(tl):
            imgs = imgs.to(DEVICE); masks = masks.to(DEVICE); bb = bb.to(DEVICE)
            with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                lg = forward_sam2_batch(model, imgs, bb, args.img_size); loss = combined_loss(lg, masks) / args.grad_accum
            loss.backward(); run += loss.item() * args.grad_accum
            if (bi + 1) % args.grad_accum == 0:
                torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
                opt.step(); opt.zero_grad(); sched.step()
        vd = evaluate(model, va_df)['overall']['dice']['mean']
        print(f"  [{tag}] ep {ep} loss {run/max(1,len(tl)):.4f} valDice {vd:.4f} lr {sched.get_last_lr()[0]:.2e} {time.time()-t0:.0f}s", flush=True)
        if vd > best:
            best, best_ep, since = vd, ep, 0
            slim = {k: v for k, v in model.state_dict().items() if 'mask_decoder' in k or 'prompt_encoder' in k or 'lora' in k.lower()}
            torch.save({'epoch': ep, 'val_dice': vd, 'mode': mode, 'lora_r': lora_r, 'state': slim}, os.path.join(outdir, 'best.pt'))
        else:
            since += 1
            if since >= args.patience and not args.smoke: print(f"  [{tag}] early stop @ ep {ep}", flush=True); break
    ck = torch.load(os.path.join(outdir, 'best.pt'), map_location=DEVICE, weights_only=False)
    model.load_state_dict(ck['state'], strict=False); model.eval()
    if args.smoke: bA = bA.head(16); bB = bB.head(16)
    results = {'tag': tag, 'mode': mode, 'lora_r': lora_r, 'lora_alpha': lora_alpha, 'trainable_params': int(n_tr),
               'best_val_dice': best, 'best_epoch': best_ep, 'n_train': int(len(tr_df)), 'n_val': int(len(va_df)),
               'baseline_M2_v0_dice_isic2018': 0.9473, 'headline_medsam2_fullft': 0.9556,
               'bucketA_canonical_isic2018_test': evaluate(model, bA),
               'bucketB_combined_holdout': evaluate(model, bB, by_dataset=True),
               'latency_ms_1024': measure_latency(model, bA)}
    da = results['bucketA_canonical_isic2018_test']['overall']['dice']['mean']
    results['vs_baseline_pp'] = round((da - 0.9473) * 100, 2)
    json.dump(results, open(rp, 'w'), indent=2)
    print(f"=== {tag} DONE bucketA Dice {da:.4f} (vs 0.9473 -> {results['vs_baseline_pp']:+.2f} pp) | lat {results['latency_ms_1024']:.0f} ms ===", flush=True)
    del model; torch.cuda.empty_cache()
    return results


def ci95(vals):
    v = np.array(vals, np.float64); n = len(v)
    mean = float(v.mean()); sd = float(v.std(ddof=1)) if n > 1 else 0.0
    sem = sd / np.sqrt(n) if n > 1 else 0.0
    t = T_0975.get(n - 1, 2.776445)
    return {"mean": mean, "std": sd, "sem": sem, "ci95_low": mean - t * sem, "ci95_high": mean + t * sem, "n": n, "values": [float(x) for x in v]}


def main():
    os.makedirs(args.out, exist_ok=True)
    df = pd.read_parquet(args.manifest)
    print("manifest:", len(df), df.split.value_counts().to_dict(), flush=True)
    json.dump(vars(args), open(os.path.join(args.out, 'config_f7.json'), 'w'), indent=2, default=str)
    bA = df[df.split == 'test_canonical'].reset_index(drop=True)
    bB = df[df.split == 'holdout_combined'].reset_index(drop=True)
    pool = df[df.split.isin(['train', 'val'])].reset_index(drop=True)
    print(f"pool {len(pool)} | bucketA {len(bA)} | bucketB {len(bB)}", flush=True)
    skf = StratifiedKFold(n_splits=args.n_folds, shuffle=True, random_state=args.seed)
    folds = list(skf.split(pool, pool['dataset_origin']))

    summary = {'design': 'full_ft x5-fold CV + LoRA r4/8/16/32 x1-fold', 'runs': {}}

    # --- full_ft 5-fold CV ---
    for f, (tr_idx, va_idx) in enumerate(folds):
        tag = f'fullft_fold{f}'
        r = train_run(tag, 'full_ft', 0, 0, pool.iloc[tr_idx], pool.iloc[va_idx], bA, bB, os.path.join(args.out, tag))
        summary['runs'][tag] = {'bucketA_dice': r['bucketA_canonical_isic2018_test']['overall']['dice']['mean'],
                                'bucketB_dice': r['bucketB_combined_holdout']['overall']['dice']['mean'],
                                'best_val_dice': r['best_val_dice'], 'best_epoch': r['best_epoch'], 'latency_ms': r['latency_ms_1024']}
        json.dump(summary, open(os.path.join(args.out, 'F7_summary.json'), 'w'), indent=2)

    # --- LoRA rank ablation, fold 0 only ---
    tr_idx, va_idx = folds[0]
    for lr_r in [4, 8, 16, 32]:
        tag = f'lora_r{lr_r}_fold0'
        r = train_run(tag, 'lora', lr_r, 2 * lr_r, pool.iloc[tr_idx], pool.iloc[va_idx], bA, bB, os.path.join(args.out, tag))
        summary['runs'][tag] = {'bucketA_dice': r['bucketA_canonical_isic2018_test']['overall']['dice']['mean'],
                                'bucketB_dice': r['bucketB_combined_holdout']['overall']['dice']['mean'],
                                'best_val_dice': r['best_val_dice'], 'best_epoch': r['best_epoch'],
                                'trainable_params': r['trainable_params'], 'latency_ms': r['latency_ms_1024']}
        json.dump(summary, open(os.path.join(args.out, 'F7_summary.json'), 'w'), indent=2)

    # --- aggregate ---
    ft_A = [summary['runs'][f'fullft_fold{f}']['bucketA_dice'] for f in range(args.n_folds)]
    ft_B = [summary['runs'][f'fullft_fold{f}']['bucketB_dice'] for f in range(args.n_folds)]
    summary['fullft_5fold_CV'] = {'bucketA': ci95(ft_A), 'bucketB': ci95(ft_B), 'headline_0.9556_in_CI':
                                  bool(ci95(ft_A)['ci95_low'] <= 0.9556 <= ci95(ft_A)['ci95_high'])}
    ft0 = summary['runs']['fullft_fold0']['bucketA_dice']
    summary['lora_ablation_fold0'] = {f'r{r}': {'bucketA_dice': summary['runs'][f'lora_r{r}_fold0']['bucketA_dice'],
                                                'delta_vs_fullft_pp': round((summary['runs'][f'lora_r{r}_fold0']['bucketA_dice'] - ft0) * 100, 3),
                                                'trainable_params': summary['runs'][f'lora_r{r}_fold0']['trainable_params']} for r in [4, 8, 16, 32]}
    summary['lora_ablation_fold0']['fullft_fold0_ref'] = ft0
    json.dump(summary, open(os.path.join(args.out, 'F7_summary.json'), 'w'), indent=2)
    cv = summary['fullft_5fold_CV']['bucketA']
    print(f"\n===== F7 DONE =====\nfull_ft 5-fold bucketA Dice = {cv['mean']:.4f} "
          f"(95% CI {cv['ci95_low']:.4f}-{cv['ci95_high']:.4f}, sd {cv['std']:.4f}) | 0.9556 in CI: {summary['fullft_5fold_CV']['headline_0.9556_in_CI']}", flush=True)
    for r in [4, 8, 16, 32]:
        a = summary['lora_ablation_fold0'][f'r{r}']
        print(f"  LoRA r{r}: bucketA {a['bucketA_dice']:.4f}  delta {a['delta_vs_fullft_pp']:+.3f}pp  ({a['trainable_params']/1e6:.2f}M params)", flush=True)


if __name__ == '__main__':
    main()
