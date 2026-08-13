from typing import Any
from database.connection import database
from bson import ObjectId

services_collection = database["services"]

def get_all_services() -> list[dict[str, Any]]:
  services= list(
     services_collection .find(
        {"active": True},
        {"_id": 0}
         
  )

    )

  
  return services



def get_service_by_id(service_id: str) -> dict[str, Any] | None:
    if not ObjectId.is_valid(service_id):
        return None

    service = services_collection.find_one(
        {
            "_id": ObjectId(service_id),
            "active": True,
        }
    )

    if service is None:
        return None

    service["id"] = str(service.pop("_id"))

    return service


def get_active_services_by_id() -> dict[str, dict[str, Any]]:
    services = services_collection.find(
        {"active": True}
    )

    services_by_id: dict[str, dict[str, Any]] = {}

    for service in services:
        service_id = str(service.pop("_id"))
        services_by_id[service_id] = service

    return services_by_id