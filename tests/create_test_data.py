from pathlib import Path

import pandas as pd


dates = pd.date_range(
    "2016-04-17",
    "2016-04-24",
    freq="D"
)

units = [1, 2, 1, 3, 2, 2, 1, 2]

rows = []

for index, (date, units_sold) in enumerate(zip(dates, units), start=1):
    rows.append(
        {
            "id": f"FOODS_1_001_CA_1",
            "item_id": "FOODS_1_001",
            "dept_id": "FOODS_1",
            "cat_id": "FOODS",
            "store_id": "CA_1",
            "state_id": "CA",
            "d": f"d_{index}",
            "units_sold": units_sold,
            "date": date,
            "day_of_week": date.dayofweek,
            "month": date.month,
            "lag_1": 0,
            "lag_7": 0,
            "rolling_mean_7": 0,
        }
    )


sales = pd.DataFrame(rows)

output_path = Path(
    "data/processed/food_sales_features.csv"
)

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

sales.to_csv(
    output_path,
    index=False
)

print(
    f"Created CI test dataset with {len(sales)} rows."
)