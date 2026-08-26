from ai_core.business_action import BusinessAction
from ai_core.decision import AIDecision, NextAction
from ai_core.entities import ExtractedEntities
from ai_core.intent import Intent
from ai_core.missing_information import detect_missing_fields
from api.schemas.conversation import BookingContext


BUSINESS_ACTION_BY_INTENT: dict[Intent, BusinessAction] = {
    Intent.BOOK: BusinessAction.CREATE_BOOKING,
    Intent.CHECK_AVAILABILITY: BusinessAction.GET_AVAILABLE_TIMES,
    Intent.GET_SERVICES: BusinessAction.GET_SERVICES,
    Intent.GET_STAFF: BusinessAction.GET_STAFF,
}


def make_decision(
    intent: Intent,
    context: BookingContext,
    entities: ExtractedEntities | None = None,
) -> AIDecision:
    """Determine the next AI action for a supported conversation intent."""

    business_action = BUSINESS_ACTION_BY_INTENT.get(intent)

    if business_action is None:
        raise ValueError(
            f"Decision logic is not defined for intent: {intent.value}"
        )

    missing_fields = detect_missing_fields(
        intent,
        context,
    )

    next_action = (
        NextAction.ASK_USER
        if missing_fields
        else NextAction.CALL_TOOL
    )

    return AIDecision(
        intent=intent,
        entities=entities or ExtractedEntities(),
        missing_fields=missing_fields,
        next_action=next_action,
        business_action=(
            business_action
            if next_action is NextAction.CALL_TOOL
            else None
        ),
    )
