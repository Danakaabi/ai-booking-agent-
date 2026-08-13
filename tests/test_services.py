from fastapi.testclient import TestClient
from database.repositories.services import (
    get_active_services_by_id,
    get_service_by_id,
)
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



def test_get_service_by_id() -> None:
    service = get_service_by_id("6a779ed59b6b145fcfe108ab")

    assert service is not None
    assert service["id"] == "6a779ed59b6b145fcfe108ab"
    assert service["name"] == "Haircut"
    assert service["duration_minutes"] == 60
    assert service["active"] is True


def test_get_active_services_by_id() -> None:
    services = get_active_services_by_id()

    service_id = "6a779ed59b6b145fcfe108ab"

    assert service_id in services
    assert services[service_id]["name"] == "Haircut"
    assert services[service_id]["duration_minutes"] == 60
    assert services[service_id]["active"] is True