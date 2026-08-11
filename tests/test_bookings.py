from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_create_booking() -> None:
    response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Dana",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-08-15T17:00:00",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_name"] == "Dana"
    assert data["service_id"] == "6a779ed59b6b145fcfe108ab"
    assert "id" in data