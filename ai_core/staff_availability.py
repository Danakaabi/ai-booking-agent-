from datetime import datetime, timedelta

from api.schemas.staff_availability import StaffAvailability
from database.repositories.staff import get_staff_by_id
from database.repositories.staff_availability import (
    get_staff_availability,
)


def staff_is_available(
    staff_id: str,
    booking_start: datetime,
    duration_minutes: int,
) -> bool:
    staff = get_staff_by_id(staff_id)

    if staff is None or not staff.get("active", False):
        return False

    booking_day = booking_start.strftime("%A").lower()
    booking_end = booking_start + timedelta(minutes=duration_minutes)

    availability_records = get_staff_availability(staff_id)

    for record in availability_records:
        availability = StaffAvailability(**record)

        if availability.day_of_week.value.lower() != booking_day:
            continue

        schedule_start = datetime.combine(
            booking_start.date(),
            availability.start_time,
        )

        schedule_end = datetime.combine(
            booking_start.date(),
            availability.end_time,
        )

        if (
            booking_start >= schedule_start
            and booking_end <= schedule_end
        ):
            return True

    return False