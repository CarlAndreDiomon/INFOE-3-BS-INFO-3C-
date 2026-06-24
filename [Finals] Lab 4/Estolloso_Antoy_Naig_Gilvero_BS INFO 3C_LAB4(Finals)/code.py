import csv
import copy

# 1. Load the data generated from Lab 3
lab3_data = []
with open('privacy_cleaned_dataset.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        lab3_data.append(dict(row))

# Protect the data
generalized_data = copy.deepcopy(lab3_data)

# Print "Before" version
if generalized_data:
    print("Before Generalization:", lab3_data[0])

# 2 & 3. Execute Generalization and Extra Logic
for record in generalized_data:
    # Convert age from string to int for math, then apply Floor Division
    age_int = int(record['age'])
    generalized_age = (age_int // 10) * 10
    record['age'] = str(generalized_age) # Update the key
    
    # Extra Criteria: Life Stages
    if age_int < 30:
        record['life_stage'] = "Under 30"
    elif 30 <= age_int <= 50:
        record['life_stage'] = "30 to 50"
    else:
        record['life_stage'] = "Over 50"

    # Zip Code String Slicing: Keep first 3, add XX
    current_zip = record['zip_code']
    record['zip_code'] = current_zip[:3] + "XX"

# Print "After" version
if generalized_data:
    print("After Generalization: ", generalized_data[0])

# 4. Export to new CSV
output_filename = "generalized_dataset.csv"
fieldnames = ["age", "life_stage", "zip_code", "salary"]

with open(output_filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    
    for record in generalized_data:
        writer.writerow(record)
        
print(f"Success: Exported to {output_filename}")