import pandas as pd
import re

IN_CSV  = r".../RQ5/RQ5-Publication-Metadata.csv"
OUT_CSV = r".../RQ5/Outputs/study-wise-author-gender-composition-v1.csv"

# Load data
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

required_cols = {"Study#", "Gender"}
if not required_cols.issubset(df.columns):
    raise ValueError("CSV must contain 'Study#' and 'Gender' columns")

rows = []
sl = 1  # serial number

for _, row in df.iterrows():
    study = row.get("Study#", "")
    gender_cell = row.get("Gender", "")

    if not isinstance(study, str) or not study.strip():
        continue

    # Split genders
    if isinstance(gender_cell, str) and gender_cell.strip():
        genders = [g.strip().lower() for g in gender_cell.split(";") if g.strip()]
    else:
        genders = []

    total_authors = len(genders)

    # Normalize genders
    males = {"m", "male", "man"}
    females = {"f", "female", "woman"}

    has_male = any(g in males for g in genders)
    has_female = any(g in females for g in genders)

    if total_authors == 0:
        composition = "Unknown"
    elif has_male and not has_female:
        composition = "Men Only"
    elif has_female and not has_male:
        composition = "Female Only"
    else:
        composition = "Mix"

    rows.append({
        "Study#": study.strip(),
        "SL": sl,
        "Total Authors": total_authors,
        "Author Gender Composition": composition
    })

    sl += 1

out_df = pd.DataFrame(
    rows,
    columns=["Study#", "SL", "Total Authors", "Author Gender Composition"]
)

out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")
print(f"Saved: {OUT_CSV}")
