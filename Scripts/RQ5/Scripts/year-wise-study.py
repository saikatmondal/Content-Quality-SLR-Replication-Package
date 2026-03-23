import pandas as pd
from collections import defaultdict

IN_CSV  = r".../RQ5/RQ5-Publication-Metadata.csv"
OUT_CSV = r".../RQ5/Outputs/year-wise-published-studies-v1.csv"

# Load data
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

required_cols = {"Year", "Study#", "Journal/Conference Name"}
if not required_cols.issubset(df.columns):
    raise ValueError(f"CSV must contain columns: {required_cols}")

# year -> list of "Sx (Venue)"
year_to_entries = defaultdict(list)

for _, row in df.iterrows():
    year = row.get("Year", "")
    study = row.get("Study#", "")
    venue = row.get("Journal/Conference Name", "")

    if pd.isna(year) or not str(year).strip():
        continue
    if not isinstance(study, str) or not study.strip():
        continue
    if not isinstance(venue, str) or not venue.strip():
        continue

    entry = f"{study.strip()} ({venue.strip()})"
    year_to_entries[int(year)].append(entry)

# Build output rows (sorted by year)
out_rows = []
for year in sorted(year_to_entries.keys()):
    studies = year_to_entries[year]
    out_rows.append({
        "Year": year,
        "Published studies": ", ".join(studies),
        "Total": len(studies)
    })

out_df = pd.DataFrame(out_rows, columns=["Year", "Published studies", "Total"])
out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")

print(f"Saved year-wise publication summary to:\n{OUT_CSV}")
