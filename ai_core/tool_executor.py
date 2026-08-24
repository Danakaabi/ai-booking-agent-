from ai_core.business_action import BusinessAction
from ai_core.business_tools import get_services, get_staff
from ai_core.conversation_service import execute_booking_from_conversation
from ai_core.decision import AIDecision, NextAction


def execute_business_action(
    decision: AIDecision,
    *,
    conversation_id: str,
) -> tuple[dict | None, str | None]:
    """Execute an approved AI business action through existing business logic."""

    if decision.next_action is not NextAction.CALL_TOOL:
        raise ValueError(
            "AI decision does not request tool execution"
        )

    if decision.business_action is BusinessAction.GET_SERVICES:
        return get_services(), None

    if decision.business_action is BusinessAction.GET_STAFF:
        return get_staff(), None

    if decision.business_action is BusinessAction.CREATE_BOOKING:
        return execute_booking_from_conversation(
            conversation_id
        )

    raise ValueError(
        "Unsupported AI business action"
    )
