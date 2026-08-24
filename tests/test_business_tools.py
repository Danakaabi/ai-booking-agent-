from datetime import date, datetime

from ai_core.business_tools import (
    get_available_times,
    get_services,
    get_staff,
)


def test_get_services_reuses_existing_repository(monkeypatch):
    expected_services = [
        {
            "id": "service-123",
            "name": "Haircut",
            "duration_minutes": 60,
            "price": 85,
            "active": True,
        }
    ]

    def fake_get_all_services():
        return expected_services

    monkeypatch.setattr(
        "ai_core.business_tools.get_all_services",
        fake_get_all_services,
    )

    result = get_services()

    assert result == expected_services


def test_get_staff_reuses_existing_repository(monkeypatch):
    expected_staff = [
        {
            "id": "staff-123",
            "name": "Sara",
            "active": True,
        }
    ]

    def fake_get_all_staff():
        return expected_staff

    monkeypatch.setattr(
        "ai_core.business_tools.get_all_staff",
        fake_get_all_staff,
    )

    result = get_staff()

    assert result == expected_staff



def test_get_available_times_reuses_existing_availability_logic(monkeypatch):
    expected_slots = [
        datetime(2026, 8, 24, 9, 0),
        datetime(2026, 8, 24, 9, 30),
    ]

    def fake_get_service_by_id(service_id: str):
        assert service_id == "service-123"
        return {
            "id": service_id,
            "name": "Haircut",
            "duration_minutes": 60,
            "price": 85,
            "active": True,
        }

    def fake_get_staff_availability(staff_id: str):
        assert staff_id == "staff-123"
        return [
            {
                "staff_id": staff_id,
                "day_of_week": "monday",
                "start_time": "09:00:00",
                "end_time": "12:00:00",
                "active": True,
            }
        ]

    def fake_generate_available_slots(
        *,
        staff_id: str,
        target_date: date,
        start_hour: int,
        end_hour: int,
        duration_minutes: int,
        interval_minutes: int = 30,
    ):
        assert staff_id == "staff-123"
        assert target_date == date(2026, 8, 24)
        assert start_hour == 9
        assert end_hour == 12
        assert duration_minutes == 60
        assert interval_minutes == 30
        return expected_slots

    monkeypatch.setattr(
        "ai_core.business_tools.get_service_by_id",
        fake_get_service_by_id,
    )
    monkeypatch.setattr(
        "ai_core.business_tools.get_staff_availability",
        fake_get_staff_availability,
    )
    monkeypatch.setattr(
        "ai_core.business_tools.generate_available_slots",
        fake_generate_available_slots,
    )

    result = get_available_times(
        staff_id="staff-123",
        service_id="service-123",
        target_date=date(2026, 8, 24),
    )

    assert result == expected_slots


def test_get_available_times_returns_empty_when_service_not_found(monkeypatch):
    monkeypatch.setattr(
        "ai_core.business_tools.get_service_by_id",
        lambda service_id: None,
    )

    result = get_available_times(
        staff_id="staff-123",
        service_id="missing-service",
        target_date=date(2026, 8, 24),
    )

    assert result == []


def test_get_available_times_returns_empty_when_no_matching_schedule(monkeypatch):
    monkeypatch.setattr(
        "ai_core.business_tools.get_service_by_id",
        lambda service_id: {
            "id": service_id,
            "name": "Haircut",
            "duration_minutes": 60,
            "price": 85,
            "active": True,
        },
    )

    monkeypatch.setattr(
        "ai_core.business_tools.get_staff_availability",
        lambda staff_id: [],
    )

    result = get_available_times(
        staff_id="staff-123",
        service_id="service-123",
        target_date=date(2026, 8, 24),
    )

    assert result == []
