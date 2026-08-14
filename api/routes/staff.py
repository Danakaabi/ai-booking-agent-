from fastapi import APIRouter, HTTPException

from api.schemas.staff import Staff
from database.repositories.staff import (
    create_staff,
    get_all_staff,
    get_staff_by_id,
)


router = APIRouter(
    prefix="/staff",
    tags=["Staff"],
)


@router.post("")
def create_staff_route(staff: Staff) -> dict:
    return create_staff(staff)


@router.get("")
def get_staff_route() -> list[dict]:
    return get_all_staff()


@router.get("/{staff_id}")
def get_staff_by_id_route(staff_id: str) -> dict:
    staff = get_staff_by_id(staff_id)

    if staff is None:
        raise HTTPException(
            status_code=404,
            detail="Staff not found",
        )

    return staff