import pandas as pd

# Load the CSV file
input_path = ".../RQ1/RQ1-Target-And-Analyzed-Components.csv"
df = pd.read_csv(input_path)

# Extract and normalize the "Target Q&A Site" column
sites = (
    df["Target Q&A Site"]
    .dropna()
    .astype(str)
    .str.replace('"', '', regex=False)
    .str.split(";")
)

# Flatten and clean
flat_sites = []
for row in sites:
    for site in row:
        site_clean = site.strip()
        if site_clean:
            flat_sites.append(site_clean)

# Count frequency
freq_df = (
    pd.Series(flat_sites)
    .value_counts()
    .reset_index()
)

freq_df.columns = ["Q&A Names", "Frequency"]

# Save output CSV
output_path = ".../RQ1/Outputs/forums_with_frequency.csv"
freq_df.to_csv(output_path, index=False)

freq_df.head(), output_path
