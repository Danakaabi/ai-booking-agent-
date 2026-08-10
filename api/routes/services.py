from fastapi import APIRouter

from api.schemas.service import Service
from database.repositories.services import get_all_services


router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.get("", response_model=list[Service])
def get_services() -> list[Service]:
    services = get_all_services()

    return [Service(**service) for service in services]