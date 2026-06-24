import csv
import random

# Read CSV file
with open("employee_data.csv", "r") as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Display original salaries
print("\n===== BEFORE SWAPPING =====")
for row in data:
    print(f"{row['name']} -> Salary: {row['salary']}")

# Extract and shuffle salaries
salaries = [row["salary"] for row in data]
random.shuffle(salaries)

# Assign swapped salaries back
for i in range(len(data)):
    data[i]["salary"] = salaries[i]

# Display swapped salaries
print("\n===== AFTER SWAPPING =====")
for row in data:
    print(f"{row['name']} -> Salary: {row['salary']}")

# Save swapped data
with open("swapped_employee_data.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["name", "age", "zip_code", "salary", "medical_risk"]
    )
    writer.writeheader()
    writer.writerows(data)

print("\nData swapping completed successfully!")
print("Swapped dataset saved as 'swapped_employee_data.csv'")