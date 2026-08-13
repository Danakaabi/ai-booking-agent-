from fastapi import APIRouter, HTTPException
from ai_core.booking_engine import booking_has_conflict
from api.schemas.booking import BookingCreate, BookingUpdate
from database.repositories.bookings import (
    create_booking,
    get_all_bookings,
    get_booking_by_id,
    update_booking,
    cancel_booking,
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.post("")
def create_booking_route(booking: BookingCreate) -> dict:
    if booking_has_conflict(booking):
        raise HTTPException(
            status_code=409,
            detail="Booking time conflicts with an existing booking",
        )

    return create_booking(booking)

@router.get("")
def get_bookings() -> list[dict]:
    return get_all_bookings()


@router.get("/{booking_id}")
def get_booking(booking_id: str) -> dict:
    booking = get_booking_by_id(booking_id)

    if booking is None:
     raise HTTPException(
        status_code=404,
        detail="Booking not found"
    )

    return booking


@router.patch("/{booking_id}")
def update_booking_route(
    booking_id: str,
    update: BookingUpdate,
) -> dict:
    booking = update_booking(
        booking_id,
        update,
    )

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    return booking


@router.patch("/{booking_id}/cancel")
def cancel_booking_route(booking_id: str) -> dict:
    booking = cancel_booking(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    return booking