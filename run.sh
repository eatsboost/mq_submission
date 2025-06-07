#!/usr/bin/env bash

days=$1
miles=$2
receipts=$3

python3 - <<EOF
import numpy as np, joblib, policy, sys

# Parse input
d = int(${days})
m = float(${miles})
r = float(${receipts})

# Rule-based estimate
base = policy.compute(d, m, r)

# Guardrails to prevent overfitting on unseen inputs
if d < 1 or d > 20 or m > 2000 or r > 5000:
    print(f"{base:.2f}")
    sys.exit(0)

# Load model
model = joblib.load("reimb_model.pkl")

# Construct features
features = np.array([[d, m, r, m/d, r/d, base, int(d==5), int(r<50), int((r/d)>90)]])
final = base + model.predict(features)[0]

# Rounding bug
cents = round(r - int(r), 2)
if cents in (0.49, 0.99):
    final += 1

print(f"{final:.2f}")
EOF
