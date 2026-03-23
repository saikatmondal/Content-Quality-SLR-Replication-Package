import pandas as pd

IN_CSV  = r".../RQ4/Outputs/evaluation-metric-cooccurrence-count.csv"
OUT_CSV = r".../RQ4/Outputs/highly-cooccurred-evaluation-metrics-by-count.csv"

# -----------------------------
# Parameters (tune as needed)
# -----------------------------
COUNT_THRESHOLD = 1  # e.g., appear together in ≥10 studies
TOP_K = 20           # set to e.g., 20 to keep only top-20 pairs

# -----------------------------
# Load count matrix
# -----------------------------
co_df = pd.read_csv(IN_CSV, index_col=0)

metrics = co_df.columns.tolist()
pairs = []

# -----------------------------
# Extract metric pairs
# -----------------------------
for i in range(len(metrics)):
    for j in range(i + 1, len(metrics)):  # upper triangle only
        m1 = metrics[i]
        m2 = metrics[j]
        count = co_df.iloc[i, j]

        if pd.isna(count):
            continue
        if int(count) >= COUNT_THRESHOLD:
            pairs.append({
                "Metric_1": m1,
                "Metric_2": m2,
                "CooccurrenceCount": int(count)
            })

# Convert to DataFrame
out_df = pd.DataFrame(pairs)

# Sort by count (descending)
out_df = out_df.sort_values("CooccurrenceCount", ascending=False)

# Optional: keep only top-K
if TOP_K is not None:
    out_df = out_df.head(TOP_K)

# Save
out_df.to_csv(OUT_CSV, index=False, encoding="utf-8")

print(f"Saved highly co-occurred metric pairs (count-based) to:\n{OUT_CSV}")
