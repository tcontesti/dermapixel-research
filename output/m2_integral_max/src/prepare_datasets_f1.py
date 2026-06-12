#!/usr/bin/env python3
"""F1 dataset preparation - M2-INTEGRAL-MAX (local-only v1).
Builds a deduplicated, stratified manifest over ISIC2017 + ISIC2018 + PH2.
CPU/IO only - no GPU. Read-only over source datasets; writes only to workspace.
"""
import os, csv, json, hashlib, sys
from pathlib import Path
import numpy as np
from PIL import Image
import pandas as pd

HOME = Path.home()
BASE = HOME / "panderm" / "datasets"
WS = HOME / "panderm" / "output" / "m2_integral_max"
MAN = WS / "manifests"
MAN.mkdir(parents=True, exist_ok=True)
SEED = 42

records = []

# --- ISIC2017 (from seg csv: relative image/mask/split) ---
d17 = BASE / "ISIC2017"
with open(d17 / "isic2017_seg.csv") as f:
    for row in csv.DictReader(f):
        records.append(dict(
            image_path=str((d17 / row["image"]).resolve()),
            mask_path=str((d17 / row["mask"]).resolve()),
            dataset_origin="ISIC2017", orig_split=row["split"],
            image_type="dermoscopic"))

# --- ISIC2018 (folder pairing) ---
d18 = BASE / "ISIC2018"
for split, dd, gg in [("train", "Training_Data", "Training_GroundTruth"),
                      ("val", "Validation_Data", "Validation_GroundTruth"),
                      ("test", "Test_Data", "Test_GroundTruth")]:
    for img in sorted((d18 / dd).glob("*.jpg")):
        m = d18 / gg / f"{img.stem}_segmentation.png"
        records.append(dict(
            image_path=str(img.resolve()), mask_path=str(m.resolve()),
            dataset_origin="ISIC2018", orig_split=split,
            image_type="dermoscopic"))

# --- PH2 (from seg csv) ---
dph = BASE / "PH2"
with open(dph / "ph2_seg.csv") as f:
    for row in csv.DictReader(f):
        records.append(dict(
            image_path=str((dph / row["image"]).resolve()),
            mask_path=str((dph / row["mask"]).resolve()),
            dataset_origin="PH2", orig_split=row["split"],
            image_type="dermoscopic"))

df = pd.DataFrame(records)
print("raw records:", len(df), df.dataset_origin.value_counts().to_dict(), flush=True)

# --- existence check ---
df["img_ok"] = df.image_path.map(os.path.isfile)
df["mask_ok"] = df.mask_path.map(os.path.isfile)
missing = df[~(df.img_ok & df.mask_ok)]
print("missing pairs:", len(missing), flush=True)
if len(missing):
    print(missing[["dataset_origin", "image_path", "img_ok", "mask_ok"]].head(20).to_string(), flush=True)
df = df[df.img_ok & df.mask_ok].drop(columns=["img_ok", "mask_ok"]).reset_index(drop=True)

# --- hashes (file sha256 + pixel md5) + mask foreground fraction ---
shas, pxs, mfg = [], [], []
for i, (ip, mp) in enumerate(zip(df.image_path, df.mask_path)):
    b = open(ip, "rb").read()
    shas.append(hashlib.sha256(b).hexdigest())
    try:
        px = hashlib.md5(np.asarray(Image.open(ip).convert("RGB")).tobytes()).hexdigest()
    except Exception as e:
        px = "ERR"; print("img decode err", ip, e, flush=True)
    pxs.append(px)
    try:
        mk = np.asarray(Image.open(mp).convert("L"))
        mfg.append(float((mk > 127).mean()))
    except Exception as e:
        mfg.append(-1.0); print("mask decode err", mp, e, flush=True)
    if i % 1000 == 0:
        print("hashed", i, "/", len(df), flush=True)
df["sha256_file"] = shas
df["md5_pixel_hash"] = pxs
df["mask_fg_frac"] = mfg

n_empty = int((df.mask_fg_frac == 0).sum())
n_corrupt = int((df.mask_fg_frac < 0).sum())
print("empty masks:", n_empty, "corrupt masks:", n_corrupt, flush=True)

# --- dedup by pixel hash (keep priority ISIC2018>ISIC2017>PH2, train>val>test) ---
prio = {"ISIC2018": 0, "ISIC2017": 1, "PH2": 2}
sprio = {"train": 0, "val": 1, "test": 2}
df["_p"] = df.dataset_origin.map(prio) + df.orig_split.map(lambda s: sprio.get(s, 3)) * 0.1
df = df.sort_values(["md5_pixel_hash", "_p", "image_path"]).reset_index(drop=True)
dup = df.duplicated("md5_pixel_hash", keep="first")

collisions, inter, intra = [], 0, 0
dup_hashes = set(df.loc[dup, "md5_pixel_hash"])
for h, g in df[df.md5_pixel_hash.isin(dup_hashes)].groupby("md5_pixel_hash"):
    dropped = [dict(path=r.image_path, dataset=r.dataset_origin, orig_split=r.orig_split)
               for _, r in g.iloc[1:].iterrows()]
    collisions.append(dict(pixel_hash=h, kept=g.iloc[0].image_path,
                           kept_dataset=g.iloc[0].dataset_origin, dropped=dropped))
    datasets = {g.iloc[0].dataset_origin} | {d["dataset"] for d in dropped}
    if len(datasets) > 1:
        inter += len(dropped)
    else:
        intra += len(dropped)
n_drop = int(dup.sum())
df = df[~dup].drop(columns=["_p"]).reset_index(drop=True)
print("dedup dropped:", n_drop, "(inter", inter, "intra", intra, ") unique:", len(df), flush=True)

# --- stratified 85/10/5 split by dataset_origin, seed 42 ---
df["split"] = None
for ds, idx in df.groupby("dataset_origin").groups.items():
    idx = np.array(list(idx))
    idx = idx[np.random.default_rng(SEED).permutation(len(idx))]
    n = len(idx); ntr = int(round(n * 0.85)); nval = int(round(n * 0.10))
    df.loc[idx[:ntr], "split"] = "train"
    df.loc[idx[ntr:ntr + nval], "split"] = "val"
    df.loc[idx[ntr + nval:], "split"] = "test"
df["fitzpatrick_type"] = np.nan

# --- holdout == test split (blinded), SHA-256 lock ---
holdout = df[df.split == "test"]
hlock = hashlib.sha256("".join(sorted(holdout.md5_pixel_hash)).encode()).hexdigest()

# --- sanity ---
assert df.md5_pixel_hash.duplicated().sum() == 0, "DUP md5 after dedup"
max_splits = int(df.groupby("md5_pixel_hash").split.nunique().max())
assert max_splits == 1, f"pixelhash spans {max_splits} splits (leakage)"
assert df.mask_path.map(os.path.isfile).all(), "missing mask after dedup"

# --- write outputs ---
cols = ["image_path", "mask_path", "dataset_origin", "split", "image_type",
        "fitzpatrick_type", "md5_pixel_hash", "sha256_file", "mask_fg_frac"]
out = df[cols].sort_values(["dataset_origin", "split", "image_path"]).reset_index(drop=True)
pq = MAN / "m2_integral_max_v1_local.parquet"
out.to_parquet(pq, index=False)
man_md5 = hashlib.md5(open(pq, "rb").read()).hexdigest()

splits_summary = {ds: {sp: int(((out.dataset_origin == ds) & (out.split == sp)).sum())
                       for sp in ["train", "val", "test"]} for ds in sorted(out.dataset_origin.unique())}
json.dump(collisions, open(MAN / "md5_collisions.json", "w"), indent=2)
json.dump(splits_summary, open(MAN / "splits_v1.json", "w"), indent=2)
json.dump(dict(n_holdout=int(len(holdout)), sha256_lock=hlock,
               per_dataset={ds: int((holdout.dataset_origin == ds).sum())
                            for ds in sorted(holdout.dataset_origin.unique())}),
          open(MAN / "test_holdout_combined_v1.json", "w"), indent=2)

print("=== F1 SUMMARY ===", flush=True)
print("unique_total:", len(out))
print("per_split:", out.split.value_counts().to_dict())
print("per_dataset:", out.dataset_origin.value_counts().to_dict())
print("splits_summary:", json.dumps(splits_summary))
print("dedup_dropped:", n_drop, "inter:", inter, "intra:", intra)
print("empty_masks:", n_empty, "corrupt_masks:", n_corrupt)
print("holdout_n:", len(holdout), "sha256_lock:", hlock)
print("manifest:", str(pq))
print("manifest_md5:", man_md5)
