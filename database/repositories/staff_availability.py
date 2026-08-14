from typing import Any

from api.schemas.staff_availability import StaffAvailability
from database.connection import database


staff_availability_collection = database["staff_availability"]


def create_staff_availability(
    availability: StaffAvailability,
) -> dict[str, Any]:
    availability_data = availability.model_dump(mode="json")

    result = staff_availability_collection.insert_one(
        availability_data
    )

    availability_data.pop("_id", None)
    availability_data["id"] = str(result.inserted_id)

    return availability_data


def get_staff_availability(
    staff_id: str,
) -> list[dict[str, Any]]:
    records = list(
        staff_availability_collection.find(
            {
                "staff_id": staff_id,
                "active": True,
            }
        )
    )

    for record in records:
        record["id"] = str(record.pop("_id"))

    return records




[{
	"resource": "/Users/dana/Desktop/ai-booking-agent/database/repositories/staff_availability.py",
	"owner": "Pylance",
	"code": {
		"value": "reportUndefinedVariable",
		"target": {
			"$mid": 1,
			"path": "/microsoft/pylance-release/blob/main/docs/diagnostics/reportUndefinedVariable.md",
			"scheme": "https",
			"authority": "github.com"
		}
	},
	"severity": 4,
	"message": "\"bookings_collection\" is not defined",
	"source": "Pylance",
	"startLineNumber": 49,
	"startColumn": 9,
	"endLineNumber": 49,
	"endColumn": 28,
	"modelVersionId": 9,
	"origin": "extHost1"
}]