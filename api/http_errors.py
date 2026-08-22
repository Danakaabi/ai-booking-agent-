from fastapi import HTTPException


def raise_booking_http_error(error: str | None) -> None:
    if error is None:
        return

    error_mapping = {
        "Booking not found": (404, "Booking not found"),
        "Service not found": (404, "Service not found"),
        "Staff not found": (404, "Staff not found"),
        "Booking time conflicts with an existing booking": (
            409,
            "Booking time conflicts with an existing booking",
        ),
        "Booking is outside business hours": (
            422,
            "Booking time is outside business hours",
        ),
        "Staff does not provide this service": (
            422,
            "Staff does not provide this service",
        ),
        "Staff is not available at this time": (
            422,
            "Staff is not available at this time",
        ),
    }

    status_code, detail = error_mapping.get(
        error,
        (422, error),
    )

    raise HTTPException(
        status_code=status_code,
        detail=detail,
    )