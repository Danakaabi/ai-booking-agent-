from datetime import datetime, time


from ai_core.availability import (
    is_booking_within_business_hours,
    is_within_business_hours,
    bookings_overlap,
    has_booking_conflict,
)

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



    