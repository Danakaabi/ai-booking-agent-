from fastapi import APIRouter, HTTPException
from datetime import date

from ai_core.available_slots import generate_available_slots
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




@router.get("/{staff_id}/available-slots")
def get_available_slots(
    staff_id: str,
    target_date: date,
    start_hour: int = 9,
    end_hour: int = 17,
    duration_minutes: int = 60,
    interval_minutes: int = 30,
) -> dict:
    staff = get_staff_by_id(staff_id)

    if staff is None:
        raise HTTPException(
            status_code=404,
            detail="Staff not found",
        )

    slots = generate_available_slots(
        staff_id=staff_id,
        target_date=target_date,
        start_hour=start_hour,
        end_hour=end_hour,
        duration_minutes=duration_minutes,
        interval_minutes=interval_minutes,
    )

    return {
        "staff_id": staff_id,
        "date": target_date.isoformat(),
        "slots": [
            slot.isoformat()
            for slot in slots
        ],
    }