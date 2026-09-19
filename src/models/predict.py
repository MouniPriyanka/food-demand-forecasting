import pandas as pd
import joblib

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

# Convert the date column to datetime
sales["date"] = pd.to_datetime(sales["date"])

print("Feature data loaded successfully.")
print("Rows:", len(sales))

# Select one existing observation
sample = sales.iloc[0]

# Get the features required by the model
features = [
    "day_of_week",
    "month",
    "lag_1",
    "lag_7",
    "rolling_mean_7"
]

# Create the input for the model
X = sample[features].to_frame().T

# Make a prediction
prediction = model.predict(X)[0]

print("\nSample observation:")
print(sample[["item_id", "store_id", "date", "units_sold"]])

print("\nPredicted demand:", prediction)

# Inspect the most recent observations
product = "FOODS_1_001"
store = "CA_1"

history = sales[
    (sales["item_id"] == product) &
    (sales["store_id"] == store)
].sort_values("date")

print("\nRecent history:")
print(
    history[
        ["date", "units_sold", "lag_1", "lag_7", "rolling_mean_7"]
    ].tail(10)
)

# Define the next day to forecast
forecast_date = history["date"].max() + pd.Timedelta(days=1)

# Get the latest historical values needed for the forecast
latest = history.iloc[-1]

lag_1 = latest["units_sold"]
lag_7 = history.iloc[-7]["units_sold"]
rolling_mean_7 = history["units_sold"].tail(7).mean()

# Create the features for the forecast date
forecast_features = pd.DataFrame({
    "day_of_week": [forecast_date.dayofweek],
    "month": [forecast_date.month],
    "lag_1": [lag_1],
    "lag_7": [lag_7],
    "rolling_mean_7": [rolling_mean_7]
})

# Predict demand
forecast = model.predict(forecast_features)[0]

print("\nForecast date:", forecast_date)
print("Product:", product)
print("Store:", store)
print("Predicted demand:", forecast)