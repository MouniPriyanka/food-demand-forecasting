import os

import pandas as pd
from sqlalchemy import create_engine, text


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://forecast_user:forecast_password@localhost:5432/food_demand"
)

engine = create_engine(DATABASE_URL)


def seed_database():
    sales = pd.read_csv(
        "data/processed/food_sales_features.csv"
    )

    sales["date"] = pd.to_datetime(
        sales["date"]
    )

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS sales (
                    id TEXT,
                    item_id TEXT,
                    dept_id TEXT,
                    cat_id TEXT,
                    store_id TEXT,
                    state_id TEXT,
                    d TEXT,
                    units_sold INTEGER,
                    date DATE,
                    day_of_week INTEGER,
                    month INTEGER,
                    lag_1 DOUBLE PRECISION,
                    lag_7 DOUBLE PRECISION,
                    rolling_mean_7 DOUBLE PRECISION
                )
                """
            )
        )

        existing_rows = connection.execute(
            text("SELECT COUNT(*) FROM sales")
        ).scalar()

    if existing_rows == 0:
        sales.to_sql(
            "sales",
            engine,
            if_exists="append",
            index=False
        )

        print(f"Inserted {len(sales)} rows into PostgreSQL.")
    else:
        print(
            f"Database already contains {existing_rows} rows. "
            "Skipping seed."
        )


if __name__ == "__main__":
    seed_database()
    