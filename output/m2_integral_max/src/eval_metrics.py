#!/usr/bin/env python3
"""Segmentation metrics for M2-INTEGRAL-MAX. Universal across F2-F8.
Per-image: Dice, IoU, F1, Precision, Recall, HD95 (scipy, no extra deps).
HD95 = 95th percentile of symmetric surface distances between predicted and
GT boundaries, in pixels at the evaluation resolution (1024x1024).
Reproducible (charter rule 10): pure numpy/scipy, documented below.
"""
import numpy as np
from scipy.ndimage import distance_transform_edt, binary_erosion

EPS = 1e-6


def _bin(x):
    return (np.asarray(x) > 0.5).astype(np.uint8)


def dice_iou(pred, gt):
    p = _bin(pred).reshape(-1); g = _bin(gt).reshape(-1)
    inter = float((p * g).sum()); s = float(p.sum() + g.sum())
    dice = (2 * inter + EPS) / (s + EPS)
    iou = (inter + EPS) / (s - inter + EPS)
    return dice, iou


def prf(pred, gt):
    p = _bin(pred).reshape(-1); g = _bin(gt).reshape(-1)
    tp = float((p * g).sum()); fp = float((p * (1 - g)).sum()); fn = float(((1 - p) * g).sum())
    prec = (tp + EPS) / (tp + fp + EPS)
    rec = (tp + EPS) / (tp + fn + EPS)
    f1 = (2 * prec * rec) / (prec + rec + EPS)
    return prec, rec, f1


def hd95(pred, gt):
    """95th-percentile symmetric boundary (Hausdorff) distance in pixels."""
    p = _bin(pred); g = _bin(gt)
    diag = float(np.hypot(*p.shape))
    if p.sum() == 0 and g.sum() == 0:
        return 0.0
    if p.sum() == 0 or g.sum() == 0:
        return diag  # one mask empty -> worst-case distance
    pb = (p & ~binary_erosion(p)).astype(bool)
    gb = (g & ~binary_erosion(g)).astype(bool)
    dt_to_g = distance_transform_edt(1 - g)   # dist of any pixel to nearest GT fg
    dt_to_p = distance_transform_edt(1 - p)
    d_pg = dt_to_g[pb]   # pred boundary -> GT
    d_gp = dt_to_p[gb]   # GT boundary -> pred
    if d_pg.size == 0 or d_gp.size == 0:
        return diag
    return float(np.percentile(np.concatenate([d_pg, d_gp]), 95))


def all_metrics(pred, gt):
    d, i = dice_iou(pred, gt)
    pr, rc, f1 = prf(pred, gt)
    return {"dice": d, "iou": i, "f1": f1, "precision": pr,
            "recall": rc, "hd95": hd95(pred, gt)}


def aggregate(metric_dicts):
    if not metric_dicts:
        return {}
    keys = metric_dicts[0].keys()
    out = {}
    for k in keys:
        v = np.array([m[k] for m in metric_dicts], dtype=np.float64)
        out[k] = {"mean": float(v.mean()), "std": float(v.std()), "n": int(v.size)}
    return out
