from datetime import timedelta

from ai_core.availability import (
    has_booking_conflict,
    is_booking_within_business_hours,
)
from ai_core.staff_availability import staff_is_available
from api.schemas.availability import Availability
from api.schemas.booking import BookingCreate
from database.repositories.availability import get_active_availability
from database.repositories.bookings import (
    get_confirmed_bookings,
    get_confirmed_bookings_by_staff_id,
)
from database.repositories.services import (
    get_active_services_by_id,
    get_service_by_id,
)
from database.repositories.staff import get_staff_by_id


def booking_has_conflict(booking: BookingCreate) -> bool:
    service = get_service_by_id(booking.service_id)

    if service is None:
        return False

    booking_start = booking.booking_datetime
    booking_end = booking_start + timedelta(
        minutes=service["duration_minutes"]
    )

    if booking.staff_id:
        confirmed_bookings = get_confirmed_bookings_by_staff_id(
            booking.staff_id
        )
    else:
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


def staff_supports_service(
    staff_id: str,
    service_id: str,
) -> bool:
    staff = get_staff_by_id(staff_id)

    if staff is None:
        return False

    return service_id in staff.get("service_ids", [])


def booking_staff_is_available(
    booking: BookingCreate,
) -> bool:
    if not booking.staff_id:
        return True

    service = get_service_by_id(booking.service_id)

    if service is None:
        return False

    return staff_is_available(
        staff_id=booking.staff_id,
        booking_start=booking.booking_datetime,
        duration_minutes=service["duration_minutes"],
    )


def validate_booking_request(
    booking: BookingCreate,
) -> tuple[bool, str | None]:
    service = get_service_by_id(booking.service_id)

    if service is None:
        return False, "Service not found"

    if not booking_is_within_business_hours(booking):
        return False, "Booking is outside business hours"

    if booking.staff_id:
        staff = get_staff_by_id(booking.staff_id)

        if staff is None:
            return False, "Staff not found"

        if not staff_supports_service(
            booking.staff_id,
            booking.service_id,
        ):
            return False, "Staff does not provide this service"

        if not booking_staff_is_available(booking):
            return False, "Staff is not available at this time"

    if booking_has_conflict(booking):
        return False, (
            "Booking time conflicts with an existing booking"
        )

    return True, None