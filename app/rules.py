from datetime import datetime

def calculate_risk(data):
    tickets = data.get("tickets", [])
    contract = data.get("contract_type", "")
    monthly = data.get("monthly_charges", 0)
    previous = data.get("previous_month_charges", 0)

    # calculate charge increase
    charge_increase = monthly - previous

    # count tickets in last 30 days
    recent_tickets = 0
    for t in tickets:
        if "date" in t:
            try:
                ticket_date = datetime.fromisoformat(t["date"])
                if (datetime.now() - ticket_date).days <= 30:
                    recent_tickets += 1
            except:
                continue

    # ✅ PRIORITY 1: Complaint + Month-to-month → HIGH
    if contract.lower() == "month-to-month":
        for t in tickets:
            if t.get("type") == "complaint":
                return "HIGH"

    # ✅ PRIORITY 2: Too many tickets → HIGH
    if recent_tickets > 5:
        return "HIGH"

    # ✅ PRIORITY 3: Charge increase + moderate tickets → MEDIUM
    if charge_increase > 0 and recent_tickets >= 3:
        return "MEDIUM"

    # ✅ DEFAULT
    return "LOW"