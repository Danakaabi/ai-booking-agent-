from ai_core.decision import AIDecision, NextAction
from ai_core.missing_fields import MissingField


CLARIFICATION_MESSAGES: dict[MissingField, str] = {
    MissingField.SERVICE_ID: "Which service would you like to book?",
    MissingField.CUSTOMER_NAME: "What name should I use for the booking?",
    MissingField.CUSTOMER_PHONE: "What phone number should I use for the booking?",
    MissingField.BOOKING_DATETIME: "What date and time would you like to book?",
    MissingField.STAFF_ID: "Which staff member would you prefer?",
}


def generate_response(decision: AIDecision) -> str:
    """Generate a deterministic user-facing response from an AI decision."""

    if decision.next_action is NextAction.ASK_USER:
        if not decision.missing_fields:
            raise ValueError(
                "ASK_USER decision requires at least one missing field"
            )

        missing_field = decision.missing_fields[0]

        return CLARIFICATION_MESSAGES[missing_field]

    if decision.next_action is NextAction.UNKNOWN:
        return "I could not understand your request. Please try again."

    raise ValueError(
        f"Response generation is not defined for action: "
        f"{decision.next_action.value}"
    )
