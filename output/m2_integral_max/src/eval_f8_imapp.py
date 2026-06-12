#!/usr/bin/env python3
"""F8 - Multi-annotator CALIBRATION of MedSAM2-tiny against IMA++ (subset of bucket A).

IMA++ provides several human annotator masks per ISIC image. For the bucket-A
images that have >=2 annotators, we ask: does the (box-prompted) MedSAM2-tiny
agree with the human consensus as well as humans agree with each other, and is
the model's pixel probability calibrated to human disagreement?

Per image: model prob (box = v1c GT box, == interactive mode) vs:
  - soft human label = mean of annotator binary masks (per-pixel agreement)
  - MV consensus (soft >= 0.5)
Metrics: human IAA (mean pairwise annotator Dice), model Dice vs MV & vs v1c GT,
ECE & Brier of model prob vs soft human label, and "within-human-envelope" rate
(model-vs-MV Dice >= min pairwise human Dice).
Eval-only. Base model = F3 M2_v2_medsam2/best.pt.
"""
import os, sys, glob, re, json, argparse, collections
import numpy as np, torch, torch.nn.functional as F
from PIL import Image
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_metrics as MET

P = argparse.ArgumentParser()
P.add_argument('--manifest', default=os.path.expanduser('~/panderm/output/m2_integral_max/manifests/m2_integral_max_v1c_local.parquet'))
P.add_argument('--best_pt', default=os.path.expanduser('~/panderm/output/m2_integral_max/outputs/M2_v2_medsam2/best.pt'))
P.add_argument('--ima_masks', default=os.path.expanduser('~/panderm/datasets/IMAplusplus/masks'))
P.add_argument('--model_id', default='facebook/sam2.1-hiera-tiny')
P.add_argument('--init_ckpt', default='/home/husll-spark-01/.cache/huggingface/hub/models--wanglab--MedSAM2/snapshots/e4a6f35edd7e091619cbc0750f462f1574e23955/MedSAM2_latest.pt')
P.add_argument('--out', default=os.path.expanduser('~/panderm/output/m2_integral_max/outputs/M2_v9_f8_imapp'))
P.add_argument('--img_size', type=int, default=1024)
P.add_argument('--min_annot', type=int, default=2)
P.add_argument('--smoke', action='store_true')
args = P.parse_args()
DEVICE = torch.device('cuda')
IMNET_MEAN = np.array([0.485, 0.456, 0.406], np.float32); IMNET_STD = np.array([0.229, 0.224, 0.225], np.float32)
S = args.img_size


def forward_one(model, img, box):
    bb = model.forward_image(img)
    _, vf, _, fs = model._prepare_backbone_features(bb)
    if model.directly_add_no_mem_embed: vf[-1] = vf[-1] + model.no_mem_embed
    feats = [f.permute(1, 2, 0).view(1, -1, *s) for f, s in zip(vf[::-1], fs[::-1])][::-1]
    se, de = model.sam_prompt_encoder(points=None, boxes=box, masks=None)
    low, _, _, _ = model.sam_mask_decoder(image_embeddings=feats[-1], image_pe=model.sam_prompt_encoder.get_dense_pe(),
                                          sparse_prompt_embeddings=se, dense_prompt_embeddings=de,
                                          multimask_output=False, repeat_image=False, high_res_features=feats[:-1])
    return torch.sigmoid(F.interpolate(low, (S, S), mode='bilinear', align_corners=False).float())[0, 0].cpu().numpy()


def build():
    from sam2.build_sam import build_sam2_hf
    m = build_sam2_hf(args.model_id).to(DEVICE)
    ck = torch.load(args.init_ckpt, map_location=DEVICE, weights_only=False)
    m.load_state_dict(ck['model'] if (isinstance(ck, dict) and 'model' in ck) else ck, strict=False)
    best = torch.load(args.best_pt, map_location=DEVICE, weights_only=False)
    m.load_state_dict(best['state'], strict=False); m.eval()
    return m


def load_bin(path):
    return (np.array(Image.open(path).convert('L').resize((S, S), Image.NEAREST), np.float32) > 127.5).astype(np.float32)


def dice(a, b):
    i = float((a * b).sum()); s = float(a.sum() + b.sum())
    return (2 * i + 1e-6) / (s + 1e-6)


def main():
    os.makedirs(args.out, exist_ok=True)
    df = pd.read_parquet(args.manifest)
    A = df[df.split == 'test_canonical'].reset_index(drop=True)
    # map ISIC id -> annotator mask files (exclude MV/ST consensus)
    pat = re.compile(r'(ISIC_\d+)_([A-Z0-9]+)_')
    byid = collections.defaultdict(dict)
    for f in glob.glob(os.path.join(args.ima_masks, '*.png')):
        mt = pat.match(os.path.basename(f))
        if not mt: continue
        iid, code = mt.group(1), mt.group(2)
        if code in ('MV', 'ST'): continue
        byid[iid].setdefault(code, f)  # one file per annotator code
    items = []
    for _, r in A.iterrows():
        iid = os.path.basename(r.image_path).split('.')[0].replace('_segmentation', '')
        ann = byid.get(iid, {})
        if len(ann) >= args.min_annot:
            items.append((r.image_path, r.mask_path, sorted(ann.values())))
    if args.smoke: items = items[:12]
    print(f"bucketA multi-annotator subset: {len(items)} imgs (>= {args.min_annot} annotators)", flush=True)
    model = build()

    NB = 15; conf = np.zeros(NB); acc = np.zeros(NB); cnt = np.zeros(NB)
    rec = []
    for k, (imgp, gtp, annfs) in enumerate(items):
        raw = np.array(Image.open(imgp).convert('RGB').resize((S, S), Image.BILINEAR), np.float32)
        gt = load_bin(gtp)  # v1c official GT
        ys, xs = np.where(gt > 0.5)
        box = np.array([0, 0, S, S], np.float32) if len(ys) == 0 else np.array([xs.min(), ys.min(), xs.max(), ys.max()], np.float32)
        img = torch.from_numpy((raw / 255. - IMNET_MEAN) / IMNET_STD).permute(2, 0, 1)[None].float().to(DEVICE)
        with torch.no_grad(), torch.amp.autocast('cuda', dtype=torch.bfloat16):
            prob = forward_one(model, img, torch.from_numpy(box)[None].float().to(DEVICE))
        hum = [load_bin(f) for f in annfs]
        soft = np.mean(hum, axis=0)            # per-pixel human agreement [0,1]
        mv = (soft >= 0.5).astype(np.float32)  # majority vote
        pred = (prob > 0.5).astype(np.float32)
        # human IAA: mean pairwise Dice
        pw = [dice(hum[a], hum[b]) for a in range(len(hum)) for b in range(a + 1, len(hum))]
        iaa_mean = float(np.mean(pw)); iaa_min = float(np.min(pw))
        d_mv = dice(pred, mv); d_gt = dice(pred, gt)
        # calibration of model prob vs soft human label (subsampled grid)
        ps = prob[::4, ::4].ravel(); ss = soft[::4, ::4].ravel()
        brier = float(np.mean((ps - ss) ** 2))
        bins = np.clip((ps * NB).astype(int), 0, NB - 1)
        for b in range(NB):
            mb = bins == b
            if mb.any(): conf[b] += ps[mb].sum(); acc[b] += ss[mb].sum(); cnt[b] += mb.sum()
        rec.append({'n_annot': len(hum), 'iaa_mean': iaa_mean, 'iaa_min': iaa_min,
                    'model_dice_vs_mv': d_mv, 'model_dice_vs_gt': d_gt, 'brier_vs_soft': brier,
                    'within_envelope': bool(d_mv >= iaa_min)})
        if (k + 1) % 50 == 0: print(f"  {k+1}/{len(items)}", flush=True)

    ece = float(np.sum(cnt / cnt.sum() * np.abs(acc / np.maximum(cnt, 1) - conf / np.maximum(cnt, 1))))
    arr = lambda key: np.array([r[key] for r in rec], float)
    out = {'model': 'MedSAM2-tiny', 'n_images': len(rec), 'mean_annotators': float(arr('n_annot').mean()),
           'human_IAA_mean_pairwise_dice': float(arr('iaa_mean').mean()),
           'model_dice_vs_MV_consensus': float(arr('model_dice_vs_mv').mean()),
           'model_dice_vs_v1c_GT': float(arr('model_dice_vs_gt').mean()),
           'calibration_vs_soft_human': {'ece_15bin': ece, 'brier_mean': float(arr('brier_vs_soft').mean())},
           'within_human_envelope_rate': float(arr('within_envelope').mean()),
           'reliability_bins': {'conf': (conf / np.maximum(cnt, 1)).tolist(), 'acc': (acc / np.maximum(cnt, 1)).tolist(), 'cnt': cnt.tolist()}}
    json.dump(out, open(os.path.join(args.out, 'imapp_calibration.json'), 'w'), indent=2)
    print(f"\n=== IMA++ CALIBRATION DONE ({out['n_images']} imgs, {out['mean_annotators']:.1f} annot/img) ===", flush=True)
    print(f"  human IAA (pairwise Dice)     {out['human_IAA_mean_pairwise_dice']:.4f}", flush=True)
    print(f"  model Dice vs MV consensus    {out['model_dice_vs_MV_consensus']:.4f}", flush=True)
    print(f"  model Dice vs v1c GT          {out['model_dice_vs_v1c_GT']:.4f}", flush=True)
    print(f"  ECE vs soft human label       {ece:.4f}  Brier {out['calibration_vs_soft_human']['brier_mean']:.4f}", flush=True)
    print(f"  within human envelope rate    {out['within_human_envelope_rate']:.3f}", flush=True)


if __name__ == '__main__':
    main()
