FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY models ./models
COPY data/processed ./data/processed
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]