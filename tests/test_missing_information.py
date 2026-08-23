from datetime import datetime

from ai_core.intent import Intent
from ai_core.missing_fields import MissingField
from ai_core.missing_information import detect_missing_fields
from api.schemas.conversation import BookingContext


def test_book_intent_reports_all_required_fields_when_context_is_empty():
    missing = detect_missing_fields(
        Intent.BOOK,
        BookingContext(),
    )

    assert missing == (
        MissingField.SERVICE_ID,
        MissingField.CUSTOMER_NAME,
        MissingField.CUSTOMER_PHONE,
        MissingField.BOOKING_DATETIME,
    )


def test_book_intent_reports_only_missing_fields():
    context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
    )

    missing = detect_missing_fields(
        Intent.BOOK,
        context,
    )

    assert missing == (
        MissingField.CUSTOMER_PHONE,
        MissingField.BOOKING_DATETIME,
    )


def test_book_intent_has_no_missing_fields_when_context_is_complete():
    context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
        customer_phone="0501234567",
        booking_datetime=datetime(2026, 8, 24, 17, 0),
    )

    missing = detect_missing_fields(
        Intent.BOOK,
        context,
    )

    assert missing == ()


def test_book_intent_does_not_require_staff_id():
    context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
        customer_phone="0501234567",
        booking_datetime=datetime(2026, 8, 24, 17, 0),
        staff_id=None,
    )

    missing = detect_missing_fields(
        Intent.BOOK,
        context,
    )

    assert MissingField.STAFF_ID not in missing
    assert missing == ()


def test_missing_field_detection_rejects_unsupported_intent():
    import pytest

    with pytest.raises(
        ValueError,
        match="Missing-field detection is not defined",
    ):
        detect_missing_fields(
            Intent.CANCEL,
            BookingContext(),
        )
