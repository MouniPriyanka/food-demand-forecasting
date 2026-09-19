import pandas as pd
# Show all columns when displaying DataFrames
pd.set_option("display.max_columns", None)

# Load sales data
sales = pd.read_csv(
    "data/raw/sales_train_validation.csv")

# Load the calendar data
calendar = pd.read_csv(
    "data/raw/calendar.csv"
)


# Keep only food products from two stores
sales = sales[
    (sales["cat_id"] == "FOODS") &
    (sales["store_id"].isin(["CA_1", "CA_2"]))
]

# Keep the first 30 available food products
selected_items = (
    sales["item_id"]
    .drop_duplicates()
    .head(30)
)

sales = sales[sales["item_id"].isin(selected_items)]

#print("Selected products:")
#print(selected_items.tolist())

#print("\nSelected stores:")
#print(sales["store_id"].unique())

#print("\nNumber of sales rows:", len(sales))

# Keep the product and store identifiers
id_columns = [
    "id",
    "item_id",
    "dept_id",
    "cat_id",
    "store_id",
    "state_id"
]

# Identify the columns containing daily sales
sales_columns = [
    column for column in sales.columns
    if column.startswith("d_")
]

print("\nNumber of daily sales columns:", len(sales_columns))

# Convert daily sales from wide format to long format
sales_long = sales.melt(
    id_vars=id_columns,
    value_vars=sales_columns,
    var_name="d",
    value_name="units_sold"
)

# Keep only the day identifier and actual date
calendar = calendar[["d", "date"]]

# Add the actual date to each sales observation
sales_long = sales_long.merge(
    calendar,
    on="d",
    how="left"
)

#print("\nSales with dates:")
#print(sales_long.head())

#print("\nSales columns:")
#print(sales_long.columns.tolist())

# Save the processed dataset
sales_long.to_csv(
    "data/processed/food_sales.csv",
    index=False
)

print("\nProcessed dataset saved to data/processed/food_sales.csv")

"""
# Keep only food products
sales = sales[sales["cat_id"] == "FOODS"]

# Check how many food rows remain
#print("Number of food rows:", len(sales))

# Keep the product and store identifiers
id_columns = [
    "id",
    "item_id",
    "dept_id",
    "cat_id",
    "store_id",
    "state_id"
]

# Identify the columns containing daily sales
sales_columns = [column for column in sales.columns if column.startswith("d_")]
#print("Number of daily sales columns:", len(sales_columns))

# Convert daily sales from wide format to long format
sales_long = sales.melt(
    id_vars=id_columns,
    value_vars=sales_columns,
    var_name="d",
    value_name="units_sold"
)

# Check the reshaped data

# Check the number of rows after reshaping
#print("Long-format rows:", len(sales_long))

# Check the column names
#print("\nLong-format columns:")
#print(sales_long.columns.tolist())

# Show the first few rows
#print("\nLong-format sales:")
#print(sales_long.head())

# Load the calendar data
calendar = pd.read_csv(
    "data/raw/calendar.csv"
)
# Keep only the columns needed for the date mapping
calendar = calendar[["d", "date"]]

# Add the actual date to each sales observation
sales_long = sales_long.merge(
    calendar,
    on="d",
    how="left"
)

# Check that the dates were added correctly
print("\nSales with dates:")
print(sales_long.head())

print("\nSales columns:")
print(sales_long.columns.tolist())

print("\nFood products:")
print(
    sales_long[["item_id", "dept_id", "store_id"]]
    .drop_duplicates()
    .head(20)
)
"""