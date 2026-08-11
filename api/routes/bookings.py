from fastapi import APIRouter

from api.schemas.booking import BookingCreate
from database.repositories.bookings import create_booking


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post("")
def create_booking_route(booking: BookingCreate) -> dict:
    return create_booking(booking)