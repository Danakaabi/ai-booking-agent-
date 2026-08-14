from api.schemas.staff_availability import StaffAvailability
from database.repositories.staff_availability import (
    create_staff_availability,
    get_staff_availability,

)
from datetime import date
from database.repositories.bookings import bookings_collection
from ai_core.available_slots import generate_available_slots

from fastapi.testclient import TestClient

from api.main import app

def test_create_staff_availability():
    availability = StaffAvailability(
        staff_id="staff-test-id",
        day_of_week="sunday",
        start_time="10:00:00",
        end_time="16:00:00",
    )

    created = create_staff_availability(availability)

    assert created["staff_id"] == "staff-test-id"
    assert created["day_of_week"] == "sunday"
    assert created["start_time"] == "10:00:00"
    assert created["end_time"] == "16:00:00"
    assert created["active"] is True
    assert "id" in created


def test_get_staff_availability():
    availability = StaffAvailability(
        staff_id="staff-availability-test",
        day_of_week="monday",
        start_time="09:00:00",
        end_time="15:00:00",
    )

    create_staff_availability(availability)

    records = get_staff_availability(
        "staff-availability-test"
    )

    assert len(records) > 0
    assert all(
        record["staff_id"] == "staff-availability-test"
        for record in records
    )


from datetime import datetime

from api.schemas.staff import Staff
from ai_core.staff_availability import staff_is_available
from database.repositories.staff import create_staff


def test_staff_is_available_within_schedule():
    staff = create_staff(
        Staff(
            name="Available Staff",
            phone="0500000040",
        )
    )

    create_staff_availability(
        StaffAvailability(
            staff_id=staff["id"],
            day_of_week="sunday",
            start_time="09:00:00",
            end_time="17:00:00",
        )
    )

    result = staff_is_available(
        staff_id=staff["id"],
        booking_start=datetime(2026, 8, 16, 10, 0),
        duration_minutes=60,
    )

    assert result is True


def test_staff_is_not_available_outside_schedule():
    staff = create_staff(
        Staff(
            name="Unavailable Staff",
            phone="0500000041",
        )
    )

    create_staff_availability(
        StaffAvailability(
            staff_id=staff["id"],
            day_of_week="sunday",
            start_time="09:00:00",
            end_time="17:00:00",
        )
    )

    result = staff_is_available(
        staff_id=staff["id"],
        booking_start=datetime(2026, 8, 16, 17, 0),
        duration_minutes=60,
    )

    assert result is False


def test_staff_is_not_available_on_unscheduled_day():
    staff = create_staff(
        Staff(
            name="Day Test Staff",
            phone="0500000042",
        )
    )

    create_staff_availability(
        StaffAvailability(
            staff_id=staff["id"],
            day_of_week="monday",
            start_time="09:00:00",
            end_time="17:00:00",
        )
    )

    result = staff_is_available(
        staff_id=staff["id"],
        booking_start=datetime(2026, 8, 16, 10, 0),
        duration_minutes=60,
    )

    assert result is False




def test_generate_available_slots():
    staff = create_staff(
        Staff(
            name="Slot Staff",
            phone="0500000043",
        )
    )

    create_staff_availability(
        StaffAvailability(
            staff_id=staff["id"],
            day_of_week="sunday",
            start_time="09:00:00",
            end_time="12:00:00",
        )
    )

    slots = generate_available_slots(
        staff_id=staff["id"],
        target_date=date(2026, 8, 16),
        start_hour=9,
        end_hour=12,
        duration_minutes=60,
        interval_minutes=30,
    )

    assert datetime(2026, 8, 16, 9, 0) in slots
    assert datetime(2026, 8, 16, 9, 30) in slots
    assert datetime(2026, 8, 16, 10, 0) in slots
    assert datetime(2026, 8, 16, 10, 30) in slots
    assert datetime(2026, 8, 16, 11, 0) in slots

    assert datetime(2026, 8, 16, 11, 30) not in slots





def test_available_slots_exclude_staff_booking_conflicts():
    staff = create_staff(
        Staff(
            name="Booked Slot Staff",
            phone="0500000044",
            service_ids=[
                "6a779ed59b6b145fcfe108ab"
            ],
        )
    )

    create_staff_availability(
        StaffAvailability(
            staff_id=staff["id"],
            day_of_week="sunday",
            start_time="09:00:00",
            end_time="12:00:00",
        )
    )

    bookings_collection.delete_many(
        {
            "customer_name": "Slot Conflict Test"
        }
    )

    bookings_collection.insert_one(
        {
            "service_id": "6a779ed59b6b145fcfe108ab",
            "staff_id": staff["id"],
            "customer_name": "Slot Conflict Test",
            "customer_phone": "0500000095",
            "booking_datetime": datetime(
                2026,
                8,
                16,
                10,
                0,
            ),
            "status": "confirmed",
        }
    )

    slots = generate_available_slots(
        staff_id=staff["id"],
        target_date=date(2026, 8, 16),
        start_hour=9,
        end_hour=12,
        duration_minutes=60,
        interval_minutes=30,
    )

    assert datetime(2026, 8, 16, 9, 0) in slots

    assert datetime(2026, 8, 16, 9, 30) not in slots
    assert datetime(2026, 8, 16, 10, 0) not in slots
    assert datetime(2026, 8, 16, 10, 30) not in slots

    assert datetime(2026, 8, 16, 11, 0) in slots




client = TestClient(app)
def test_available_slots_api():
    staff = create_staff(
        Staff(
            name="Slots API Staff",
            phone="0500000045",
            service_ids=[
                "6a779ed59b6b145fcfe108ab"
            ],
        )
    )

    create_staff_availability(
        StaffAvailability(
            staff_id=staff["id"],
            day_of_week="sunday",
            start_time="09:00:00",
            end_time="12:00:00",
        )
    )

    response = client.get(
        f"/staff/{staff['id']}/available-slots",
        params={
            "target_date": "2026-08-16",
            "start_hour": 9,
            "end_hour": 12,
            "duration_minutes": 60,
            "interval_minutes": 30,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["staff_id"] == staff["id"]
    assert data["date"] == "2026-08-16"
    assert isinstance(data["slots"], list)

    assert "2026-08-16T09:00:00" in data["slots"]
    assert "2026-08-16T11:00:00" in data["slots"]
    assert "2026-08-16T11:30:00" not in data["slots"]