import csv
import math
import sys
from collections import defaultdict

# -------------------------------
# Configuration
# -------------------------------
JTL_FILE = "JpetStorePractice_Updated.jtl"

ERROR_THRESHOLD = 2      # Overall Error %
P90_THRESHOLD = 5000     # milliseconds (5 sec)

# -------------------------------
# Store transaction data
# -------------------------------
transaction_times = defaultdict(list)
transaction_total = defaultdict(int)
transaction_failed = defaultdict(int)

overall_total = 0
overall_failed = 0


# -------------------------------
# Function to calculate percentile
# -------------------------------
def calculate_percentile(values, percentile):

    values.sort()

    index = math.ceil((percentile / 100) * len(values)) - 1

    if index < 0:
        index = 0

    if index >= len(values):
        index = len(values) - 1

    return values[index]


# -------------------------------
# Read JTL
# -------------------------------
with open(JTL_FILE, newline='', encoding='utf-8') as file:

    reader = csv.DictReader(file)

    for row in reader:

        label = row["label"]

        # Read only Transaction Controllers
        if not label.startswith("T"):
            continue

        elapsed = int(row["elapsed"])
        success = row["success"].lower() == "true"

        overall_total += 1

        transaction_total[label] += 1
        transaction_times[label].append(elapsed)

        if not success:
            overall_failed += 1
            transaction_failed[label] += 1


# -------------------------------
# Overall Error %
# -------------------------------
overall_error = 0

if overall_total > 0:
    overall_error = (overall_failed / overall_total) * 100


print("\n====================================================")
print("          PERFORMANCE TEST SLA REPORT")
print("====================================================")
print(f"Total Transactions     : {overall_total}")
print(f"Failed Transactions    : {overall_failed}")
print(f"Overall Error %        : {overall_error:.2f}%")
print("====================================================\n")


build_failed = False

# -------------------------------
# Check Overall Error %
# -------------------------------
if overall_error > ERROR_THRESHOLD:

    print(f"FAIL : Overall Error % ({overall_error:.2f}) exceeded SLA ({ERROR_THRESHOLD}%)\n")

    build_failed = True

else:

    print(f"PASS : Overall Error % within SLA ({ERROR_THRESHOLD}%)\n")


# -------------------------------
# Transaction Wise P90
# -------------------------------
print("Transaction Wise Response Time")
print("-" * 70)
print("{:<30} {:>10} {:>15}".format("Transaction", "P90(ms)", "Status"))
print("-" * 70)

for transaction in sorted(transaction_times.keys()):

    p90 = calculate_percentile(transaction_times[transaction], 90)

    if p90 > P90_THRESHOLD:

        status = "FAIL"
        build_failed = True

    else:

        status = "PASS"

    print("{:<30} {:>10} {:>15}".format(transaction, p90, status))

print("-" * 70)


# -------------------------------
# Final Result
# -------------------------------
if build_failed:

    print("\nBUILD FAILED : SLA Violated")

    sys.exit(1)

else:

    print("\nBUILD PASSED : SLA Met")

    sys.exit(0)