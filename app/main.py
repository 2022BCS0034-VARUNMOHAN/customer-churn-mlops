from fastapi import FastAPI
from app.rules import calculate_risk

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Churn Risk API running"}

@app.post("/predict-risk")
def predict(data: dict):
    risk = calculate_risk(data)
    return {"risk": risk}