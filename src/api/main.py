from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib

from src.models.predict import forecast_demand
from src.data.database import load_sales

app = FastAPI()

model = joblib.load(
    "models/demand_model.pkl"
)

sales = load_sales()

@app.get("/")
def root():
    return {"message": "Food Demand Forecasting API is running"}


@app.get("/forecast")
def forecast(product: str, store: str):
    try:
        forecast_date, predicted_demand = forecast_demand(
            product,
            store,
            sales,
            model
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    return {
        "product": product,
        "store": store,
        "forecast_date": forecast_date,
        "predicted_demand": predicted_demand
    }