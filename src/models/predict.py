import pandas as pd
import joblib

def create_forecast_features(history, forecast_date):
    latest = history.iloc[-1]

    lag_1 = latest["units_sold"]
    lag_7 = history.iloc[-7]["units_sold"]
    rolling_mean_7 = history["units_sold"].tail(7).mean()

    return pd.DataFrame({
        "day_of_week": [forecast_date.dayofweek],
        "month": [forecast_date.month],
        "lag_1": [lag_1],
        "lag_7": [lag_7],
        "rolling_mean_7": [rolling_mean_7]
    })

def forecast_demand(product, store, sales, model):
    history = sales[
        (sales["item_id"] == product) &
        (sales["store_id"] == store)
    ].sort_values("date")

    if history.empty:
        raise ValueError(
            "Product or store not found in the dataset."
        )

    forecast_date = history["date"].max() + pd.Timedelta(days=1)

    forecast_features = create_forecast_features(
        history,
        forecast_date
    )

    forecast = model.predict(forecast_features)[0]

    return forecast_date, forecast

def main():
    # Load the trained model
    model = joblib.load(
        "models/demand_model.pkl"
    )

    print("Model loaded successfully.")
    print("Model type:", type(model).__name__)

    # Load the feature-engineered sales data
    sales = pd.read_csv(
        "data/processed/food_sales_features.csv"
    )

    sales["date"] = pd.to_datetime(sales["date"])

    print("Feature data loaded successfully.")
    print("Rows:", len(sales))

    product = "FOODS_1_001"
    store = "CA_1"

    forecast_date, forecast = forecast_demand(
        product,
        store,
        sales,
        model
    )

    print("\nForecast date:", forecast_date)
    print("Product:", product)
    print("Store:", store)
    print("Predicted demand:", forecast)


if __name__ == "__main__":
    main()