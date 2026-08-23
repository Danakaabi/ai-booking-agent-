import pytest
from pydantic import ValidationError

from ai_core.resolved_entities import ResolvedEntities


def test_resolved_entities_can_be_empty():
    entities = ResolvedEntities()

    assert entities.service_id is None
    assert entities.staff_id is None


def test_resolved_entities_accept_partial_resolution():
    entities = ResolvedEntities(
        service_id="service-123",
    )

    assert entities.service_id == "service-123"
    assert entities.staff_id is None


def test_resolved_entities_accept_complete_resolution():
    entities = ResolvedEntities(
        service_id="service-123",
        staff_id="staff-123",
    )

    assert entities.service_id == "service-123"
    assert entities.staff_id == "staff-123"


def test_resolved_entities_reject_empty_id():
    with pytest.raises(ValidationError):
        ResolvedEntities(
            service_id="",
        )

from ai_core.entities import ExtractedEntities
from ai_core.entity_resolver import resolve_entities


def test_resolve_entities_resolves_service_id():
    entities = ExtractedEntities(
        service_name="Haircut",
    )

    result = resolve_entities(
        entities,
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[],
    )

    assert result.service_id == "service-123"
    assert result.staff_id is None


def test_resolve_entities_resolves_staff_id():
    entities = ExtractedEntities(
        staff_name="Sara",
    )

    result = resolve_entities(
        entities,
        services_by_id={},
        staff_members=[
            {
                "id": "staff-123",
                "name": "Sara",
            }
        ],
    )

    assert result.service_id is None
    assert result.staff_id == "staff-123"


def test_resolve_entities_is_case_insensitive():
    entities = ExtractedEntities(
        service_name="haircut",
        staff_name="sara",
    )

    result = resolve_entities(
        entities,
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[
            {
                "id": "staff-123",
                "name": "Sara",
            }
        ],
    )

    assert result.service_id == "service-123"
    assert result.staff_id == "staff-123"


def test_resolve_entities_returns_none_for_unknown_names():
    entities = ExtractedEntities(
        service_name="Unknown Service",
        staff_name="Unknown Staff",
    )

    result = resolve_entities(
        entities,
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[
            {
                "id": "staff-123",
                "name": "Sara",
            }
        ],
    )

    assert result.service_id is None
    assert result.staff_id is None
