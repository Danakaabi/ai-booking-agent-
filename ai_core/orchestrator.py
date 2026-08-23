from typing import Any

from ai_core.context_preparation import prepare_booking_context
from ai_core.decision import AIDecision, NextAction
from ai_core.decision_engine import make_decision
from ai_core.entity_extractor import extract_entities
from ai_core.entity_resolver import resolve_entities
from ai_core.intent import Intent
from ai_core.intent_detector import detect_intent
from api.schemas.conversation import BookingContext


def process_message(
    message: str,
    *,
    current_context: BookingContext,
    services_by_id: dict[str, dict[str, Any]],
    staff_members: list[dict[str, Any]],
) -> tuple[AIDecision, BookingContext]:
    """Process a user message through the deterministic AI core."""

    intent = detect_intent(message)

    if intent is Intent.UNKNOWN:
        return (
            AIDecision(
                intent=Intent.UNKNOWN,
                next_action=NextAction.UNKNOWN,
            ),
            BookingContext(),
        )

    service_names = tuple(
        service["name"]
        for service in services_by_id.values()
        if isinstance(service.get("name"), str)
    )

    staff_names = tuple(
        staff["name"]
        for staff in staff_members
        if isinstance(staff.get("name"), str)
    )

    entities = extract_entities(
        message,
        service_names=service_names,
        staff_names=staff_names,
    )

    resolved = resolve_entities(
        entities,
        services_by_id=services_by_id,
        staff_members=staff_members,
    )

    context_update = prepare_booking_context(
        entities,
        resolved,
    )

    merged_context = current_context.model_copy(
        update=context_update.model_dump(exclude_none=True)
    )

    decision = make_decision(
        intent,
        merged_context,
        entities=entities,
    )

    return decision, context_update
