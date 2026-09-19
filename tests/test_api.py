from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_forecast_endpoint():
    response = client.get(
        "/forecast?product=FOODS_1_001&store=CA_1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product"] == "FOODS_1_001"
    assert data["store"] == "CA_1"
    assert data["forecast_date"] == "2016-04-25T00:00:00"
    assert isinstance(data["predicted_demand"], float)

def test_forecast_endpoint_invalid_product():
    response = client.get(
        "/forecast?product=FOODS_999_999&store=CA_99"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Product or store not found in the dataset."