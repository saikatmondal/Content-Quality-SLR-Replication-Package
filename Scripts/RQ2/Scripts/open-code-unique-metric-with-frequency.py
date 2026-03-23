import pandas as pd
import re
from collections import Counter

IN_CSV  = r".../RQ2/RQ2-Quality-Metrics"
OUT_CSV = r".../RQ2/Outputs/unique-metric-frequency.csv"

# Load dataset
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

counter = Counter()
pattern = re.compile(r"\[(.*?)\]")  # extract all [...]

for value in df.get("Label_Coding", []):
    if not isinstance(value, str) or not value.strip():
        continue

    # Find all bracketed groups
    for group in pattern.findall(value):
        if not group.strip():
            continue

        # Normalize: strip spaces + lowercase
        terms = [
            t.strip().lower()
            for t in group.split(",")
            if t.strip()
        ]
        counter.update(terms)

# Convert to DataFrame (sorted by frequency desc, name asc)
out_df = pd.DataFrame(
    sorted(counter.items(), key=lambda x: (-x[1], x[0])),
    columns=["metric name", "frequency"]
)

# Write output CSV
out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")

print(f"Saved unique metric frequencies to:\n{OUT_CSV}")