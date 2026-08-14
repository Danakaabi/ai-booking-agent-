from bson import ObjectId

from api.schemas.staff import Staff
from database.connection import database


staff_collection = database["staff"]


def create_staff(staff: Staff) -> dict:
    staff_data = staff.model_dump()

    result = staff_collection.insert_one(staff_data)

    staff_data.pop("_id", None)
    staff_data["id"] = str(result.inserted_id)

    return staff_data


def get_staff_by_id(staff_id: str) -> dict | None:
    if not ObjectId.is_valid(staff_id):
        return None

    staff = staff_collection.find_one(
        {"_id": ObjectId(staff_id)}
    )

    if staff is None:
        return None

    staff["id"] = str(staff.pop("_id"))

    return staff


def get_all_staff() -> list[dict]:
    staff_members = list(
        staff_collection.find(
            {"active": True}
        )
    )

    for staff in staff_members:
        staff["id"] = str(staff.pop("_id"))

    return staff_members



def get_staff_by_service_id(service_id: str) -> list[dict]:
    staff_members = list(
        staff_collection.find(
            {
                "active": True,
                "service_ids": service_id,
            }
        )
    )

    for staff in staff_members:
        staff["id"] = str(staff.pop("_id"))

    return staff_members