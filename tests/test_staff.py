from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from api.main import app
from api.schemas.staff import Staff
from database.repositories.staff import (
    create_staff,
    get_all_staff,
    get_staff_by_id,
    get_staff_by_service_id,
)


client = TestClient(app)


def test_staff_schema_accepts_valid_data():
    staff = Staff(
        name="Staff Member",
        phone="0500000020",
    )

    assert staff.name == "Staff Member"
    assert staff.phone == "0500000020"
    assert staff.active is True


def test_staff_schema_rejects_short_name():
    with pytest.raises(ValidationError):
        Staff(
            name="S",
            phone="0500000020",
        )


def test_create_staff_repository():
    staff = Staff(
        name="Repository Staff",
        phone="0500000021",
    )

    created_staff = create_staff(staff)

    assert created_staff["name"] == "Repository Staff"
    assert created_staff["phone"] == "0500000021"
    assert created_staff["active"] is True
    assert "id" in created_staff


def test_get_staff_by_id_repository():
    staff = Staff(
        name="Staff By ID",
        phone="0500000022",
    )

    created_staff = create_staff(staff)

    stored_staff = get_staff_by_id(created_staff["id"])

    assert stored_staff is not None
    assert stored_staff["id"] == created_staff["id"]
    assert stored_staff["name"] == "Staff By ID"


def test_get_staff_by_id_repository_not_found():
    staff = get_staff_by_id(
        "000000000000000000000000"
    )

    assert staff is None


def test_get_all_staff_returns_active_staff():
    active_staff = Staff(
        name="Active Staff",
        phone="0500000023",
        active=True,
    )

    inactive_staff = Staff(
        name="Inactive Staff",
        phone="0500000024",
        active=False,
    )

    created_active = create_staff(active_staff)
    created_inactive = create_staff(inactive_staff)

    staff_members = get_all_staff()

    staff_ids = [
        staff["id"]
        for staff in staff_members
    ]

    assert created_active["id"] in staff_ids
    assert created_inactive["id"] not in staff_ids
    assert all(staff["active"] is True for staff in staff_members)


def test_create_staff_api():
    response = client.post(
        "/staff",
        json={
            "name": "API Staff",
            "phone": "0500000025",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "API Staff"
    assert data["phone"] == "0500000025"
    assert data["active"] is True
    assert "id" in data


def test_get_staff_api():
    create_staff(
        Staff(
            name="GET Staff",
            phone="0500000026",
        )
    )

    response = client.get("/staff")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert all(staff["active"] is True for staff in data)


def test_get_staff_by_id_api():
    created_staff = create_staff(
        Staff(
            name="API Staff By ID",
            phone="0500000027",
        )
    )

    response = client.get(
        f"/staff/{created_staff['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == created_staff["id"]
    assert data["name"] == "API Staff By ID"


def test_get_staff_by_id_api_not_found():
    response = client.get(
        "/staff/000000000000000000000000"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Staff not found"



def test_staff_can_be_linked_to_service():
    staff = Staff(
        name="Service Staff",
        phone="0500000028",
        service_ids=[
            "6a779ed59b6b145fcfe108ab"
        ],
    )

    created_staff = create_staff(staff)

    assert created_staff["service_ids"] == [
        "6a779ed59b6b145fcfe108ab"
    ]




def test_get_staff_by_service_id():
    service_id = "6a779ed59b6b145fcfe108ab"

    linked_staff = Staff(
        name="Linked Staff",
        phone="0500000029",
        service_ids=[service_id],
    )

    unlinked_staff = Staff(
        name="Unlinked Staff",
        phone="0500000030",
        service_ids=[],
    )

    created_linked = create_staff(linked_staff)
    created_unlinked = create_staff(unlinked_staff)

    staff_members = get_staff_by_service_id(service_id)

    staff_ids = [
        staff["id"]
        for staff in staff_members
    ]

    assert created_linked["id"] in staff_ids
    assert created_unlinked["id"] not in staff_ids