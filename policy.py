# policy.py
def compute(days, miles, receipts):
    per_diem = (
        days * 100 if days <= 5 else
        days * 75 if days <= 10 else
        days * 50
    )
    if days == 5:
        per_diem += 50

    if miles <= 100:
        mileage = miles * 0.58
    else:
        mileage = 100 * 0.58 + (miles - 100) * 0.40

    if days < 4:
        cap_day = 75
    elif days <= 6:
        cap_day = 120
    else:
        cap_day = 90

    cap_total = cap_day * days
    if receipts < 50:
        reimb = 0
    elif receipts <= cap_total:
        reimb = receipts
    else:
        reimb = cap_total + (receipts - cap_total) * 0.25

    miles_per_day = miles / days if days != 0 else 0
    if 180 <= miles_per_day <= 220:
        reimb += 20

    if days >= 8 and receipts / days > 90:
        reimb -= 30

    if round(receipts - int(receipts), 2) in (0.49, 0.99):
        reimb += 1

    return round(per_diem + mileage + reimb, 2)
