import pandas as pd

# Load the processed sales data
sales = pd.read_csv(
    "data/processed/food_sales.csv"
)

# Convert the date column from text to datetime
sales["date"] = pd.to_datetime(sales["date"])

# Create the day-of-week feature
sales["day_of_week"] = sales["date"].dt.dayofweek

# Create the month feature
sales["month"] = sales["date"].dt.month

# Sort observations by product, store, and date
sales = sales.sort_values(
    ["item_id", "store_id", "date"]
)

# Create the previous day's demand for each product and store
sales["lag_1"] = (
    sales
    .groupby(["item_id", "store_id"])["units_sold"]
    .shift(1)
)

# Create the demand from seven days earlier
sales["lag_7"] = (
    sales
    .groupby(["item_id", "store_id"])["units_sold"]
    .shift(7)
)

# Create the average demand from the previous 7 days
sales["rolling_mean_7"] = (
    sales
    .groupby(["item_id", "store_id"])["units_sold"]
    .shift(1)
    .rolling(7)
    .mean()
)

# Remove rows without enough historical demand
sales = sales.dropna(
    subset=["lag_1", "lag_7", "rolling_mean_7"]
)

print("\nRows after removing missing history:", len(sales))

# Save the feature-engineered dataset
sales.to_csv(
    "data/processed/food_sales_features.csv",
    index=False
)

print("\nFeature-engineered dataset saved.")