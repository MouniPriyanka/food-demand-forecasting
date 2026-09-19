import pandas as pd

# Inspect the sales data



sales = pd.read_csv(
    "data/raw/sales_train_validation.csv",
    nrows=5
)

#print(sales.head())
#print("\nColumns:")
#print(sales.columns.tolist()) 



# Inspect the calendar data

calendar = pd.read_csv(
    "data/raw/calendar.csv",
    nrows=5
)

#print("\nCalendar:")
#print(calendar)

#print("\nCalendar columns:")
#print(calendar.columns.tolist())

# Inspect the price data

prices = pd.read_csv(
    "data/raw/sell_prices.csv",
    nrows=5
)

#print("\nPrices:")
#print(prices)

#print("\nPrice columns:")
#print(prices.columns.tolist())


# Inspect sales dimensions


sales_full = pd.read_csv(
    "data/raw/sales_train_validation.csv"
)

print("\nNumber of sales rows:")
print(len(sales_full))

print("\nCategories:")
print(sales_full["cat_id"].value_counts())

print("\nNumber of stores:")
print(sales_full["store_id"].nunique())

print("\nNumber of items:")
print(sales_full["item_id"].nunique())

# Inspect stores

print("\nStores:")
print(sales_full["store_id"].value_counts())