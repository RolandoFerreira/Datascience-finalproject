# Customer Churn Predictor

A Dockerized FastAPI application that predicts customer churn from e-commerce behavior data fetched from [DummyJSON](https://dummyjson.com).

Built for the Introduction to Data Science final project — Prof. Yrupe Fresco.

---

## Run the app

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

Interactive docs (Swagger UI): `http://localhost:8000/docs`

---

## Endpoints

### `GET /health`
Returns `{"status": "ok"}` — used by Docker to confirm the container is running.

### `GET /features`
Returns the list of input fields expected by `/predict`.

### `POST /predict`
Accepts a JSON body with user features and returns a churn prediction.

**Request:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "spend_per_cart": 45.0,
    "items_per_cart": 2.5,
    "quantity_per_item": 1.2,
    "avg_items_per_cart": 2.5,
    "total_products": 5,
    "total_quantity": 6,
    "is_low_spender": 0,
    "is_one_time_buyer": 0
  }'
```

**Response:**
```json
{
  "churned": false,
  "churn_probability": 0.213
}
```

---

## Project structure
churn-predictor/

├── app/

│   ├── main.py        # FastAPI app and endpoints

│   ├── model.py       # Model training and loading

│   ├── features.py    # Feature generation and churn labeling

│   └── scraper.py     # DummyJSON data fetcher

├── notebooks/

│   └── exploration.ipynb   # EDA, feature selection (all 4 methods), retention analysis

├── data/

│   └── raw/

│       └── users_carts.json

├── Dockerfile

├── docker-compose.yml

└── requirements.txt
---

## Data source

Data is fetched from [DummyJSON](https://dummyjson.com) — a free, no-auth e-commerce API. Users and their cart data are joined to simulate purchase behavior. No API key required.

To re-fetch data and retrain the model locally (outside Docker):

```bash
cd app
python scraper.py   # fetches data to data/raw/users_carts.json
python model.py     # retrains and saves model.pkl
```
