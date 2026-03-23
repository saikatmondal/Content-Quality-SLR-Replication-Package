import pandas as pd
import re
from collections import defaultdict

IN_CSV  = r".../RQ5/RQ5-Publication-Metadata.csv"
OUT_CSV = r".../RQ5/Outputs/contributing-authors-gender-count-v1.csv"

# Load data
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

required_cols = {"Authors", "Gender"}
if not required_cols.issubset(df.columns):
    raise ValueError("CSV must contain 'Authors' and 'Gender' columns")

def normalize_author_name(name: str) -> str:
    """
    Normalize author names by:
    - stripping leading/trailing spaces
    - collapsing multiple internal spaces into one
    """
    name = name.strip()
    name = re.sub(r"\s+", " ", name)
    return name

# (author, gender) -> count
author_gender_count = defaultdict(int)

for _, row in df.iterrows():
    authors_cell = row.get("Authors", "")
    gender_cell  = row.get("Gender", "")

    if not isinstance(authors_cell, str) or not authors_cell.strip():
        continue
    if not isinstance(gender_cell, str) or not gender_cell.strip():
        continue

    authors = [
        normalize_author_name(a)
        for a in authors_cell.split(";")
        if a.strip()
    ]

    genders = [
        g.strip().lower()
        for g in gender_cell.split(";")
        if g.strip()
    ]

    # Safety check: lengths should match
    if len(authors) != len(genders):
        print(f"WARNING: Author/Gender length mismatch -> {authors_cell} | {gender_cell}")
        continue

    for author, gender in zip(authors, genders):
        author_gender_count[(author, gender)] += 1

# Build output rows
rows = []
for (author, gender), count in sorted(
    author_gender_count.items(),
    key=lambda x: (-x[1], x[0][0].lower())
):
    rows.append({
        "Author Name": author,
        "Gender": gender.capitalize(),
        "Count": count
    })

out_df = pd.DataFrame(rows, columns=["Author Name", "Gender", "Count"])
out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")

print(f"Saved: {OUT_CSV}")