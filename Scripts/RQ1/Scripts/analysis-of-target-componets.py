import csv

# Input CSV file path
csv_path = r".../RQ1/RQ1-Target-And-Analyzed-Components.csv"

selected_studies = []

# Read the CSV
with open(csv_path, newline='', encoding="ISO-8859-1") as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        # Check if Question == 1
        if row.get("Qn_title", "").strip() == "1":
            selected_studies.append(row.get("Study#", "").strip())

# Remove empty entries if any
selected_studies = [s for s in selected_studies if s]

# Prepare output
studies_str = ", ".join(selected_studies)
total_count = len(selected_studies)

# Print results
print("Selected Studies:")
print(studies_str)
print("\nTotal Count:", total_count)
