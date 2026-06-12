#!/usr/bin/env python3
"""F1c - integrate HAM10000-seg (Tschandl, 10,015 masks) into manifest v1c.
Reuses v1 hashes for the 4188 existing; hashes only the new HAM images.
Global pixel-MD5 re-dedup, immutable bucket A (1000 canonical ISIC2018 test),
re-split train/val 85/15 + bucket B holdout 5%. CPU/IO only. Keeps v1/v1b.
"""
import json, hashlib
from pathlib import Path
import numpy as np
from PIL import Image
import pandas as pd

HOME = Path.home()
BASE = HOME / "panderm" / "datasets"
MAN = HOME / "panderm" / "output" / "m2_integral_max" / "manifests"
SEED = 42
KEEP = ["image_path", "mask_path", "dataset_origin", "image_type",
        "md5_pixel_hash", "sha256_file", "mask_fg_frac"]

# --- existing 4188 (already hashed + intra-deduped in v1) ---
exist = pd.read_parquet(MAN / "m2_integral_max_v1_local.parquet")[KEEP].copy()
print("v1 existing:", len(exist), flush=True)

# --- HAM10000-seg records ---
mdir = BASE / "HAM10000_seg" / "HAM10000_segmentations_lesion_tschandl"
idir = BASE / "HAM10000_clean" / "ISIC2018"
ham, missing = [], 0
for m in sorted(mdir.glob("*_segmentation.png")):
    stem = m.name.replace("_segmentation.png", "")
    img = idir / f"{stem}.jpg"
    if not img.is_file():
        missing += 1
        continue
    ham.append(dict(image_path=str(img.resolve()), mask_path=str(m.resolve()),
                    dataset_origin="HAM10000", image_type="dermoscopic"))
print("HAM records paired:", len(ham), "missing imgs:", missing, flush=True)

for i, r in enumerate(ham):
    r["sha256_file"] = hashlib.sha256(open(r["image_path"], "rb").read()).hexdigest()
    try:
        r["md5_pixel_hash"] = hashlib.md5(np.asarray(Image.open(r["image_path"]).convert("RGB")).tobytes()).hexdigest()
    except Exception as e:
        r["md5_pixel_hash"] = "ERR"; print("imgerr", r["image_path"], e, flush=True)
    try:
        r["mask_fg_frac"] = float((np.asarray(Image.open(r["mask_path"]).convert("L")) > 127).mean())
    except Exception as e:
        r["mask_fg_frac"] = -1.0; print("maskerr", r["mask_path"], e, flush=True)
    if i % 1000 == 0:
        print("ham hashed", i, "/", len(ham), flush=True)
hamdf = pd.DataFrame(ham)[KEEP]
n_empty = int((hamdf.mask_fg_frac == 0).sum()); n_corrupt = int((hamdf.mask_fg_frac < 0).sum())
print("HAM empty masks:", n_empty, "corrupt:", n_corrupt, flush=True)

# --- combine + global dedup by pixel hash ---
alldf = pd.concat([exist, hamdf], ignore_index=True)
print("combined raw:", len(alldf), alldf.dataset_origin.value_counts().to_dict(), flush=True)
prio = {"ISIC2018": 0, "ISIC2017": 1, "PH2": 2, "HAM10000": 3}
alldf["_p"] = alldf.dataset_origin.map(prio)
alldf = alldf.sort_values(["md5_pixel_hash", "_p", "image_path"]).reset_index(drop=True)
dup = alldf.duplicated("md5_pixel_hash", keep="first")
coll, inter, intra, ham_inter = [], 0, 0, 0
for h, g in alldf[alldf.md5_pixel_hash.isin(set(alldf.loc[dup, "md5_pixel_hash"]))].groupby("md5_pixel_hash"):
    dropped = [dict(path=r.image_path, dataset=r.dataset_origin) for _, r in g.iloc[1:].iterrows()]
    coll.append(dict(pixel_hash=h, kept=g.iloc[0].image_path, kept_dataset=g.iloc[0].dataset_origin, dropped=dropped))
    dss = {g.iloc[0].dataset_origin} | {d["dataset"] for d in dropped}
    if len(dss) > 1:
        inter += len(dropped)
        if "HAM10000" in dss:
            ham_inter += len(dropped)
    else:
        intra += len(dropped)
n_drop = int(dup.sum())
allu = alldf[~dup].drop(columns=["_p"]).reset_index(drop=True)
print("dedup dropped:", n_drop, "inter:", inter, "intra:", intra, "HAM-involved-inter:", ham_inter,
      "unique:", len(allu), flush=True)

# --- bucket A immutable (1000 canonical ISIC2018 test) ---
is_canon = allu.image_path.str.contains("/ISIC2018/Test_Data/")
A = allu[is_canon].copy(); rest = allu[~is_canon].copy().reset_index(drop=True)
assert len(A) == 1000, f"bucket A != 1000 ({len(A)})"

# --- bucket B 5% stratified ---
N_B = int(round(len(rest) * 0.05))
rng = np.random.default_rng(SEED); Bidx = []
for ds in sorted(rest.dataset_origin.unique()):
    idx = rest.index[rest.dataset_origin == ds].to_numpy()
    idx = idx[rng.permutation(len(idx))]
    Bidx.extend(idx[:int(round(N_B * len(idx) / len(rest)))].tolist())
Bidx = Bidx[:N_B]
B = rest.loc[Bidx].copy(); tv = rest.drop(index=Bidx).copy().reset_index(drop=True)

# --- train/val 85/15 stratified ---
tv["split"] = None
for ds in sorted(tv.dataset_origin.unique()):
    idx = tv.index[tv.dataset_origin == ds].to_numpy()
    idx = idx[np.random.default_rng(SEED).permutation(len(idx))]
    ntr = int(round(len(idx) * 0.85))
    tv.loc[idx[:ntr], "split"] = "train"; tv.loc[idx[ntr:], "split"] = "val"
A["split"] = "test_canonical"; B["split"] = "holdout_combined"
out = pd.concat([tv, B, A], ignore_index=True)
out["fitzpatrick_type"] = np.nan
out = out.sort_values(["dataset_origin", "split", "image_path"]).reset_index(drop=True)

# --- sanity ---
assert out.md5_pixel_hash.duplicated().sum() == 0
assert int(out.groupby("md5_pixel_hash").split.nunique().max()) == 1
assert not out[out.split.isin(["train", "val"])].image_path.str.contains("/ISIC2018/Test_Data/").any()

def lock(s):
    return hashlib.sha256("".join(sorted(s.md5_pixel_hash)).encode()).hexdigest()
lockA = lock(out[out.split == "test_canonical"]); lockB = lock(out[out.split == "holdout_combined"])
v1b_lockA = json.load(open(MAN / "test_canonico_isic2018_v1b.json"))["sha256_lock"]
assert lockA == v1b_lockA, f"bucket A CHANGED vs v1b!  {lockA} != {v1b_lockA}"
print("bucket A immutable vs v1b: OK", flush=True)

# --- write ---
cols = ["image_path", "mask_path", "dataset_origin", "split", "image_type",
        "fitzpatrick_type", "md5_pixel_hash", "sha256_file", "mask_fg_frac"]
out = out[cols]
pq = MAN / "m2_integral_max_v1c_local.parquet"
out.to_parquet(pq, index=False)
man_md5 = hashlib.md5(open(pq, "rb").read()).hexdigest()

splits_summary = {ds: {sp: int(((out.dataset_origin == ds) & (out.split == sp)).sum())
                       for sp in ["train", "val", "holdout_combined", "test_canonical"]}
                  for ds in sorted(out.dataset_origin.unique())}
json.dump(coll, open(MAN / "md5_collisions_v1c.json", "w"), indent=2)
json.dump(splits_summary, open(MAN / "splits_v1c.json", "w"), indent=2)
json.dump(dict(n=1000, sha256_lock=lockA, immutable_vs_v1b=True,
               desc="canonical ISIC2018 Task1 Test_Data, baseline-comparable vs 0.9473"),
          open(MAN / "test_canonico_isic2018_v1c.json", "w"), indent=2)
json.dump(dict(n=int((out.split == "holdout_combined").sum()), sha256_lock=lockB,
               per_dataset={ds: int(((out.split == "holdout_combined") & (out.dataset_origin == ds)).sum())
                            for ds in sorted(out.dataset_origin.unique())}),
          open(MAN / "test_holdout_combined_v1c.json", "w"), indent=2)
json.dump(dict(n_total=len(out), per_dataset=out.dataset_origin.value_counts().to_dict(),
               per_split=out.split.value_counts().to_dict(), splits_summary=splits_summary,
               dedup=dict(dropped=n_drop, inter=inter, intra=intra, ham_involved_inter=ham_inter),
               ham_empty_masks=n_empty, ham_corrupt_masks=n_corrupt,
               manifest_md5=man_md5),
          open(MAN / "dataset_stats_v1c.json", "w"), indent=2)

print("=== v1c SUMMARY ===")
print("unique_total:", len(out))
print("per_dataset:", out.dataset_origin.value_counts().to_dict())
print("per_split:", out.split.value_counts().to_dict())
print("splits_summary:", json.dumps(splits_summary))
print("dedup_dropped:", n_drop, "inter:", inter, "intra:", intra, "HAM_inter:", ham_inter)
print("bucketA_lock:", lockA[:16], "(== v1b)")
print("bucketB_n:", int((out.split == "holdout_combined").sum()), "lock:", lockB[:16])
print("manifest:", str(pq), "md5:", man_md5)
