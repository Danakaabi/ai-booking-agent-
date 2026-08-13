from datetime import datetime, time


from ai_core.availability import (
    is_booking_within_business_hours,
    is_within_business_hours,
    bookings_overlap,
    has_booking_conflict,
)
from api.schemas.booking import BookingCreate
from ai_core.booking_engine import booking_is_within_business_hours

from database.repositories.availability import get_active_availability

import pytest
from pydantic import ValidationError

from api.schemas.availability import Availability


def test_booking_time_within_business_hours():
    result = is_within_business_hours(
        booking_time=time(10, 0),
        opening_time=time(9, 0),
        closing_time=time(17, 0),
    )



    assert result is True


def test_booking_time_at_closing_time_is_not_available():
    result = is_within_business_hours(
        booking_time=time(17, 0),
        opening_time=time(9, 0),
        closing_time=time(17, 0),
    )

    assert result is False


def test_booking_time_before_opening_time_is_not_available():
    result = is_within_business_hours(
        booking_time=time(8, 0),
        opening_time=time(9, 0),
        closing_time=time(17, 0),
    )

    assert result is False




def test_full_booking_duration_fits_within_business_hours():
    result = is_booking_within_business_hours(
        booking_start=datetime(2026, 8, 13, 16, 0),
        duration_minutes=60,
        opening_time=time(9, 0),
        closing_time=time(17, 0),
    )

    assert result is True


def test_booking_duration_exceeds_closing_time():
    result = is_booking_within_business_hours(
        booking_start=datetime(2026, 8, 13, 16, 30),
        duration_minutes=60,
        opening_time=time(9, 0),
        closing_time=time(17, 0),
    )

    assert result is False


def test_overlapping_bookings_are_detected():
    result = bookings_overlap(
        new_start=datetime(2026, 8, 13, 10, 30),
        new_end=datetime(2026, 8, 13, 11, 30),
        existing_start=datetime(2026, 8, 13, 10, 0),
        existing_end=datetime(2026, 8, 13, 11, 0),
    )

    assert result is True


def test_back_to_back_bookings_do_not_overlap():
    result = bookings_overlap(
        new_start=datetime(2026, 8, 13, 11, 0),
        new_end=datetime(2026, 8, 13, 12, 0),
        existing_start=datetime(2026, 8, 13, 10, 0),
        existing_end=datetime(2026, 8, 13, 11, 0),
    )

    assert result is False


def test_new_booking_that_contains_existing_booking_overlaps():
    result = bookings_overlap(
        new_start=datetime(2026, 8, 13, 9, 30),
        new_end=datetime(2026, 8, 13, 11, 30),
        existing_start=datetime(2026, 8, 13, 10, 0),
        existing_end=datetime(2026, 8, 13, 11, 0),
    )

    assert result is True


def test_new_booking_inside_existing_booking_overlaps():
    result = bookings_overlap(
        new_start=datetime(2026, 8, 13, 10, 15),
        new_end=datetime(2026, 8, 13, 10, 45),
        existing_start=datetime(2026, 8, 13, 10, 0),
        existing_end=datetime(2026, 8, 13, 11, 0),
    )

    assert result is True


def test_identical_booking_times_overlap():
    result = bookings_overlap(
        new_start=datetime(2026, 8, 13, 10, 0),
        new_end=datetime(2026, 8, 13, 11, 0),
        existing_start=datetime(2026, 8, 13, 10, 0),
        existing_end=datetime(2026, 8, 13, 11, 0),
    )

    assert result is True


def test_has_booking_conflict_detects_overlap():
    existing_bookings = [
        {
            "service_id": "service-1",
            "booking_datetime": datetime(2026, 8, 13, 10, 0),
            "status": "confirmed",
        }
    ]

    services_by_id = {
        "service-1": {
            "duration_minutes": 60,
        }
    }

    result = has_booking_conflict(
        new_start=datetime(2026, 8, 13, 10, 30),
        new_end=datetime(2026, 8, 13, 11, 30),
        existing_bookings=existing_bookings,
        services_by_id=services_by_id,
    )

    assert result is True


def test_has_booking_conflict_returns_false_when_no_overlap():
    existing_bookings = [
        {
            "service_id": "service-1",
            "booking_datetime": datetime(2026, 8, 13, 10, 0),
            "status": "confirmed",
        }
    ]

    services_by_id = {
        "service-1": {
            "duration_minutes": 60,
        }
    }

    result = has_booking_conflict(
        new_start=datetime(2026, 8, 13, 11, 0),
        new_end=datetime(2026, 8, 13, 12, 0),
        existing_bookings=existing_bookings,
        services_by_id=services_by_id,
    )

    assert result is False



def test_availability_schema_accepts_valid_time_range():
    availability = Availability(
        day_of_week="sunday",
        start_time="09:00:00",
        end_time="17:00:00",
        active=True,
    )

    assert availability.day_of_week == "sunday"
    assert availability.start_time == time(9, 0)
    assert availability.end_time == time(17, 0)
    assert availability.active is True


def test_availability_schema_rejects_invalid_time_range():
    with pytest.raises(
        ValidationError,
        match="end_time must be later than start_time",
    ):
        Availability(
            day_of_week="sunday",
            start_time="17:00:00",
            end_time="09:00:00",
            active=True,
        )





def test_availability_schema_rejects_invalid_day_of_week():
    with pytest.raises(ValidationError):
        Availability(
            day_of_week="pizza",
            start_time="09:00:00",
            end_time="17:00:00",
            active=True,
        )



def test_booking_engine_accepts_booking_within_business_hours():
    booking = BookingCreate(
        service_id="6a779ed59b6b145fcfe108ab",
        customer_name="Availability Test",
        customer_phone="0500000000",
        booking_datetime=datetime(2026, 8, 16, 10, 0),
    )

    result = booking_is_within_business_hours(booking)

    assert result is True

def test_booking_engine_rejects_booking_that_exceeds_business_hours():
    booking = BookingCreate(
        service_id="6a779ed59b6b145fcfe108ab",
        customer_name="Availability Outside Hours Test",
        customer_phone="0500000000",
        booking_datetime=datetime(2026, 8, 16, 16, 30),
    )

    result = booking_is_within_business_hours(booking)

    assert result is False

def test_booking_engine_rejects_booking_before_business_hours():
    booking = BookingCreate(
        service_id="6a779ed59b6b145fcfe108ab",
        customer_name="Before Hours Test",
        customer_phone="0500000000",
        booking_datetime=datetime(2026, 8, 16, 8, 30),
    )

    result = booking_is_within_business_hours(booking)

    assert result is False