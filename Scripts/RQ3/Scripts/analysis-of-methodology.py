import re
import pandas as pd

# =========================
# Inputs
# =========================
IN_CSV  = r".../RQ3/RQ3-Methodologies.csv"
OUT_CSV = r".../RQ3/Outputs/RQ3-Methodologies-Processed.csv"

# =========================
# Helpers
# =========================
PAIR_RE = re.compile(r'\s*([^;\[\]]+?)\s*\[\s*([^\]]*?)\s*\]\s*')  # HighLabel [details]

def split_items(s: str):
    """Split details by comma, trim, drop empties, keep order unique (case-insensitive)."""
    if not isinstance(s, str):
        return []
    parts = [p.strip() for p in s.split(",")]
    seen, out = set(), []
    for p in parts:
        if p and p.lower() != "nan":
            key = p.lower()          # <-- normalization
            if key not in seen:
                seen.add(key)
                out.append(key)     # <-- store lowercase
    return out


# def split_items(s: str):
#     """Split details by comma, trim, drop empties, keep order unique."""
#     if not isinstance(s, str):
#         return []
#     parts = [p.strip() for p in s.split(",")]
#     seen, out = set(), []
#     for p in parts:
#         if p and p.lower() != "nan" and p not in seen:
#             seen.add(p)
#             out.append(p)
#     return out

def parse_label_coding(label_coding: str):
    """
    Parse: High label metrics [details raw metrics]; High2 [details2];
    Returns: list of (methodology, [raw_metrics...])
    """
    if not isinstance(label_coding, str) or not label_coding.strip():
        return []

    pairs = []
    for m in PAIR_RE.finditer(label_coding):
        methodology = m.group(1).strip()
        details_str = m.group(2).strip()
        raw_metrics = split_items(details_str)
        if methodology:
            pairs.append((methodology, raw_metrics))
    return pairs

# =========================
# Load & validate (ISO-8859-1)
# =========================
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

required_cols = {"Study#", "Categorized_Methodology"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns in {IN_CSV}: {sorted(missing)}")

# =========================
# Aggregate
# =========================
agg = {}  # methodology -> {"studies": set(), "metrics": set()}
for _, row in df.iterrows():
    study = str(row["Study#"]).strip()
    categorized_methodology = row["Categorized_Methodology"]

    for methodology, raw_metrics in parse_label_coding(categorized_methodology):
        if methodology not in agg:
            agg[methodology] = {"studies": set(), "metrics": set()}
        if study and study.lower() != "nan":
            agg[methodology]["studies"].add(study)
        for rm in raw_metrics:
            agg[methodology]["metrics"].add(rm)

# =========================
# Build output table
# =========================
out_rows = []
for methodology, d in agg.items():
    studies = sorted(d["studies"], key=lambda x: (len(x), x))
    metrics = sorted(d["metrics"], key=lambda x: x.lower())

    out_rows.append({
        "Methodology": methodology,
        "Count": len(studies),
        "Associated Studies": ", ".join(studies),
        "Details": ", ".join(metrics),
    })

out_df = pd.DataFrame(out_rows).sort_values(
    by=["Count", "Methodology"], ascending=[False, True]
).reset_index(drop=True)

# =========================
# Save (ISO-8859-1)
# =========================
out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")

# Preview
# print(out_df.head(2).to_string(index=False))
# print(f"\nSaved: {OUT_CSV}")
