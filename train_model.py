import pandas as pd, numpy as np, joblib, json
from sklearn.ensemble import GradientBoostingRegressor
from policy import compute

with open('public_cases.json') as f:
    data = json.load(f)

X, y = [], []

for case in data:
    i = case['input']
    d, m, r = i['trip_duration_days'], i['miles_traveled'], i['total_receipts_amount']
    rule_est = compute(d, m, r)

    features = [
        d, m, r,
        m / d, r / d,
        rule_est,
        int(d == 5),
        int(r < 50),
        int((r / d) > 90)
    ]

    X.append(features)
    y.append(case['expected_output'] - rule_est)  # residual

model = GradientBoostingRegressor(
    n_estimators=300,
    max_depth=3,
    learning_rate=0.05,
    subsample=0.7,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, 'reimb_model.pkl')
print("✅ Model saved as reimb_model.pkl")
