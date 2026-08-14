from datetime import date, datetime, timedelta

from ai_core.availability import has_booking_conflict
from ai_core.staff_availability import staff_is_available
from database.repositories.bookings import (
    get_confirmed_bookings_by_staff_id,
)
from database.repositories.services import (
    get_active_services_by_id,
)


def generate_available_slots(
    staff_id: str,
    target_date: date,
    start_hour: int,
    end_hour: int,
    duration_minutes: int,
    interval_minutes: int = 30,
) -> list[datetime]:
    slots: list[datetime] = []

    current = datetime.combine(
        target_date,
        datetime.min.time(),
    ).replace(hour=start_hour)

    end = datetime.combine(
        target_date,
        datetime.min.time(),
    ).replace(hour=end_hour)

    confirmed_bookings = get_confirmed_bookings_by_staff_id(
        staff_id
    )

    services_by_id = get_active_services_by_id()

    while current < end:
        slot_end = current + timedelta(
            minutes=duration_minutes
        )

        within_staff_schedule = staff_is_available(
            staff_id=staff_id,
            booking_start=current,
            duration_minutes=duration_minutes,
        )

        has_conflict = has_booking_conflict(
            new_start=current,
            new_end=slot_end,
            existing_bookings=confirmed_bookings,
            services_by_id=services_by_id,
        )

        if within_staff_schedule and not has_conflict:
            slots.append(current)

        current += timedelta(
            minutes=interval_minutes
        )

    return slots