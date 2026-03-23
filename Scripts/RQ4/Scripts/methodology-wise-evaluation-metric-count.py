import pandas as pd
from collections import Counter

IN_CSV  = r".../RQ4/Outputs/methodology-vs-evaluation-metrics.csv"
OUT_CSV = r".../RQ4/Outputs/methodology-wise-metric-counts.csv"


df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

METHOD_COLS = [f"M{i}" for i in range(1, 12)]  # M1..M11
METRIC_COL = "EvaluationMetrics"

# Counter per methodology
method_to_counter = {m: Counter() for m in METHOD_COLS}

def split_metrics(s: str):
    """Split by ';' and clean tokens."""
    if not isinstance(s, str):
        return []
    parts = [p.strip() for p in s.split(";")]
    return [p for p in parts if p]  # drop empties

for _, row in df.iterrows():
    metrics = split_metrics(row.get(METRIC_COL, ""))

    if not metrics:
        continue

    for m in METHOD_COLS:
        val = row.get(m, 0)

        # Treat 1 / "1" / 1.0 as present
        present = False
        if isinstance(val, (int, float)) and val == 1:
            present = True
        elif isinstance(val, str) and val.strip() == "1":
            present = True

        if present:
            method_to_counter[m].update(metrics)

# Build output rows
out_rows = []
for m in METHOD_COLS:
    c = method_to_counter[m]

    # Sort metrics by count desc, then name asc (deterministic)
    items = sorted(c.items(), key=lambda x: (-x[1], x[0].lower()))

    formatted = "; ".join([f"{name} ({count})" for name, count in items])

    out_rows.append({
        "Methodology": m,
        "EvaluationMetrics(Count)": formatted
    })

out_df = pd.DataFrame(out_rows, columns=["Methodology", "EvaluationMetrics(Count)"])
out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")

print(f"Saved: {OUT_CSV}")
