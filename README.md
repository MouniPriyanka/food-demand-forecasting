# Food Demand Forecasting Service

A small end-to-end machine learning application for forecasting food product demand from historical retail sales data.

The project uses historical sales data to predict future demand for individual products at specific stores. The goal is to demonstrate a practical machine learning workflow that can support inventory planning and potentially help reduce food waste caused by overstocking.

## Current Architecture

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
FastAPI prediction service
        ↓
Docker container
```

## Technologies

- Python
- Pandas
- scikit-learn
- FastAPI
- Uvicorn
- PostgreSQL *(planned)*
- Docker
- pytest
- Git

## Dataset

This project uses the **M5 Forecasting Accuracy** dataset, which contains historical Walmart retail sales data.

The dataset includes daily unit sales for products across multiple stores.

For the initial version of this project, the data was reduced to:

- Category: `FOODS`
- Stores: `CA_1` and `CA_2`
- Products: 30 food products
- Historical daily sales

The reduced dataset keeps the project small enough to work with locally while preserving a realistic forecasting problem.

## Data Processing

The raw M5 sales data is originally provided in a wide format, with one column for each day.

The preprocessing pipeline:

1. Selects the food category.
2. Selects the initial stores and products.
3. Converts the daily sales columns from wide format to long format.
4. Joins the sales data with the calendar data.
5. Saves the processed dataset for subsequent steps.

The resulting data contains product, store, date, and units sold information.

## Feature Engineering

The forecasting model uses historical demand and calendar information.

Current features:

- Day of week
- Month
- Previous day's demand (`lag_1`)
- Demand seven days earlier (`lag_7`)
- Seven-day rolling mean

The lag and rolling features are calculated using only previous observations to avoid target leakage.

## Model

A `HistGradientBoostingRegressor` from scikit-learn is currently used for demand prediction.

The data is split chronologically rather than randomly:

- Training period: before `2016-01-25`
- Test period: from `2016-01-25`

This prevents future observations from being used to train the model.

### Baseline

A simple previous-day demand prediction is used as the baseline.

Test MAE:

```text
1.657
```

### Machine Learning Model

The gradient boosting model achieves:

```text
Test MAE: 1.436
```

This represents approximately a **13.3% reduction in MAE compared with the baseline** on the selected test period.

The trained model is saved as:

```text
models/demand_model.pkl
```

## Prediction Service

The forecasting logic is separated from the API layer.

For example, a forecast can be generated for:

```text
Product: FOODS_1_001
Store: CA_1
```

The current prediction workflow:

```text
Product + Store
      ↓
Historical sales
      ↓
Forecast features
      ↓
Trained model
      ↓
Predicted demand
```

## FastAPI

The model is exposed through a REST API.

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

Tests can be run with:

```powershell
pytest
```

## Running Locally

Create and activate the virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the API:

```powershell
uvicorn src.api.main:app --reload
```

The API is then available at:

```text
http://127.0.0.1:8000
```

## Running with Docker

Build the Docker image:

```powershell
docker build -t food-demand-api .
```

Run the container:

```powershell
docker run -p 8000:8000 food-demand-api
```

The API can then be accessed at:

```text
http://127.0.0.1:8000
```

The Docker image packages the Python runtime, dependencies, application code, trained model, and processed dataset so that the application can run consistently outside the local development environment.

## Project Structure

```text
food-demand-forecasting/
│
├── src/
│   ├── data/
│   │   └── preprocessing.py
│   │
│   ├── features/
│   │   └── engineering.py
│   │
│   ├── models/
│   │   ├── train.py
│   │   └── predict.py
│   │
│   └── api/
│       └── main.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── tests/
│   ├── test_prediction.py
│   └── test_api.py
│
├── models/
│   └── demand_model.pkl
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Current Limitations

This is intentionally a small first version of the system.

Current limitations include:

- Only a subset of the M5 dataset is used.
- The API currently reads processed data from a CSV file.
- The model currently produces a one-day-ahead forecast.
- Model hyperparameters have not been extensively tuned.
- The application is currently designed for local execution.

## Planned Improvements

The next stages of the project will include:

- PostgreSQL for persistent structured data storage
- A database access layer between the API and database
- Docker Compose for running the API and database together
- Improved configuration and environment variables
- Additional model and feature experiments
- More comprehensive tests
- Improved documentation
- GitHub repository setup
- Deployment of the service