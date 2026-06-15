import pandas as pd
import numpy as np

FEATURES = [
    "spend_per_cart",
    "items_per_cart",
    "quantity_per_item",
    "avg_items_per_cart",
    "cart_frequency_score",
    "engagement_trend",
    "is_low_spender",
    "is_one_time_buyer",
    "is_senior",
    "is_young",
]

def generate_features(df):
    df["spend_per_cart"]     = df["total_spent"]   / (df["num_carts"] + 1)
    df["items_per_cart"]     = df["total_products"] / (df["num_carts"] + 1)
    df["quantity_per_item"]  = df["total_quantity"] / (df["total_products"] + 1)
    df["avg_items_per_cart"] = df["total_quantity"] / (df["num_carts"] + 1)
    df["cart_frequency_score"] = df["num_carts"] / (df["age"] / 10)
    df["engagement_trend"] = df["total_quantity"] / (df["total_products"] + 1)
    df["is_low_spender"]    = (df["total_spent"] < df["total_spent"].quantile(0.30)).astype(int)
    df["is_one_time_buyer"] = (df["num_carts"] <= 1).astype(int)
    df["is_senior"] = (df["age"] >= 55).astype(int)
    df["is_young"]  = (df["age"] <= 25).astype(int)

    return df

def label_churn(df):
    low_spend_threshold = df["total_spent"].quantile(0.30)
    df["churned"] = (
        (df["num_carts"] <= 1) & (df["total_spent"] < low_spend_threshold)
    ).astype(int)
    return df