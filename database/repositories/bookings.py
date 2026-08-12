from typing import Any
from api.schemas.booking import BookingCreate, BookingUpdate
from database.connection import database
from bson import ObjectId

bookings_collection = database["bookings"]

def create_booking(booking: BookingCreate) -> dict[str, Any]:
    booking_data = booking.model_dump()
    result = bookings_collection.insert_one(booking_data)

    booking_data.pop("_id", None)
    booking_data["id"] = str(result.inserted_id)

    return booking_data


def get_all_bookings() -> list[dict[str, Any]]:
    bookings = list(bookings_collection.find())
    for booking in bookings:
       booking["id"] = str(booking.pop("_id"))

    return bookings

def get_booking_by_id(booking_id: str) -> dict[str, Any] | None:
    booking = bookings_collection.find_one(
        {"_id": ObjectId(booking_id)}
    )

    if booking is None:
        return None

    booking["id"] = str(booking.pop("_id"))

    return booking


def update_booking(
    booking_id: str,
    update: BookingUpdate,
) -> dict[str, Any] | None:
    update_data = update.model_dump(exclude_none=True)

    result = bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        return None

    return get_booking_by_id(booking_id)



def cancel_booking(booking_id: str) -> dict[str, Any] | None:
    result = bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "cancelled"}},
    )

    if result.matched_count == 0:
        return None

    return get_booking_by_id(booking_id)



def cancel_booking(booking_id: str) -> dict[str, Any] | None:
    result = bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "cancelled"}},
    )

    if result.matched_count == 0:
        return None

    return get_booking_by_id(booking_id)
