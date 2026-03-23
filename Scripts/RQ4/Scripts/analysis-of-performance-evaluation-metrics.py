import pandas as pd
from collections import defaultdict

# =========================
# Input / Output
# =========================
IN_CSV  = r".../RQ4/RQ4-Evaluation.csv"
OUT_CSV = r".../RQ4/Outputs/RQ4-Evaluation-Processed.csv"

# =========================
# Load data
# =========================
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

# Validate required columns
required_cols = {"Study#", "Final Performance Evaluation"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# =========================
# Aggregate: metric -> set(studies)
# =========================
metric_study_map = defaultdict(set)

for _, row in df.iterrows():
    study = str(row["Study#"]).strip()
    metrics = row["Final Performance Evaluation"]

    if not study or study.lower() == "nan":
        continue

    if isinstance(metrics, str):
        for m in metrics.split(";"):
            metric = m.strip().lower()   # normalize to lower case
            if metric and metric != "nan":
                metric_study_map[metric].add(study)

# =========================
# Build output DataFrame
# =========================
out_rows = []
for metric, studies in metric_study_map.items():
    out_rows.append({
        "Evaluation Metric Name": metric,
        "Study Count": len(studies),
        "Studies": ", ".join(sorted(studies, key=lambda x: (len(x), x)))
    })

out_df = pd.DataFrame(out_rows).sort_values(
    by=["Study Count", "Evaluation Metric Name"],
    ascending=[False, True]
).reset_index(drop=True)

# =========================
# Save CSV
# =========================
out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")

# =========================
# Preview
# =========================
# print(out_df.head(20).to_string(index=False))
# print(f"\nSaved: {OUT_CSV}")
