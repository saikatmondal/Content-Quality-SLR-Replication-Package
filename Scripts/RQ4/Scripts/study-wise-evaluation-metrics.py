import pandas as pd
import re
from collections import defaultdict

# ---- Paths (edit if needed) ----
IN_CSV  = r".../RQ4/Outputs/RQ4-Evaluation-Group-Aggregated.csv"
OUT_CSV = r".../RQ4/Outputs/study-wise-evaluation-metrics.csv"

# If you run on Windows, you can use your own paths, e.g.:
# IN_CSV  = r"E:/.../RQ4-Evaluation-Group-Aggregated.csv"
# OUT_CSV = r"E:/.../study_wise_evaluation_metrics.csv"

# ---- Config ----
STUDY_START = 1
STUDY_END = 127  # inclusive

# ---- Load ----
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

# Map: "S1" -> set of metrics
study_to_metrics = defaultdict(set)

# Extract studies like S1, S2, ... (case-insensitive)
study_pat = re.compile(r"\bS(\d{1,3})\b", re.IGNORECASE)

for _, row in df.iterrows():
    studies_cell = row.get("Studies", "")
    metric = row.get("Group Name", "")

    if not isinstance(metric, str) or not metric.strip():
        continue
    if not isinstance(studies_cell, str) or not studies_cell.strip():
        continue

    metric_clean = metric.strip()

    # Find all studies mentioned in this cell
    nums = study_pat.findall(studies_cell)
    for n in nums:
        n_int = int(n)
        if STUDY_START <= n_int <= STUDY_END:
            study_to_metrics[f"S{n_int}"].add(metric_clean)

# Build output for ALL studies S1..S127 (even if empty)
out_rows = []
for i in range(STUDY_START, STUDY_END + 1):
    s = f"S{i}"
    metrics_sorted = sorted(study_to_metrics.get(s, set()), key=lambda x: x.lower())
    out_rows.append({
        "Study#": s,
        "EvaluationMetrics": "; ".join(metrics_sorted)
    })

out_df = pd.DataFrame(out_rows, columns=["Study#", "EvaluationMetrics"])
out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")

print(f"Saved: {OUT_CSV}")
