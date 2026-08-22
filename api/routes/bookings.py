from fastapi import APIRouter, HTTPException

from ai_core.booking_engine import (
    execute_booking_cancellation,
    execute_booking_request,
    execute_booking_update,
)
from api.http_errors import raise_booking_http_error
from api.schemas.booking import BookingCreate, BookingUpdate
from database.repositories.bookings import (
    

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
    raise_booking_http_error(error)
    

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
    raise_booking_http_error(error)
    if update_booking is None:
        raise HTTPException(
            status_code=500,
            detail="Booking could not be updated",
        )
        
    return updated_booking

@router.patch("/{booking_id}/cancel")
def cancel_booking_route(booking_id: str) -> dict:
    cancelled_booking, error = execute_booking_cancellation(
        booking_id
    )

    raise_booking_http_error(error)

    if cancelled_booking is None:
        raise HTTPException(
            status_code=500,
            detail="Booking could not be cancelled",
        )

    return cancelled_booking