from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api():
    response = client.post("/predict-risk", json={
        "monthly_charges": 50,
        "previous_month_charges": 20,
        "contract_type": "Month-to-month",
        "tickets": []
    })
    assert response.status_code == 200