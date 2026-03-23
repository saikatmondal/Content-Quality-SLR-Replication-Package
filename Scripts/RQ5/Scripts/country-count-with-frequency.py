import pandas as pd
import re
from collections import Counter

IN_CSV  = r".../RQ5/RQ5-Publication-Metadata.csv"
OUT_CSV = r".../RQ5/Outputs/country-with-frequency-count-v1.csv"

# Load data
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

if "Country" not in df.columns:
    raise ValueError("CSV must contain a 'Country' column")

counter = Counter()

def normalize_country(name: str) -> str:
    """
    Normalize country names by:
    - stripping leading/trailing spaces
    - collapsing multiple spaces
    """
    name = name.strip()
    name = re.sub(r"\s+", " ", name)
    return name

for _, row in df.iterrows():
    cell = row.get("Country", "")

    if not isinstance(cell, str) or not cell.strip():
        continue

    countries = [
        normalize_country(c)
        for c in cell.split(";")
        if c.strip()
    ]

    counter.update(countries)

# Build output
out_df = pd.DataFrame(
    sorted(counter.items(), key=lambda x: (-x[1], x[0].lower())),
    columns=["Country", "Count"]
)

out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")

print(f"Saved country-wise counts to:\n{OUT_CSV}")
