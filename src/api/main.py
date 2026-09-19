from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Food Demand Forecasting API is running"}