import pandas as pd
import numpy as np

IN_CSV  = r"E:/PhD Milestones/Comprehensive/ReplicationPackage/Data-N-Scripts/RQ4/Outputs/evaluation-metric-jaccard-similarity.csv"
OUT_CSV = r"E:/PhD Milestones/Comprehensive/ReplicationPackage/Data-N-Scripts/RQ4/Outputs/highly-cooccurred-evaluation-metrics-jaccard.csv"

# -----------------------------
# Parameters (adjust as needed)
# -----------------------------
JACCARD_THRESHOLD = 0.5   # strong co-occurrence
TOP_K = 20             # set to e.g., 20 to keep only top-20 pairs

# -----------------------------
# Load Jaccard matrix
# -----------------------------
jac_df = pd.read_csv(IN_CSV, index_col=0)

metrics = jac_df.columns.tolist()
pairs = []

# -----------------------------
# Extract metric pairs
# -----------------------------
for i in range(len(metrics)):
    for j in range(i + 1, len(metrics)):  # upper triangle only
        m1 = metrics[i]
        m2 = metrics[j]
        val = jac_df.iloc[i, j]

        if pd.isna(val):
            continue
        if val >= JACCARD_THRESHOLD:
            pairs.append({
                "Metric_1": m1,
                "Metric_2": m2,
                "Jaccard": round(val, 3)
            })

# Convert to DataFrame
out_df = pd.DataFrame(pairs)

# Sort by Jaccard value (descending)
out_df = out_df.sort_values("Jaccard", ascending=False)

# Optional: keep only top-K
if TOP_K is not None:
    out_df = out_df.head(TOP_K)

# Save
out_df.to_csv(OUT_CSV, index=False, encoding="utf-8")

print(f"Saved highly co-occurred metric pairs to:\n{OUT_CSV}")
