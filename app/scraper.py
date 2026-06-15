import requests
import pandas as pd
import json
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fetch_users(limit=100):
    users = []
    skip = 0
    while skip < limit:
        r = requests.get(f"https://dummyjson.com/users?limit=30&skip={skip}")
        batch = r.json().get("users", [])
        if not batch:
            break
        users.extend(batch)
        skip += 30
        time.sleep(0.3)
    return users

def fetch_carts():
    r = requests.get("https://dummyjson.com/carts?limit=0")
    return r.json().get("carts", [])

def build_dataset(save_path=None):
    if save_path is None:
        save_path = os.path.join(BASE_DIR, "data", "raw", "users_carts.json")

    users = fetch_users(limit=100)
    carts = fetch_carts()

    cart_map = {}
    for cart in carts:
        uid = cart["userId"]
        if uid not in cart_map:
            cart_map[uid] = []
        cart_map[uid].append(cart)

    records = []
    for u in users:
        uid = u["id"]
        user_carts = cart_map.get(uid, [])
        records.append({
            "user_id":        uid,
            "age":            u.get("age", 0),
            "gender":         u.get("gender", ""),
            "num_carts":      len(user_carts),
            "total_spent":    sum(c.get("total", 0) for c in user_carts),
            "total_products": sum(c.get("totalProducts", 0) for c in user_carts),
            "total_quantity": sum(c.get("totalQuantity", 0) for c in user_carts),
        })

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(records, f)

    print(f"Saved {len(records)} user records to {save_path}")
    return records

def load_dataset(path=None):
    if path is None:
        path = os.path.join(BASE_DIR, "data", "raw", "users_carts.json")
    with open(path) as f:
        return json.load(f)

if __name__ == "__main__":
    build_dataset()