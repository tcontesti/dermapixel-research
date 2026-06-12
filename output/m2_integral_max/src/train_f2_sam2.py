#!/usr/bin/env python3
"""F2 - SAM2.1-Large segmentation on M2-INTEGRAL-MAX v1b data.
Replicates the production architecture (frozen image encoder, trainable
mask-decoder + prompt-encoder, GT-bbox prompt) that produced Dice 0.9473.

--mode full_ft : dense FT of mask decoder + prompt encoder (== production)
--mode lora    : LoRA r/alpha on mask-decoder Linears + trainable prompt enc
--mode both    : run both sequentially

Recipe (plan sec 4.1): AdamW lr1e-4 wd0.01, grad_accum 4 (eff batch 16),
warmup 200 + cosine, 30 ep, early stop patience 5, bf16, 1024x1024,
Dice+BCE (0.5/0.5), aug HFlip/VFlip/Rot90/ColorJitter(mild).
Eval: bucket A (canonical ISIC2018 test, vs 0.9473) + bucket B
(combined holdout) + per dataset_origin. Metrics via eval_metrics.py.
"""
import os, sys, time, json, random, argparse
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_metrics as M

P = argparse.ArgumentParser()
P.add_argument('--mode', choices=['full_ft', 'lora', 'both'], default='full_ft')
P.add_argument('--manifest', default=os.path.expanduser('~/panderm/output/m2_integral_max/manifests/m2_integral_max_v1b_local.parquet'))
P.add_argument('--out', default=os.path.expanduser('~/panderm/output/m2_integral_max/outputs/M2_v1_sam21'))
P.add_argument('--model_id', default='facebook/sam2.1-hiera-large')
P.add_argument('--init_ckpt', default='', help='state_dict to load after build (e.g. MedSAM2_latest.pt)')
P.add_argument('--init_ckpt_key', default='model', help='subkey holding the state dict')
P.add_argument('--epochs', type=int, default=30)
P.add_argument('--lr', type=float, default=1e-4)
P.add_argument('--batch_size', type=int, default=4)
P.add_argument('--grad_accum', type=int, default=4)
P.add_argument('--img_size', type=int, default=1024)
P.add_argument('--warmup', type=int, default=200)
P.add_argument('--patience', type=int, default=5)
P.add_argument('--lora_r', type=int, default=8)
P.add_argument('--lora_alpha', type=int, default=16)
P.add_argument('--lora_dropout', type=float, default=0.1)
P.add_argument('--seed', type=int, default=42)
P.add_argument('--smoke', action='store_true', help='tiny subset + 1 epoch to validate pipeline')
args = P.parse_args()

random.seed(args.seed); np.random.seed(args.seed)
torch.manual_seed(args.seed); torch.cuda.manual_seed_all(args.seed)
DEVICE = torch.device('cuda')
SAM_MEAN = np.array([0.485, 0.456, 0.406], np.float32)
SAM_STD = np.array([0.229, 0.224, 0.225], np.float32)


class ManifestSeg(Dataset):
    def __init__(self, df, img_size, train=False, smoke=False):
        if smoke:
            df = df.groupby('dataset_origin', group_keys=False).head(8)
        self.df = df.reset_index(drop=True)
        self.img_size = img_size
        self.train = train

    def __len__(self):
        return len(self.df)

    def _bbox(self, mask, jitter=20):
        ys, xs = np.where(mask > 0.5)
        if len(ys) == 0:
            return np.array([0, 0, self.img_size, self.img_size], np.float32)
        x1, y1, x2, y2 = xs.min(), ys.min(), xs.max(), ys.max()
        if self.train and jitter > 0:
            x1 = max(0, x1 - random.randint(0, jitter)); y1 = max(0, y1 - random.randint(0, jitter))
            x2 = min(self.img_size - 1, x2 + random.randint(0, jitter)); y2 = min(self.img_size - 1, y2 + random.randint(0, jitter))
        return np.array([x1, y1, x2, y2], np.float32)

    def __getitem__(self, i):
        r = self.df.iloc[i]
        img = Image.open(r.image_path).convert('RGB').resize((self.img_size, self.img_size), Image.BILINEAR)
        mask = Image.open(r.mask_path).convert('L').resize((self.img_size, self.img_size), Image.NEAREST)
        img = np.array(img, np.float32) / 255.0
        mask = (np.array(mask, np.float32) > 127.5).astype(np.float32)
        if self.train:
            if random.random() < 0.5:        # HFlip
                img = img[:, ::-1].copy(); mask = mask[:, ::-1].copy()
            if random.random() < 0.5:        # VFlip
                img = img[::-1].copy(); mask = mask[::-1].copy()
            k = random.randint(0, 3)         # Rot90 * k
            if k:
                img = np.rot90(img, k).copy(); mask = np.rot90(mask, k).copy()
            if random.random() < 0.5:        # mild ColorJitter (brightness/contrast)
                img = np.clip(img * (1 + (random.random() - 0.5) * 0.2)
                              + (random.random() - 0.5) * 0.1, 0, 1)
        img = (img - SAM_MEAN) / SAM_STD
        img_t = torch.from_numpy(img).permute(2, 0, 1).float()
        mask_t = torch.from_numpy(mask).unsqueeze(0).float()
        bbox = self._bbox(mask)
        return img_t, mask_t, bbox, r.dataset_origin, r.image_path


def dice_loss(pred, tgt, smooth=1.0):
    pred = torch.sigmoid(pred)
    pf = pred.view(pred.size(0), -1); tf = tgt.view(tgt.size(0), -1)
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
    feats = [f.permute(1, 2, 0).view(bs, -1, *fs)
             for f, fs in zip(vision_feats[::-1], feat_sizes[::-1])][::-1]
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


def build_model(mode):
    from sam2.build_sam import build_sam2_hf
    m = build_sam2_hf(args.model_id).to(DEVICE)
    if args.init_ckpt:
        ck = torch.load(args.init_ckpt, map_location=DEVICE, weights_only=False)
        sd = ck[args.init_ckpt_key] if (isinstance(ck, dict) and args.init_ckpt_key in ck) else ck
        probe = 'image_encoder.trunk.patch_embed.proj.weight'
        before = m.state_dict()[probe].detach().float().clone()
        res = m.load_state_dict(sd, strict=False)
        after = m.state_dict()[probe].detach().float()
        changed = not torch.allclose(before, after)
        matches = (probe in sd) and torch.allclose(after, sd[probe].to(DEVICE).float())
        print(f"[init_ckpt] {os.path.basename(args.init_ckpt)}: missing={len(res.missing_keys)} "
              f"unexpected={len(res.unexpected_keys)} encoder_changed={changed} encoder_matches_ckpt={matches}",
              flush=True)
        assert changed and matches, "INIT CKPT LOADER BUG: image encoder did not load the provided weights"
    for p in m.image_encoder.parameters():
        p.requires_grad = False
    for p in m.sam_prompt_encoder.parameters():
        p.requires_grad = True
    if mode == 'full_ft':
        for p in m.sam_mask_decoder.parameters():
            p.requires_grad = True
    elif mode == 'lora':
        from peft import LoraConfig, get_peft_model
        cfg = LoraConfig(r=args.lora_r, lora_alpha=args.lora_alpha, lora_dropout=args.lora_dropout,
                         target_modules=['q_proj', 'k_proj', 'v_proj', 'out_proj'], bias='none')
        m.sam_mask_decoder = get_peft_model(m.sam_mask_decoder, cfg)
    tr = sum(p.numel() for p in m.parameters() if p.requires_grad)
    tot = sum(p.numel() for p in m.parameters())
    print(f"[{mode}] trainable {tr/1e6:.3f}M / {tot/1e6:.1f}M", flush=True)
    return m, tr


@torch.no_grad()
def evaluate(model, df, img_size, by_dataset=False):
    model.eval()
    ds = ManifestSeg(df, img_size, train=False)
    dl = DataLoader(ds, batch_size=4, shuffle=False, num_workers=4, pin_memory=True)
    per_img, origins = [], []
    for imgs, masks, bboxes, dsorigin, _ in dl:
        imgs = imgs.to(DEVICE); bboxes = bboxes.to(DEVICE)
        with torch.amp.autocast('cuda', dtype=torch.bfloat16):
            logits = forward_sam2_batch(model, imgs, bboxes, img_size)
        pred = (torch.sigmoid(logits) > 0.5).float().cpu().numpy()
        gt = masks.numpy()
        for j in range(pred.shape[0]):
            per_img.append(M.all_metrics(pred[j, 0], gt[j, 0])); origins.append(dsorigin[j])
    agg = M.aggregate(per_img)
    res = {"overall": agg, "n": len(per_img)}
    if by_dataset:
        origins = np.array(origins)
        res["per_dataset"] = {o: M.aggregate([per_img[k] for k in range(len(per_img)) if origins[k] == o])
                              for o in sorted(set(origins))}
    return res


def measure_latency(model, df, img_size, n=50):
    model.eval()
    ds = ManifestSeg(df.head(n), img_size, train=False)
    dl = DataLoader(ds, batch_size=1, shuffle=False, num_workers=2)
    torch.cuda.synchronize(); ts = []
    with torch.no_grad():
        for imgs, _, bboxes, _, _ in dl:
            imgs = imgs.to(DEVICE); bboxes = bboxes.to(DEVICE)
            torch.cuda.synchronize(); t0 = time.time()
            with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                forward_sam2_batch(model, imgs, bboxes, img_size)
            torch.cuda.synchronize(); ts.append((time.time() - t0) * 1000)
    return float(np.median(ts[2:]))  # drop warmup


def save_sanity(model, df, img_size, outdir, n=5):
    os.makedirs(outdir, exist_ok=True)
    sub = df.sample(min(n, len(df)), random_state=args.seed)
    ds = ManifestSeg(sub, img_size, train=False)
    model.eval()
    for k in range(len(ds)):
        imgs, masks, bboxes, _, path = ds[k]
        with torch.no_grad(), torch.amp.autocast('cuda', dtype=torch.bfloat16):
            logits = forward_sam2_batch(model, imgs.unsqueeze(0).to(DEVICE),
                                        torch.as_tensor(bboxes, dtype=torch.float32)[None].to(DEVICE), img_size)
        pred = (torch.sigmoid(logits)[0, 0] > 0.5).cpu().numpy().astype(np.uint8) * 255
        gt = (masks[0].numpy() * 255).astype(np.uint8)
        raw = np.array(Image.open(path).convert('RGB').resize((img_size, img_size)))
        panel = np.concatenate([raw,
                                np.stack([gt] * 3, -1),
                                np.stack([pred] * 3, -1)], axis=1)
        Image.fromarray(panel).save(os.path.join(outdir, f"sanity_{k}.png"))


def train_one(mode, df, outdir):
    os.makedirs(outdir, exist_ok=True)
    model, n_tr = build_model(mode)
    tr_df = df[df.split == 'train']; va_df = df[df.split == 'val']
    tr = ManifestSeg(tr_df, args.img_size, train=True, smoke=args.smoke)
    va = ManifestSeg(va_df, args.img_size, train=False, smoke=args.smoke)
    print(f"train {len(tr)} val {len(va)}", flush=True)
    tl = DataLoader(tr, batch_size=args.batch_size, shuffle=True, num_workers=4, pin_memory=True, drop_last=True)
    vl = DataLoader(va, batch_size=args.batch_size, shuffle=False, num_workers=4, pin_memory=True)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=args.lr, weight_decay=0.01)
    epochs = 1 if args.smoke else args.epochs
    total_steps = max(1, (len(tl) // args.grad_accum) * epochs)
    warm = min(args.warmup, max(1, total_steps - 1))
    def lr_lambda(step):
        if step < warm:
            return (step + 1) / warm
        prog = (step - warm) / max(1, total_steps - warm)
        return 0.5 * (1 + np.cos(np.pi * prog))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda)

    best, best_ep, since = 0.0, 0, 0
    for ep in range(1, epochs + 1):
        model.train(); model.image_encoder.eval()
        t0 = time.time(); opt.zero_grad(); running = 0.0; nstep = 0
        for bi, (imgs, masks, bboxes, _, _) in enumerate(tl):
            imgs = imgs.to(DEVICE); masks = masks.to(DEVICE); bboxes = bboxes.to(DEVICE)
            with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                logits = forward_sam2_batch(model, imgs, bboxes, args.img_size)
                loss = combined_loss(logits, masks) / args.grad_accum
            loss.backward(); running += loss.item() * args.grad_accum
            if (bi + 1) % args.grad_accum == 0:
                torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
                opt.step(); opt.zero_grad(); sched.step(); nstep += 1
        # validate (dice only, fast)
        vr = evaluate(model, va_df if not args.smoke else va.df, args.img_size)
        vdice = vr['overall']['dice']['mean']
        print(f"ep {ep} loss {running/max(1,len(tl)):.4f} valDice {vdice:.4f} "
              f"lr {sched.get_last_lr()[0]:.2e} {time.time()-t0:.0f}s", flush=True)
        if vdice > best:
            best, best_ep, since = vdice, ep, 0
            slim = {k: v for k, v in model.state_dict().items()
                    if 'mask_decoder' in k or 'prompt_encoder' in k or 'lora' in k.lower()}
            torch.save({'epoch': ep, 'val_dice': vdice, 'mode': mode, 'state': slim},
                       os.path.join(outdir, 'best.pt'))
        else:
            since += 1
            if since >= args.patience and not args.smoke:
                print(f"early stop @ ep {ep}", flush=True); break

    # reload best
    ck = torch.load(os.path.join(outdir, 'best.pt'), map_location=DEVICE, weights_only=False)
    model.load_state_dict(ck['state'], strict=False); model.eval()
    print(f"best valDice {best:.4f} @ ep {best_ep}", flush=True)

    bucketA = df[df.split == 'test_canonical']
    bucketB = df[df.split == 'holdout_combined']
    if args.smoke:
        bucketA = bucketA.head(16)
        bucketB = bucketB.head(16)
    results = {
        'model_id': f"M2_v1_sam21_{mode}", 'mode': mode, 'trainable_params': int(n_tr),
        'best_val_dice': best, 'best_epoch': best_ep,
        'baseline_M2_v0_dice_isic2018': 0.9473,
        'bucketA_canonical_isic2018_test': evaluate(model, bucketA, args.img_size),
        'bucketB_combined_holdout': evaluate(model, bucketB, args.img_size, by_dataset=True),
        'latency_ms_1024': measure_latency(model, bucketA, args.img_size),
    }
    da = results['bucketA_canonical_isic2018_test']['overall']['dice']['mean']
    results['vs_baseline_pp'] = round((da - 0.9473) * 100, 2)
    json.dump(results, open(os.path.join(outdir, 'results.json'), 'w'), indent=2)
    save_sanity(model, bucketB, args.img_size, os.path.join(outdir, 'sanity_check'))
    print(f"=== {mode} DONE  bucketA Dice {da:.4f} (vs 0.9473 -> {results['vs_baseline_pp']:+.2f} pp) "
          f"| latency {results['latency_ms_1024']:.0f} ms ===", flush=True)
    return results


def main():
    df = pd.read_parquet(args.manifest)
    print("manifest:", len(df), df.split.value_counts().to_dict(), flush=True)
    json.dump(vars(args), open(os.path.join(args.out, 'config_f2.json'), 'w'), indent=2, default=str)
    modes = ['full_ft', 'lora'] if args.mode == 'both' else [args.mode]
    allres = {}
    for mode in modes:
        outdir = args.out if mode == 'full_ft' else args.out + '_lora'
        allres[mode] = train_one(mode, df, outdir)
    json.dump(allres, open(os.path.join(args.out, 'F2_summary.json'), 'w'), indent=2)


if __name__ == '__main__':
    os.makedirs(args.out, exist_ok=True)
    main()
