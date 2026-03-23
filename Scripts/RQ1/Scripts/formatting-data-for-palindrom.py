import csv

# Input CSV file path
csv_path = r".../RQ1/Outputs/analyzed_components_by_study_.....csv"

output_lines = []

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for idx, row in enumerate(reader, start=1):
        feature = row["Feature Name"].strip()
        count = row["Count"].strip()
        percentage = row["Percentage"].strip().replace("%", "")
        
        line = (
            f'{{ "name": "{feature} - {count} ({percentage}%)", '
            f'"id": "1_{idx}" }},'
        )
        output_lines.append(line)

# Print output
for line in output_lines:
    print(line)
