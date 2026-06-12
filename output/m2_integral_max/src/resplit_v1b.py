#!/usr/bin/env python3
"""F1.5 re-split v1b - preserve canonical ISIC2018 test for baseline comparability.
Reads v1 manifest (no re-hash). Keeps v1 intact. CPU/IO only.

Buckets:
  A = test_canonical : the 1000 canonical ISIC2018 Test_Data images (NEVER train/val)
  B = holdout_combined : 210 stratified from the REST (excl. bucket A)
  train/val = 85/15 stratified by dataset_origin (seed 42) over remaining
"""
import json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

MAN = Path.home() / "panderm" / "output" / "m2_integral_max" / "manifests"
SEED = 42
df = pd.read_parquet(MAN / "m2_integral_max_v1_local.parquet").reset_index(drop=True)
assert len(df) == 4188, len(df)

# --- Bucket A: canonical ISIC2018 test (path-based, the official Test_Data) ---
is_canon = df.image_path.str.contains("/ISIC2018/Test_Data/")
A = df[is_canon].copy()
rest = df[~is_canon].copy().reset_index(drop=True)
print("bucket A (ISIC2018 canonical test):", len(A))
print("rest:", len(rest), rest.dataset_origin.value_counts().to_dict())

# --- Bucket B: 210 stratified from rest by dataset_origin (proportional) ---
N_B = 210
B_idx = []
rng = np.random.default_rng(SEED)
counts = rest.dataset_origin.value_counts()
for ds in sorted(rest.dataset_origin.unique()):
    idx = rest.index[rest.dataset_origin == ds].to_numpy()
    idx = idx[rng.permutation(len(idx))]
    n_take = int(round(N_B * len(idx) / len(rest)))
    B_idx.extend(idx[:n_take].tolist())
B_idx = B_idx[:N_B]
B = rest.loc[B_idx].copy()
trainval = rest.drop(index=B_idx).copy().reset_index(drop=True)
print("bucket B (holdout combined):", len(B), B.dataset_origin.value_counts().to_dict())

# --- train/val 85/15 stratified by dataset_origin (seed 42) over trainval ---
trainval["split"] = None
for ds in sorted(trainval.dataset_origin.unique()):
    idx = trainval.index[trainval.dataset_origin == ds].to_numpy()
    idx = idx[np.random.default_rng(SEED).permutation(len(idx))]
    ntr = int(round(len(idx) * 0.85))
    trainval.loc[idx[:ntr], "split"] = "train"
    trainval.loc[idx[ntr:], "split"] = "val"

A["split"] = "test_canonical"
B["split"] = "holdout_combined"
out = pd.concat([trainval, B, A], ignore_index=True)
out = out.sort_values(["dataset_origin", "split", "image_path"]).reset_index(drop=True)

# --- sanity ---
assert out.md5_pixel_hash.duplicated().sum() == 0
assert int(out.groupby("md5_pixel_hash").split.nunique().max()) == 1, "leakage across splits"
assert len(out) == 4188
# bucket A never in train/val
assert not out[out.split.isin(["train", "val"])].image_path.str.contains("/ISIC2018/Test_Data/").any()

# --- locks ---
def lock(sub):
    return hashlib.sha256("".join(sorted(sub.md5_pixel_hash)).encode()).hexdigest()
lockA = lock(out[out.split == "test_canonical"])
lockB = lock(out[out.split == "holdout_combined"])

pq = MAN / "m2_integral_max_v1b_local.parquet"
out.to_parquet(pq, index=False)
man_md5 = hashlib.md5(open(pq, "rb").read()).hexdigest()

splits_summary = {ds: {sp: int(((out.dataset_origin == ds) & (out.split == sp)).sum())
                       for sp in ["train", "val", "holdout_combined", "test_canonical"]}
                  for ds in sorted(out.dataset_origin.unique())}
json.dump(splits_summary, open(MAN / "splits_v1b.json", "w"), indent=2)
json.dump(dict(n=int((out.split == "test_canonical").sum()), sha256_lock=lockA,
               desc="canonical ISIC2018 Task1 Test_Data, baseline-comparable (vs 0.9473)"),
          open(MAN / "test_canonico_isic2018_v1b.json", "w"), indent=2)
json.dump(dict(n=int((out.split == "holdout_combined").sum()), sha256_lock=lockB,
               per_dataset={ds: int(((out.split == "holdout_combined") & (out.dataset_origin == ds)).sum())
                            for ds in sorted(out.dataset_origin.unique())}),
          open(MAN / "test_holdout_combined_v1b.json", "w"), indent=2)

print("=== v1b SUMMARY ===")
print("total:", len(out))
print("per_split:", out.split.value_counts().to_dict())
print("splits_summary:", json.dumps(splits_summary))
print("bucketA_n:", int((out.split == "test_canonical").sum()), "lock:", lockA[:16])
print("bucketB_n:", int((out.split == "holdout_combined").sum()), "lock:", lockB[:16])
print("manifest:", str(pq), "md5:", man_md5)
