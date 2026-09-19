import pandas as pd
import joblib

from src.models.predict import forecast_demand


sales = pd.read_csv(
    "data/processed/food_sales_features.csv"
)

sales["date"] = pd.to_datetime(sales["date"])

model = joblib.load(
    "models/demand_model.pkl"
)


def test_forecast_demand():
    forecast_date, prediction = forecast_demand(
        "FOODS_1_001",
        "CA_1",
        sales,
        model
    )

    assert forecast_date == pd.Timestamp("2016-04-25")
    assert isinstance(prediction, float)