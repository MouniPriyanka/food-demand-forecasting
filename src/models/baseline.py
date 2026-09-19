import pandas as pd

# Load the feature-engineered dataset
sales = pd.read_csv(
    "data/processed/food_sales_features.csv"
)

# Convert the date column from text to datetime
sales["date"] = pd.to_datetime(sales["date"])

print("Rows loaded:", len(sales))

# Use yesterday's demand as the baseline prediction
sales["baseline_prediction"] = sales["lag_1"]

# Check the date range
print("\nFirst date:", sales["date"].min())
print("Last date:", sales["date"].max())

# Define the start of the test period
test_start = pd.Timestamp("2016-01-25")

# Split the data chronologically
train = sales[sales["date"] < test_start].copy()
test = sales[sales["date"] >= test_start].copy()

print("\nTraining rows:", len(train))
print("Test rows:", len(test))

print("\nTraining period:")
print(train["date"].min(), "to", train["date"].max())

print("\nTest period:")
print(test["date"].min(), "to", test["date"].max())

# Calculate baseline MAE on the test period
baseline_mae = (
    test["units_sold"] - test["baseline_prediction"]
).abs().mean()

print("\nTest baseline MAE:", baseline_mae)
