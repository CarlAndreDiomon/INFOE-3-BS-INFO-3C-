import copy
import csv

# Sample dataset from previous lab
raw_data = [
    {
        "name": "John Cruz",
        "age": 27,
        "zip_code": "58001",
        "salary": 65000,
        "medical_risk": "Low"
    },
    {
        "name": "Maria Santos",
        "age": 34,
        "zip_code": "58002",
        "salary": 72000,
        "medical_risk": "Medium"
    },
    {
        "name": "Mark Reyes",
        "age": 42,
        "zip_code": "58003",
        "salary": 85000,
        "medical_risk": "High"
    }
]

# Create a safe copy
new_data = copy.deepcopy(raw_data)

# Keys to suppress
hit_list = ["name", "medical_risk"]

# Suppression Process
for record in new_data:
    for key in hit_list:
        record.pop(key, None)

# Verification
print("Sample Record After Suppression:")
print(new_data[0])

# Export to CSV
with open("privacy_cleaned_data.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["age", "zip_code", "salary"]
    )

    writer.writeheader()
    writer.writerows(new_data)

print("Privacy-cleaned dataset saved successfully.")