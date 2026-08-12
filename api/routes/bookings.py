from fastapi import APIRouter

from api.schemas.booking import BookingCreate
from database.repositories.bookings import create_booking, get_all_bookings


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post("")
def create_booking_route(booking: BookingCreate) -> dict:
    return create_booking(booking)


@router.get("")
def get_bookings() -> list[dict]:
    return get_all_bookings()
