from typing import Any

from database.connection import database


availability_collection = database["availability"]


def get_active_availability() -> list[dict[str, Any]]:
    availability = list(
        availability_collection.find(
            {"active": True},
            {"_id": 0},
        )
    )

    return availability