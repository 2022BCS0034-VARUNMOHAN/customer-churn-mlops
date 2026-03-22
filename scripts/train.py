import json
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
import joblib
import matplotlib.pyplot as plt
import os

# create artifacts folder
os.makedirs("artifacts", exist_ok=True)

# load data
with open("data/processed_data.json") as f:
    data = json.load(f)

rows = []

for customer in data:
    tickets = customer.get("tickets", [])
    monthly = customer.get("monthly_charges", 0)
    previous = customer.get("previous_month_charges", 0)
    contract = customer.get("contract_type", "")

    now = datetime.now()

    t7 = t30 = t90 = 0
    complaint = 0
    query = 0

    for t in tickets:
        if "date" in t:
            try:
                d = datetime.fromisoformat(t["date"])
                days = (now - d).days

                if days <= 7:
                    t7 += 1
                if days <= 30:
                    t30 += 1
                if days <= 90:
                    t90 += 1
            except:
                continue

        if t.get("type") == "complaint":
            complaint += 1
        if t.get("type") == "query":
            query += 1

    charge_change = monthly - previous

    # simulate churn label
    churn = 1 if t30 > 5 or (contract == "Month-to-month" and complaint > 0) else 0

    rows.append({
        "t7": t7,
        "t30": t30,
        "t90": t90,
        "complaint": complaint,
        "query": query,
        "charge_change": charge_change,
        "contract": 1 if contract.lower() == "month-to-month" else 0,
        "churn": churn
    })

df = pd.DataFrame(rows)

X = df.drop("churn", axis=1)
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

preds = model.predict(X_test)
probs = model.predict_proba(X_test)[:, 1]

# metrics
report = classification_report(y_test, preds)
roc = roc_auc_score(y_test, probs)

print("Classification Report:")
print(report)
print("ROC AUC:", roc)

# save metrics
with open("artifacts/metrics.txt", "w") as f:
    f.write("Classification Report:\n")
    f.write(report)
    f.write("\nROC AUC: " + str(roc))

# ROC curve
fpr, tpr, _ = roc_curve(y_test, probs)

plt.figure()
plt.plot(fpr, tpr, label="ROC Curve")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.savefig("artifacts/roc_curve.png")
plt.show()

# save model
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")