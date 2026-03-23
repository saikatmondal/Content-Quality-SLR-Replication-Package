import pandas as pd
from collections import defaultdict

# Load the CSV file with appropriate encoding
file_path = ".../RQ1/RQ1-Target-And-Analyzed-Components.csv"
df = pd.read_csv(file_path, encoding="ISO-8859-1")

# Filter only rows where relevant column is not null
filtered_df = df[df["Question"].notnull()]

# Normalize component strings
def normalize_component(component):
    return component.strip().lower().replace('\n', ' ').replace('\r', '').replace('  ', ' ')

# Dictionary to map each component to a set of study numbers
component_study_map = defaultdict(set)

# Build mapping from "Analyzed Componets"
for _, row in filtered_df.iterrows():
    study = str(row["Study#"]).strip()
    components = str(row["Analyzed Componets"])
    if components and study:
        # Split by semicolon and normalize
        for comp in components.split(';'):
            norm_comp = normalize_component(comp)
            if norm_comp:
                component_study_map[norm_comp].add(study)

# Create result DataFrame
result_df = pd.DataFrame(
    [(component, ", ".join(sorted(studies)), len(studies)) for component, studies in sorted(component_study_map.items())],
    columns=["Feature Name", "Studies", "Count"]
)

# Save result
output_path = "E:/PhD Milestones/Comprehensive/ReplicationPackage/Data-N-Scripts/RQ1/Outputs/analyzed_components_by_study_question_v2.csv"
result_df.to_csv(output_path, index=False)

# Print sample output
print(result_df.sort_values(by="Count", ascending=False).head(20))
