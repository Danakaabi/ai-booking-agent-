from fastapi import APIRouter

from api.schemas.service import Service


router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.get("", response_model=list[Service])
def get_services() -> list[Service]:
    return [
        Service(
            name="Haircut",
            duration_minutes=60,
            price=85.0,
            active=True,
        )
    ]