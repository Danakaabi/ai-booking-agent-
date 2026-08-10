from typing import Any
from api.routes import services
from database.connection import database

services_collection = database["services"]

def get_all_services() -> list[dict[str, Any]]:
  services= list(
     services_collection .find(
        {"active": True},
        {"_id": 0}
         
  )

    )

  
  return services