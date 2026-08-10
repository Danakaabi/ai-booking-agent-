from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_get_services() -> None:
    response = client.get("/services")

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Haircut",
            "duration_minutes": 60,
            "price": 85.0,
            "active": True,
        }
    ]