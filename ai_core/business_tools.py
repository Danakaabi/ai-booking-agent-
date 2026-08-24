from datetime import date, datetime

from ai_core.available_slots import generate_available_slots
from database.repositories.services import (
    get_all_services,
    get_service_by_id,
)
from database.repositories.staff import get_all_staff
from database.repositories.staff_availability import (
    get_staff_availability,
)


def get_services() -> list[dict]:
    """Return all active services through existing repository logic."""
    return get_all_services()


def get_staff() -> list[dict]:
    """Return all active staff through existing repository logic."""
    return get_all_staff()


def get_available_times(
    staff_id: str,
    service_id: str,
    target_date: date,
) -> list[datetime]:
    """Return available booking times using existing availability logic."""
    service = get_service_by_id(service_id)

    if service is None:
        return []

    target_day = target_date.strftime("%A").lower()

    schedules = [
        record
        for record in get_staff_availability(staff_id)
        if record["day_of_week"].lower() == target_day
    ]

    if not schedules:
        return []

    start_times = [
        datetime.fromisoformat(
            f"{target_date.isoformat()}T{record['start_time']}"
        ).time()
        for record in schedules
    ]
    end_times = [
        datetime.fromisoformat(
            f"{target_date.isoformat()}T{record['end_time']}"
        ).time()
        for record in schedules
    ]

    earliest_start = min(start_times)
    latest_end = max(end_times)

    start_hour = earliest_start.hour
    end_hour = latest_end.hour + (
        1
        if (
            latest_end.minute
            or latest_end.second
            or latest_end.microsecond
        )
        else 0
    )

    return generate_available_slots(
        staff_id=staff_id,
        target_date=target_date,
        start_hour=start_hour,
        end_hour=end_hour,
        duration_minutes=service["duration_minutes"],
        interval_minutes=30,
    )
