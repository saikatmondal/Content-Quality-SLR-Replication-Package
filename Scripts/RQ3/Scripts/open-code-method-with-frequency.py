import pandas as pd
import re
from collections import Counter

IN_CSV  = r".../RQ3/RQ3-Methodologies.csv"
OUT_CSV = r".../RQ3/Outputs/unique-method-frequency.csv"

# Load dataset
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

counter = Counter()

# Extract content inside [...]
bracket_pattern = re.compile(r"\[(.*?)\]")

# Split on commas NOT inside parentheses
comma_split_pattern = re.compile(r",\s*(?![^()]*\))")

for value in df.get("Categorized_Methodology", []):
    if not isinstance(value, str) or not value.strip():
        continue

    for group in bracket_pattern.findall(value):
        if not group.strip():
            continue

        terms = [
            t.strip().lower()
            for t in comma_split_pattern.split(group)
            if t.strip()
        ]
        counter.update(terms)

# Convert to DataFrame
out_df = pd.DataFrame(
    sorted(counter.items(), key=lambda x: (-x[1], x[0])),
    columns=["metric name", "frequency"]
)

# Write output
out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")

print(f"Saved unique method frequencies to:\n{OUT_CSV}")



# import pandas as pd
# import re
# from collections import Counter

# IN_CSV  = r"E:/PhD Milestones/Comprehensive/ReplicationPackage/ResearchQuestions/RQ3/RQ3-V7.csv"
# OUT_CSV = r"E:/PhD Milestones/Comprehensive/ReplicationPackage/Data-N-Scripts/RQ3/Outputs/unique-method-frequency.csv"

# # Load dataset
# df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

# counter = Counter()
# pattern = re.compile(r"\[(.*?)\]")  # extract all [...]

# for value in df.get("Categorized_Methodology", []):
#     if not isinstance(value, str) or not value.strip():
#         continue

#     # Find all bracketed groups
#     for group in pattern.findall(value):
#         if not group.strip():
#             continue

#         # Normalize: strip spaces + lowercase
#         terms = [
#             t.strip().lower()
#             for t in group.split(",")
#             if t.strip()
#         ]
#         counter.update(terms)

# # Convert to DataFrame (sorted by frequency desc, name asc)
# out_df = pd.DataFrame(
#     sorted(counter.items(), key=lambda x: (-x[1], x[0])),
#     columns=["metric name", "frequency"]
# )

# # Write output CSV
# out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")

# print(f"Saved unique metric frequencies to:\n{OUT_CSV}")