import pandas as pd
import joblib
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

# Load the feature-engineered dataset
sales = pd.read_csv(
    "data/processed/food_sales_features.csv"
)

# Convert the date column to datetime
sales["date"] = pd.to_datetime(sales["date"])

# Define the features used by the model
features = [
    "day_of_week",
    "month",
    "lag_1",
    "lag_7",
    "rolling_mean_7"
]

# Define the target we want to predict
target = "units_sold"

# Define the start of the test period
test_start = pd.Timestamp("2016-01-25")

# Split the data chronologically
train = sales[sales["date"] < test_start].copy()
test = sales[sales["date"] >= test_start].copy()

# Prepare training data
X_train = train[features]
y_train = train[target]

# Prepare test data
X_test = test[features]
y_test = test[target]

print("Training rows:", len(X_train))
print("Test rows:", len(X_test))

# Create the model
model = HistGradientBoostingRegressor(
    max_iter=100,
    learning_rate=0.1,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Make predictions on unseen test data
predictions = model.predict(X_test)

# Calculate test MAE
model_mae = mean_absolute_error(
    y_test,
    predictions
)

print("\nModel Test MAE:", model_mae)

# Show a few predictions
results = test[
    ["item_id", "store_id", "date", "units_sold"]
].copy()

results["prediction"] = predictions

print("\nSample predictions:")
print(results.head(10))

# Save the trained model
joblib.dump(
    model,
    "models/demand_model.pkl"
)

print("\nModel saved to models/demand_model.pkl")