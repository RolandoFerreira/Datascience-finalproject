from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from model import load_model
from features import FEATURES

app = FastAPI(title="Churn Predictor API - DummyJSON E-commerce")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")


class UserFeatures(BaseModel):
    spend_per_cart:       float
    items_per_cart:       float
    quantity_per_item:    float
    avg_items_per_cart:   float
    cart_frequency_score: float
    engagement_trend:     float
    is_low_spender:       int
    is_one_time_buyer:    int
    is_senior:            int
    is_young:             int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/features")
def features():
    return {"expected_fields": FEATURES}

@app.post("/predict")
def predict(user: UserFeatures):
    X = [[
        user.spend_per_cart,
        user.items_per_cart,
        user.quantity_per_item,
        user.avg_items_per_cart,
        user.cart_frequency_score,
        user.engagement_trend,
        user.is_low_spender,
        user.is_one_time_buyer,
        user.is_senior,
        user.is_young,
    ]]
    prob = model.predict_proba(X)[0][1]
    return {
        "churned": bool(prob >= 0.5),
        "churn_probability": round(float(prob), 4)
    }