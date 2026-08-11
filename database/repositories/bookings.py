from typing import Any

from api.schemas.booking import BookingCreate
from database.connection import database


bookings_collection = database["bookings"]

def create_booking(booking: BookingCreate) -> dict[str, Any]:
    booking_data = booking.model_dump()
    result = bookings_collection.insert_one(booking_data)

    booking_data.pop("_id", None)
    booking_data["id"] = str(result.inserted_id)

    return booking_data