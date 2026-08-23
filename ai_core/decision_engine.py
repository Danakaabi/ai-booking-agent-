from ai_core.decision import AIDecision, NextAction
from ai_core.entities import ExtractedEntities
from ai_core.intent import Intent
from ai_core.missing_information import detect_missing_fields
from api.schemas.conversation import BookingContext


def make_decision(
    intent: Intent,
    context: BookingContext,
    entities: ExtractedEntities | None = None,
) -> AIDecision:
    """Determine the next AI action for a supported conversation intent."""

    if intent is not Intent.BOOK:
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
    )
