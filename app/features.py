from datetime import datetime

def extract_features(data):
    tickets = data.get("tickets", [])
    monthly = data.get("monthly_charges", 0)
    previous = data.get("previous_month_charges", 0)
    contract = data.get("contract_type", "")

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

    return [[
        t7,
        t30,
        t90,
        complaint,
        query,
        charge_change,
        1 if contract.lower() == "month-to-month" else 0
    ]]