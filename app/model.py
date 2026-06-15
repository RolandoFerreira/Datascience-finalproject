import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from scraper import load_dataset
from features import generate_features, label_churn, FEATURES

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")

def train_and_save(save_path=None):
    if save_path is None:
        save_path = MODEL_PATH

    data = load_dataset()
    df = pd.DataFrame(data)
    df = generate_features(df)
    df = label_churn(df)

    print("Churn distribution:\n", df["churned"].value_counts())

    X = df[FEATURES]
    y = df["churned"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X, y)
    joblib.dump(model, save_path)
    print(f"Model saved to {save_path}")
    return model

def load_model(path=None):
    if path is None:
        path = MODEL_PATH
    return joblib.load(path)

if __name__ == "__main__":
    train_and_save()