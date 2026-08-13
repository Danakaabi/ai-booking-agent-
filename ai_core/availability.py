from datetime import datetime, time, timedelta


def is_within_business_hours(
    booking_time: time,
    opening_time: time,
    closing_time: time,
) -> bool:
    """
    Check whether a requested booking time falls within business hours.
    """

    return opening_time <= booking_time < closing_time


def is_booking_within_business_hours(
    booking_start: datetime,
    duration_minutes: int,
    opening_time: time,
    closing_time: time,
) -> bool:
    """
    Check whether the full booking duration fits within business hours.
    """

    booking_end = booking_start + timedelta(minutes=duration_minutes)

    opening_datetime = datetime.combine(
        booking_start.date(),
        opening_time,
    )

    closing_datetime = datetime.combine(
        booking_start.date(),
        closing_time,
    )

    return (
        booking_start >= opening_datetime
        and booking_end <= closing_datetime
    )


def bookings_overlap(
    new_start: datetime,
    new_end: datetime,
    existing_start: datetime,
    existing_end: datetime,
) -> bool:
    """
    Check whether two booking time ranges overlap.
    """

    return new_start < existing_end and new_end > existing_start


def has_booking_conflict(
    new_start: datetime,
    new_end: datetime,
    existing_bookings: list[dict],
    services_by_id: dict[str, dict],
) -> bool:
    """
    Check whether a new booking overlaps with any existing confirmed booking.

    Each existing booking uses its service_id to determine
    the booking duration from services_by_id.
    """

    for booking in existing_bookings:
        service = services_by_id.get(booking["service_id"])

        if service is None:
            continue

        existing_start = booking["booking_datetime"]
        existing_end = existing_start + timedelta(
            minutes=service["duration_minutes"]
        )

        if bookings_overlap(
            new_start=new_start,
            new_end=new_end,
            existing_start=existing_start,
            existing_end=existing_end,
        ):
            return True

    return False