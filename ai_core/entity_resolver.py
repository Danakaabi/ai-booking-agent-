from typing import Any

from ai_core.entities import ExtractedEntities
from ai_core.resolved_entities import ResolvedEntities


def _normalize_name(value: str) -> str:
    return value.strip().casefold()


def _resolve_service_id(
    service_name: str | None,
    services_by_id: dict[str, dict[str, Any]],
) -> str | None:
    if service_name is None:
        return None

    normalized_name = _normalize_name(service_name)

    for service_id, service in services_by_id.items():
        name = service.get("name")

        if (
            isinstance(name, str)
            and _normalize_name(name) == normalized_name
        ):
            return service_id

    return None


def _resolve_staff_id(
    staff_name: str | None,
    staff_members: list[dict[str, Any]],
) -> str | None:
    if staff_name is None:
        return None

    normalized_name = _normalize_name(staff_name)

    for staff in staff_members:
        name = staff.get("name")
        staff_id = staff.get("id")

        if (
            isinstance(name, str)
            and isinstance(staff_id, str)
            and _normalize_name(name) == normalized_name
        ):
            return staff_id

    return None


def resolve_entities(
    entities: ExtractedEntities,
    *,
    services_by_id: dict[str, dict[str, Any]],
    staff_members: list[dict[str, Any]],
) -> ResolvedEntities:
    """Resolve extracted entity names to internal system identifiers."""

    return ResolvedEntities(
        service_id=_resolve_service_id(
            entities.service_name,
            services_by_id,
        ),
        staff_id=_resolve_staff_id(
            entities.staff_name,
            staff_members,
        ),
    )
