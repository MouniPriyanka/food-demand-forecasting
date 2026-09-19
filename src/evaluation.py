import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import math


sales = pd.read_csv(
    "data/processed/food_sales_features.csv"
)

sales["date"] = pd.to_datetime(sales["date"])

model = joblib.load(
    "models/demand_model.pkl"
)

features = [
    "day_of_week",
    "month",
    "lag_1",
    "lag_7",
    "rolling_mean_7"
]

test_start = pd.Timestamp("2016-01-25")

test = sales[
    sales["date"] >= test_start
].copy()

predictions = model.predict(
    test[features]
)

test["prediction"] = predictions

test["absolute_error"] = (
    test["units_sold"] - test["prediction"]
).abs()

test["recommended_units"] = (
    test["prediction"]
    .apply(math.ceil)
)

mae = mean_absolute_error(
    test["units_sold"],
    test["prediction"]
)

print("Test MAE:", mae)

print("\nSample evaluation results:")

print(
    test[
        [
            "date",
            "item_id",
            "store_id",
            "units_sold",
            "prediction",
            "absolute_error",
            "recommended_units"
        ]
    ].head(10)
)

test[
    [
        "date",
        "item_id",
        "store_id",
        "units_sold",
        "prediction",
        "absolute_error",
        "recommended_units"
    ]
].to_csv(
    "data/processed/model_evaluation.csv",
    index=False
)

print(
    "\nEvaluation results saved to "
    "data/processed/model_evaluation.csv"
)


sample = test[
    (test["item_id"] == "FOODS_1_001") &
    (test["store_id"] == "CA_1")
].copy()

plt.figure(figsize=(12, 6))

plt.plot(
    sample["date"],
    sample["units_sold"],
    label="Actual demand"
)

plt.plot(
    sample["date"],
    sample["prediction"],
    label="Predicted demand"
)

plt.xlabel("Date")
plt.ylabel("Units sold")
plt.title(
    "Actual vs Predicted Demand - FOODS_1_001, CA_1"
)

plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "data/processed/actual_vs_predicted.png"
)

plt.show()

product_summary = (
    test
    .groupby(["item_id", "store_id"])
    .agg(
        average_predicted_demand=("prediction", "mean"),
        peak_predicted_demand=("prediction", "max"),
        recommended_stock=("recommended_units", "max")
    )
    .reset_index()
)

product_summary = product_summary.sort_values(
    "average_predicted_demand",
    ascending=False
)

print("\nTop 10 products by average predicted demand:")
print(
    product_summary.head(10).to_string(index=False)
)
top_products = product_summary.head(10).copy()

top_products["product_store"] = (
    top_products["item_id"]
    + " · "
    + top_products["store_id"]
)

plt.figure(figsize=(12, 6))

plt.barh(
    top_products["product_store"],
    top_products["recommended_stock"]
)

plt.xlabel("Recommended stock (units)")
plt.ylabel("Product / store")
plt.title(
    "Top Product/Store Combinations by Recommended Stock"
)

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "data/processed/top_recommended_stock.png"
)

plt.show()

for store in ["CA_1", "CA_2"]:

    store_products = product_summary[
        product_summary["store_id"] == store
    ].sort_values("item_id")

    plt.figure(figsize=(12, 8))

    plt.barh(
        store_products["item_id"],
        store_products["average_predicted_demand"]
    )

    plt.xlabel("Average predicted daily demand (units)")
    plt.ylabel("Product")
    plt.title(
        f"Average Predicted Demand - {store}"
    )

    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.savefig(
        f"data/processed/average_predicted_demand_{store}.png"
    )

    plt.show()