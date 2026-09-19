from fastapi import FastAPI
import pandas as pd
import joblib

from src.models.predict import forecast_demand

app = FastAPI()

model = joblib.load(
    "models/demand_model.pkl"
)

sales = pd.read_csv(
    "data/processed/food_sales_features.csv"
)

sales["date"] = pd.to_datetime(sales["date"])

@app.get("/")
def root():
    return {"message": "Food Demand Forecasting API is running"}


@app.get("/forecast")
def forecast(product: str, store: str):
    forecast_date, predicted_demand = forecast_demand(
        product,
        store,
        sales,
        model
    )

    return {
        "product": product,
        "store": store,
        "forecast_date": forecast_date,
        "predicted_demand": predicted_demand
    }