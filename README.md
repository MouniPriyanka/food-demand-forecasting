# Food Demand Forecasting Service

A small end-to-end machine learning application for forecasting food product demand from historical retail sales data.

The project uses historical Walmart retail sales data to predict next-day demand for individual products at specific stores. The goal is to demonstrate a practical machine learning workflow that can support inventory planning and provide a demand-based signal for reducing potential food waste caused by overstocking.

## Architecture

```text
M5 retail sales data
        ↓
Data preprocessing
        ↓
Feature engineering
        ↓
Historical demand features
        ↓
Machine learning model
        ↓
Trained model
        ↓
PostgreSQL
        ↓
FastAPI prediction service
        ↓
Docker Compose
        ↓
Automated tests + GitHub Actions CI
```

The application separates data preparation, model training, prediction logic, database access, and the API layer.

## Technologies

- Python 3.13
- Pandas
- scikit-learn
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- psycopg2
- Docker
- Docker Compose
- pytest
- GitHub Actions
- Git

## Dataset

This project uses the **M5 Forecasting Accuracy** dataset, which contains historical Walmart retail sales data.

The dataset includes daily unit sales for products across multiple stores, along with calendar and pricing information.

For the initial version of this project, the data was reduced to:

- Category: `FOODS`
- Stores: `CA_1` and `CA_2`
- Products: 30 food products
- Historical daily sales

The reduced dataset keeps the project small enough to work with locally while preserving a realistic retail demand forecasting problem.

The raw M5 dataset is not committed to the repository because of its size.

## Data Processing

The raw M5 sales data is originally provided in a wide format, with one column for each day.

The preprocessing pipeline:

1. Selects the `FOODS` category.
2. Selects stores `CA_1` and `CA_2`.
3. Selects 30 food products.
4. Converts daily sales columns from wide format to long format.
5. Joins the sales data with the M5 calendar data.
6. Produces a structured daily sales dataset.

The resulting data contains product, store, date, and units-sold information.

## Feature Engineering

The forecasting model uses recent demand history and calendar information.

Current features:

- Day of week
- Month
- Previous day's demand (`lag_1`)
- Demand seven days earlier (`lag_7`)
- Seven-day rolling mean (`rolling_mean_7`)

The lag and rolling features are calculated using previous observations only to avoid target leakage.

The final feature set contains:

```text
day_of_week
month
lag_1
lag_7
rolling_mean_7
```

## Model

A `HistGradientBoostingRegressor` from scikit-learn is used for demand prediction.

The data is split chronologically rather than randomly:

- Training period: before `2016-01-25`
- Test period: `2016-01-25` onward

This prevents future observations from being used to train the model.

### Baseline

A simple previous-day demand prediction is used as the baseline.

```text
Test MAE: 1.657 units
```

### Machine Learning Model

The gradient boosting model achieves:

```text
Test MAE: 1.436 units
```

This represents approximately a **13.3% reduction in MAE compared with the baseline** on the same chronological test period.

The trained model is saved as:

```text
models/demand_model.pkl
```

## Evaluation

The model was evaluated using a chronological holdout period beginning on `2016-01-25`.

| Model | Test MAE |
|---|---:|
| Previous-day baseline | 1.657 |
| HistGradientBoostingRegressor | 1.436 |

The model reduces MAE by approximately **13.3%** compared with the baseline.

Predictions remain continuous during model evaluation rather than being rounded to whole units. This preserves the accuracy of the regression metric.

For a simple inventory-oriented interpretation, predicted demand can be rounded up to the nearest whole unit. This is treated as a **demand-based stocking signal**, not a complete inventory optimization recommendation, because the current system does not model current inventory, lead times, safety stock, or ordering costs.

### Evaluation findings

The model captures general product and store demand levels, but it can underestimate sudden demand spikes and overestimate sudden drops.

The current feature set uses recent demand history and basic calendar features. It does not yet incorporate factors such as price changes, promotions, or events, which may help explain some sudden changes in demand.

Demand also varies substantially between products and stores. This demonstrates the importance of product- and store-specific forecasting rather than relying on a single demand estimate for all products.

The project includes visualizations for:

- Actual versus predicted demand
- Product-level predicted demand
- Store-level demand comparisons
- Demand-based stocking signals

## Prediction Service

The forecasting logic is separated from the API layer.

For example:

```text
Product: FOODS_1_001
Store: CA_1
```

The prediction workflow is:

```text
Product + Store
        ↓
Historical sales from PostgreSQL
        ↓
Forecast features
        ↓
Trained model
        ↓
Predicted next-day demand
```

The current prediction example produces:

```text
Forecast date: 2016-04-25
Product: FOODS_1_001
Store: CA_1
Predicted demand: 1.0307
```

## PostgreSQL

PostgreSQL is used as the application's structured data store.

The database layer is implemented in:

```text
src/data/database.py
```

The application retrieves historical sales through the database rather than reading the production dataset directly from a CSV file.

A database seed service is provided for Docker Compose:

```text
src/data/seed_database.py
```

The seed process creates the required `sales` table and loads the processed sales data into PostgreSQL.

## FastAPI

The trained model is exposed through a REST API.

### Health endpoint

```http
GET /
```

Response:

```json
{
  "message": "Food Demand Forecasting API is running"
}
```

### Forecast endpoint

```http
GET /forecast?product=FOODS_1_001&store=CA_1
```

Example response:

```json
{
  "product": "FOODS_1_001",
  "store": "CA_1",
  "forecast_date": "2016-04-25T00:00:00",
  "predicted_demand": 1.0307256704334413
}
```

If the requested product or store does not exist, the API returns HTTP `404`.

## Docker Compose

The application can be run as a multi-container system using Docker Compose.

The Compose architecture contains three services:

```text
PostgreSQL
    ↓
Database seed
    ↓
FastAPI
```

The database health check ensures PostgreSQL is ready before the seed service starts.

The API starts only after the database has been successfully seeded.

Start the complete application with:

```powershell
docker compose up --build
```

The API is then available at:

```text
http://127.0.0.1:8000
```

Example:

```text
http://127.0.0.1:8000/forecast?product=FOODS_1_001&store=CA_1
```

The Docker setup packages the application runtime, dependencies, trained model, processed data, PostgreSQL database, and database initialization process into a reproducible local environment.

## Testing

The project includes automated tests for:

- Demand forecasting logic
- Invalid product/store handling
- FastAPI forecast endpoint
- FastAPI error handling

The current test suite contains four tests.

```text
4 passed
```

Run the tests locally with:

```powershell
pytest
```

For CI, a lightweight synthetic dataset is generated automatically rather than committing the large M5 dataset to the repository.

## Continuous Integration

GitHub Actions is used to automatically validate the project on repository changes.

The CI pipeline:

1. Checks out the repository.
2. Sets up Python 3.13.
3. Installs project dependencies.
4. Creates a lightweight CI test dataset.
5. Starts PostgreSQL.
6. Seeds the database.
7. Runs the automated test suite.

The workflow is defined in:

```text
.github/workflows/ci.yml
```

The current CI pipeline passes successfully.

## Running Locally

### Option 1: Docker Compose

The recommended way to run the complete application is Docker Compose:

```powershell
docker compose up --build
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Option 2: Python development environment

Create and activate the virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

For local development, PostgreSQL must be running and the database must contain the processed sales data.

The API can then be started with:

```powershell
uvicorn src.api.main:app --reload
```

## Project Structure

```text
food-demand-forecasting/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── src/
│   ├── data/
│   │   ├── preprocessing.py
│   │   ├── database.py
│   │   └── seed_database.py
│   │
│   ├── features/
│   │   └── engineering.py
│   │
│   ├── models/
│   │   ├── train.py
│   │   └── predict.py
│   │
│   ├── api/
│   │   └── main.py
│   │
│   └── evaluation.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── tests/
│   ├── create_test_data.py
│   ├── test_prediction.py
│   └── test_api.py
│
├── models/
│   └── demand_model.pkl
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Current Limitations

This is intentionally a small first version of the system.

Current limitations include:

- Only a subset of the M5 dataset is used.
- Only 30 products across two stores are included in the initial modeling scope.
- The model produces a one-day-ahead forecast.
- The current feature set does not include price, promotions, or event information.
- Model hyperparameters have not been extensively tuned.
- The system provides a demand forecast rather than a full inventory optimization solution.
- Inventory levels, lead times, safety stock, and ordering costs are not currently modeled.
- The application has been validated locally and through CI, but is not currently deployed as a public production service.

## Potential Future Improvements

Possible future extensions include:

- Incorporating price, promotions, and event features
- Comparing additional forecasting models
- Hyperparameter optimization
- Multi-day forecasting
- Forecast uncertainty and prediction intervals
- More comprehensive database schemas
- Inventory-aware replenishment recommendations
- Monitoring model performance over time
- Cloud deployment
- Production authentication and configuration management

## Key Takeaways

This project demonstrates an end-to-end machine learning workflow rather than only a model-training experiment.

It combines:

- Real-world retail sales data
- Data preprocessing
- Time-series feature engineering
- Chronological model evaluation
- Baseline comparison
- Machine learning regression
- PostgreSQL data storage
- FastAPI model serving
- Docker containerization
- Docker Compose orchestration
- Automated testing
- GitHub Actions CI

The final system achieved a **13.3% reduction in test MAE compared with a previous-day demand baseline** while remaining small enough to develop and run locally.