from fastapi import FastAPI
import joblib
from app.features import extract_features
import os

app = FastAPI()

# load trained model
model_path = os.path.join(os.path.dirname(__file__), "..", "model.pkl")
model = joblib.load(model_path)
@app.get("/")
def home():
    return {"message": "ML Churn Prediction API running"}

@app.post("/predict-risk")
def predict(data: dict):
    features = extract_features(data)
    pred = model.predict(features)[0]

    return {
        "risk": "HIGH" if pred == 1 else "LOW"
    }