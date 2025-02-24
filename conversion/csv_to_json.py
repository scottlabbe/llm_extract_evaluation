import csv, json, os

# Define file paths
csv_path = '/Users/scottlabbe/Projects/Evaluate/extraction/data/pdf_extract_questions.csv'
json_path = os.path.join(os.path.dirname(csv_path), 'pdf_extract_questions.json')

# Create a dictionary to group rows by report number
reports = {}

with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader, start=1):
        report = row["Report #"]
        if report not in reports:
            reports[report] = []
        # Use the '#' column if it exists, otherwise fallback to row number
        question_id = row.get("#", str(i))
        reports[report].append({
            "id": question_id,
            "question": row["Question"],
            "answer": row["Answer"]
        })

# Write the grouped data to JSON with pretty printing
with open(json_path, "w") as jsonfile:
    json.dump(reports, jsonfile, indent=4)

print(f"JSON file created at: {json_path}")