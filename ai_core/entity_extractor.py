import re

from ai_core.entities import ExtractedEntities


PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+?\d[\d\s-]{6,18}\d)(?!\d)")


def _find_known_name(
    message: str,
    known_names: tuple[str, ...],
) -> str | None:
    for name in sorted(known_names, key=len, reverse=True):
        pattern = re.compile(
            rf"(?<!\w){re.escape(name)}(?!\w)",
            re.IGNORECASE,
        )

        if pattern.search(message):
            return name

    return None


def _extract_phone(message: str) -> str | None:
    match = PHONE_PATTERN.search(message)

    if match is None:
        return None

    return re.sub(r"[\s-]", "", match.group())


def extract_entities(
    message: str,
    *,
    service_names: tuple[str, ...] = (),
    staff_names: tuple[str, ...] = (),
) -> ExtractedEntities:
    """Extract deterministic entities from a user message."""

    return ExtractedEntities(
        service_name=_find_known_name(message, service_names),
        customer_phone=_extract_phone(message),
        staff_name=_find_known_name(message, staff_names),
    )
