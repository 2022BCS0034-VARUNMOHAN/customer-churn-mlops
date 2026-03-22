import pandas as pd
import json
import random
from datetime import datetime, timedelta

df = pd.read_csv("data/Telco-Customer-Churn.csv")

processed = []

for _, row in df.iterrows():

    monthly = float(row["MonthlyCharges"])
    previous = monthly - random.uniform(-20, 20)

    tickets = []
    num_tickets = random.randint(0, 6)

    for _ in range(num_tickets):
        tickets.append({
            "type": random.choice(["complaint", "query"]),
            "date": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
        })

    processed.append({
        "customerID": row["customerID"],
        "monthly_charges": monthly,
        "previous_month_charges": round(previous, 2),
        "contract_type": row["Contract"],
        "tickets": tickets
    })

with open("data/processed_data.json", "w") as f:
    json.dump(processed, f, indent=2)

print("Processed data saved!")