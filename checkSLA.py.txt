import csv
import sys

total = 0
failed = 0
total_time = 0

with open("JpetStorePractice_Updated.jtl", newline='') as file:
    reader = csv.DictReader(file)

    for row in reader:
        total += 1
        total_time += int(row["elapsed"])

        if row["success"].lower() == "false":
            failed += 1

average = total_time / total
error_percentage = (failed / total) * 100

print("================================")
print("Average Response Time :", average, "ms")
print("Error Percentage      :", error_percentage, "%")
print("================================")

if average > 2000:
    print("SLA Failed : Average Response Time > 2 seconds")
    sys.exit(1)

if error_percentage > 1:
    print("SLA Failed : Error Percentage > 1%")
    sys.exit(1)

print("SLA Passed")
sys.exit(0)