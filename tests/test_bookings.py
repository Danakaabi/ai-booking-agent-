from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from ai_core.availability import has_booking_conflict
from ai_core.booking_engine import booking_has_conflict
from api.main import app
from api.schemas.booking import BookingCreate
from database.repositories.bookings import (
    bookings_collection,
    get_confirmed_bookings,
)
from database.repositories.services import get_active_services_by_id


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_test_bookings():
    """
    Remove test bookings before and after every test.

    This keeps tests isolated and prevents previous test runs
    from causing false 409 Conflict responses.
    """

    test_customer_names = [
        "Dana",
        "Dana Updated",
        "Cancel Test",
        "Conflict Test",
        "Conflict Integration Test",
        "Existing Booking",
        "New Booking",
        "First Booking",
        "Conflicting Booking",
        "Cancelled Slot Test",
        "Replacement Booking",
    ]

    bookings_collection.delete_many(
        {
            "customer_name": {
                "$in": test_customer_names,
            }
        }
    )

    yield

    bookings_collection.delete_many(
        {
            "customer_name": {
                "$in": test_customer_names,
            }
        }
    )


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
    create_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Dana",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-08-16T10:00:00",
        },
    )

    assert create_response.status_code == 200

    response = client.get("/bookings")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]


def test_get_booking_by_id() -> None:
    create_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Dana",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-08-17T10:00:00",
        },
    )

    assert create_response.status_code == 200

    created_booking = create_response.json()
    booking_id = created_booking["id"]

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


def test_update_booking() -> None:
    create_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Dana",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-08-18T10:00:00",
        },
    )

    assert create_response.status_code == 200

    booking_id = create_response.json()["id"]

    response = client.patch(
        f"/bookings/{booking_id}",
        json={
            "customer_name": "Dana Updated",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == booking_id
    assert data["customer_name"] == "Dana Updated"
    assert data["customer_phone"] == "0500000000"


def test_update_booking_not_found() -> None:
    response = client.patch(
        "/bookings/000000000000000000000000",
        json={
            "customer_name": "Test Name",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Booking not found"


def test_cancel_booking() -> None:
    create_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Cancel Test",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-08-25T17:00:00",
        },
    )

    assert create_response.status_code == 200

    booking_id = create_response.json()["id"]

    response = client.patch(
        f"/bookings/{booking_id}/cancel"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == booking_id
    assert data["status"] == "cancelled"


def test_cancel_booking_not_found() -> None:
    response = client.patch(
        "/bookings/000000000000000000000000/cancel"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


def test_get_confirmed_bookings_excludes_cancelled() -> None:
    create_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Conflict Test",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-08-30T10:00:00",
        },
    )

    assert create_response.status_code == 200

    booking_id = create_response.json()["id"]

    cancel_response = client.patch(
        f"/bookings/{booking_id}/cancel"
    )

    assert cancel_response.status_code == 200

    confirmed_bookings = get_confirmed_bookings()

    confirmed_ids = [
        booking["id"]
        for booking in confirmed_bookings
    ]

    assert booking_id not in confirmed_ids

    assert all(
        booking["status"] == "confirmed"
        for booking in confirmed_bookings
    )


def test_confirmed_booking_causes_conflict() -> None:
    create_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Conflict Integration Test",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-09-01T10:00:00",
        },
    )

    assert create_response.status_code == 200

    confirmed_bookings = get_confirmed_bookings()
    services_by_id = get_active_services_by_id()

    result = has_booking_conflict(
        new_start=datetime(2026, 9, 1, 10, 30),
        new_end=datetime(2026, 9, 1, 11, 30),
        existing_bookings=confirmed_bookings,
        services_by_id=services_by_id,
    )

    assert result is True


def test_booking_engine_detects_conflict() -> None:
    create_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Existing Booking",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-09-05T10:00:00",
        },
    )

    assert create_response.status_code == 200

    requested_booking = BookingCreate(
        service_id="6a779ed59b6b145fcfe108ab",
        customer_name="New Booking",
        customer_phone="0511111111",
        booking_datetime=datetime(2026, 9, 5, 10, 30),
    )

    result = booking_has_conflict(
        requested_booking
    )

    assert result is True


def test_create_booking_rejects_conflict() -> None:
    first_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "First Booking",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-09-10T10:00:00",
        },
    )

    assert first_response.status_code == 200

    conflict_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Conflicting Booking",
            "customer_phone": "0511111111",
            "booking_datetime": "2026-09-10T10:30:00",
        },
    )

    assert conflict_response.status_code == 409

    assert conflict_response.json()["detail"] == (
        "Booking time conflicts with an existing booking"
    )


def test_cancelled_booking_does_not_cause_conflict() -> None:
    create_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Cancelled Slot Test",
            "customer_phone": "0500000000",
            "booking_datetime": "2026-09-12T10:00:00",
        },
    )

    assert create_response.status_code == 200

    booking_id = create_response.json()["id"]

    cancel_response = client.patch(
        f"/bookings/{booking_id}/cancel"
    )

    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == "cancelled"

    replacement_response = client.post(
        "/bookings",
        json={
            "service_id": "6a779ed59b6b145fcfe108ab",
            "customer_name": "Replacement Booking",
            "customer_phone": "0511111111",
            "booking_datetime": "2026-09-12T10:00:00",
        },
    )

    assert replacement_response.status_code == 200