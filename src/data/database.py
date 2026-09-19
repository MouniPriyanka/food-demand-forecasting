import os

import pandas as pd
from sqlalchemy import create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://forecast_user:forecast_password@localhost:5432/food_demand"
)

engine = create_engine(DATABASE_URL)


def load_sales():
    query = """
        SELECT *
        FROM sales
        ORDER BY item_id, store_id, date
    """

    sales = pd.read_sql(
        query,
        engine
    )

    sales["date"] = pd.to_datetime(
        sales["date"]
    )

    return sales