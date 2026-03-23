import pandas as pd
from collections import Counter

# -----------------------------
# Paths
# -----------------------------
IN_CSV  = r".../study-wise-evaluation-metrics.csv"
OUT_CSV = r".../study-wise-evaluation-metrics-with-count.csv"

TOTAL_STUDIES = 127

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(IN_CSV, encoding="utf-8")

if "Study#" not in df.columns or "EvaluationMetrics" not in df.columns:
    raise ValueError("CSV must contain 'Study#' and 'EvaluationMetrics' columns")

# -----------------------------
# Count metrics per study
# -----------------------------
metric_counts = []

for _, row in df.iterrows():
    metrics = row.get("EvaluationMetrics", "")

    if isinstance(metrics, str) and metrics.strip():
        count = len([m for m in metrics.split(";") if m.strip()])
    else:
        count = 0

    metric_counts.append(count)

# Append new column
df["MetricCount"] = metric_counts

# -----------------------------
# Distribution summary
# -----------------------------
dist = Counter(metric_counts)

print("Evaluation Metric Usage per Study\n")
for k in sorted(dist):
    freq = dist[k]
    percent = (freq / TOTAL_STUDIES) * 100
    print(f"{k}-metric: {freq} ({percent:.1f}%)")

# -----------------------------
# Save CSV (append-only change)
# -----------------------------
df.to_csv(OUT_CSV, index=False, encoding="utf-8")

print(f"\nSaved CSV with metric counts to:\n{OUT_CSV}")
