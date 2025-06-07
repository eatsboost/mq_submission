# generate_private_results_fast.py

import json
import numpy as np
import joblib
from policy import compute

# 1. Load private cases
with open("private_cases.json") as f:
    private = json.load(f)

# 2. Load model once
model = joblib.load("reimb_model.pkl")

# 3. Predict in batch
results = []
for case in private:
    d = case["trip_duration_days"]
    m = case["miles_traveled"]
    r = case["total_receipts_amount"]
    
    # Rule-based estimate
    base = compute(d, m, r)
    
    # Guardrail for unseen inputs
    if d < 1 or d > 20 or m > 2000 or r > 5000:
        pred = base
    else:
        feats = np.array([[d, m, r, m/d, r/d, base, int(d==5), int(r<50), int((r/d)>90)]])
        pred = base + model.predict(feats)[0]
        # Rounding bug
        cents = round(r - int(r), 2)
        if cents in (0.49, 0.99):
            pred += 1
    
    results.append(round(pred, 2))

# 4. Write to private_results.txt
with open("private_results.txt", "w") as f:
    for v in results:
        f.write(f"{v:.2f}\n")

print("✅ private_results.txt generated (fast)")
