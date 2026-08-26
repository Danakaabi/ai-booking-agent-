from ai_core.intent import Intent
from ai_core.missing_fields import MissingField
from api.schemas.conversation import BookingContext


BOOK_REQUIRED_FIELDS: tuple[MissingField, ...] = (
    MissingField.SERVICE_ID,
    MissingField.CUSTOMER_NAME,
    MissingField.CUSTOMER_PHONE,
    MissingField.BOOKING_DATETIME,
)

AVAILABILITY_REQUIRED_FIELDS: tuple[MissingField, ...] = (
    MissingField.SERVICE_ID,
    MissingField.STAFF_ID,
    MissingField.BOOKING_DATETIME,
)


def detect_missing_fields(
    intent: Intent,
    context: BookingContext,
) -> tuple[MissingField, ...]:
    """Return required context fields that are still missing for an intent."""

    if intent is Intent.BOOK:
        required_fields = BOOK_REQUIRED_FIELDS

    elif intent is Intent.CHECK_AVAILABILITY:
        required_fields = AVAILABILITY_REQUIRED_FIELDS

    elif intent in (
        Intent.GET_SERVICES,
        Intent.GET_STAFF,
    ):
        required_fields = ()

    else:
        raise ValueError(
            f"Missing-field detection is not defined for intent: {intent.value}"
        )

    missing: list[MissingField] = []

    for field in required_fields:
        if getattr(context, field.value) is None:
            missing.append(field)

    return tuple(missing)
