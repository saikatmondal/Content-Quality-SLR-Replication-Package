import pandas as pd
from collections import defaultdict

IN_CSV  = r".../RQ5/RQ5-Publication-Metadata.csv"
OUT_CSV = r".../RQ5/Outputs/venue-wise-published-studies-v1.csv"

# Load
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")
required_cols = {"Journal/Conference Name", "Study#", "Year", "Journal/Conference"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# (venue, type) -> list of "Sx (Year)"
venue_to_entries = defaultdict(list)

for _, row in df.iterrows():
    venue = row.get("Journal/Conference Name", "")
    vtype = row.get("Journal/Conference", "")
    study = row.get("Study#", "")
    year  = row.get("Year", "")

    if not isinstance(venue, str) or not venue.strip():
        continue
    if not isinstance(vtype, str) or not vtype.strip():
        continue
    if not isinstance(study, str) or not study.strip():
        continue
    if pd.isna(year) or not str(year).strip():
        continue

    entry = f"{study.strip()} ({int(year)})"
    venue_to_entries[(venue.strip(), vtype.strip())].append(entry)

# Build output rows (sorted by total desc, then venue asc)
out_rows = []
for (venue, vtype), entries in venue_to_entries.items():
    out_rows.append({
        "Venue": venue,
        "Journal/Conference": vtype,
        "Published studies": ", ".join(entries),
        "Total": len(entries)
    })

out_df = pd.DataFrame(out_rows, columns=["Venue", "Journal/Conference", "Published studies", "Total"])
out_df = out_df.sort_values(by=["Total", "Venue"], ascending=[False, True])

# Save
out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")
print(f"Saved: {OUT_CSV}")
