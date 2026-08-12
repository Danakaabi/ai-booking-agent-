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


def test_get_bookings() -> None:
    response = client.get("/bookings")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]


def test_get_booking_by_id() -> None:
    # First, create a booking to ensure there is at least one booking in the database
    create_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Dana",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-08-15T17:00:00",
        },
    )
    assert create_response.status_code == 200
    created_booking = create_response.json()
    booking_id = created_booking["id"]

    # Now, retrieve the booking by its ID
    get_response = client.get(f"/bookings/{booking_id}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["id"] == booking_id
    assert data["customer_name"] == "Dana"


def test_get_booking_by_id_not_found() -> None:
    response = client.get(
        "/bookings/000000000000000000000000"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Booking not found"