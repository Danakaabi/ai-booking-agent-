from datetime import timedelta

from api.schemas.availability import Availability
from api.schemas.booking import BookingCreate
from ai_core.availability import (
    has_booking_conflict,
    is_booking_within_business_hours,
)
from database.repositories.availability import get_active_availability
from database.repositories.bookings import get_confirmed_bookings
from database.repositories.services import (
    get_active_services_by_id,
    get_service_by_id,
)

def booking_has_conflict(booking: BookingCreate) -> bool:
    """
    Check whether a requested booking conflicts with
    any existing confirmed booking.
    """

    service = get_service_by_id(booking.service_id)

    if service is None:
        return False

    booking_start = booking.booking_datetime

    booking_end = booking_start + timedelta(
        minutes=service["duration_minutes"]
    )

    confirmed_bookings = get_confirmed_bookings()
    services_by_id = get_active_services_by_id()

    return has_booking_conflict(
        new_start=booking_start,
        new_end=booking_end,
        existing_bookings=confirmed_bookings,
        services_by_id=services_by_id,
    )




def booking_is_within_business_hours(
    booking: BookingCreate,
) -> bool:
    service = get_service_by_id(booking.service_id)

    if service is None:
        return False

    booking_day = booking.booking_datetime.strftime("%A").lower()

    availability_records = get_active_availability()

    for record in availability_records:
        availability = Availability(**record)

        if availability.day_of_week.value != booking_day:
            continue

        return is_booking_within_business_hours(
            booking_start=booking.booking_datetime,
            duration_minutes=service["duration_minutes"],
            opening_time=availability.start_time,
            closing_time=availability.end_time,
        )

    return False