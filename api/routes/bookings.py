from fastapi import APIRouter, HTTPException

from ai_core.booking_engine import (
    execute_booking_request,
    execute_booking_update,
)
from api.schemas.booking import BookingCreate, BookingUpdate
from database.repositories.bookings import (
    cancel_booking,

    get_all_bookings,
    get_booking_by_id,
    update_booking,
)


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post("")
def create_booking_route(booking: BookingCreate) -> dict:
    created_booking, error = execute_booking_request(booking)

    if error == "Service not found":
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    if error == "Staff not found":
        raise HTTPException(
            status_code=404,
            detail="Staff not found",
        )

    if error == "Booking time conflicts with an existing booking":
        raise HTTPException(
            status_code=409,
            detail="Booking time conflicts with an existing booking",
        )

    if error == "Booking is outside business hours":
        raise HTTPException(
            status_code=422,
            detail="Booking time is outside business hours",
        )

    if error == "Staff does not provide this service":
        raise HTTPException(
            status_code=422,
            detail="Staff does not provide this service",
        )

    if error == "Staff is not available at this time":
        raise HTTPException(
            status_code=422,
            detail="Staff is not available at this time",
        )

    if error is not None:
        raise HTTPException(
            status_code=422,
            detail=error,
        )

    if created_booking is None:
        raise HTTPException(
            status_code=500,
            detail="Booking could not be created",
        )

    return created_booking

@router.get("")
def get_bookings() -> list[dict]:
    return get_all_bookings()


@router.get("/{booking_id}")
def get_booking(booking_id: str) -> dict:
    booking = get_booking_by_id(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    return booking
@router.patch("/{booking_id}")
def update_booking_route(
    booking_id: str,
    update: BookingUpdate,
) -> dict:
    updated_booking, error = execute_booking_update(
        booking_id,
        update,
    )

    if error == "Booking not found":
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    if error == "Service not found":
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    if error == "Staff not found":
        raise HTTPException(
            status_code=404,
            detail="Staff not found",
        )

    if error == "Booking time conflicts with an existing booking":
        raise HTTPException(
            status_code=409,
            detail="Booking time conflicts with an existing booking",
        )

    if error == "Booking is outside business hours":
        raise HTTPException(
            status_code=422,
            detail="Booking time is outside business hours",
        )

    if error == "Staff does not provide this service":
        raise HTTPException(
            status_code=422,
            detail="Staff does not provide this service",
        )

    if error == "Staff is not available at this time":
        raise HTTPException(
            status_code=422,
            detail="Staff is not available at this time",
        )

    if error is not None:
        raise HTTPException(
            status_code=422,
            detail=error,
        )

    if updated_booking is None:
        raise HTTPException(
            status_code=500,
            detail="Booking could not be updated",
        )

    return updated_booking

@router.patch("/{booking_id}/cancel")
def cancel_booking_route(booking_id: str) -> dict:
    booking = cancel_booking(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    return booking