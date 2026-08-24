from ai_core.business_tools import get_services, get_staff


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
