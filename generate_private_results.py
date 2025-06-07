import json
import subprocess

with open("private_cases.json") as f:
    data = json.load(f)

results = []

for case in data:
    d = str(case["trip_duration_days"])
    m = str(case["miles_traveled"])
    r = str(case["total_receipts_amount"])

    result = subprocess.check_output(["./run.sh", d, m, r])
    results.append(result.decode().strip())

with open("private_results.txt", "w") as f:
    for line in results:
        f.write(line + "\n")

print("✅ private_results.txt generated")
