from datetime import datetime

import pytest

from ai_core.decision import NextAction
from ai_core.decision_engine import make_decision
from ai_core.intent import Intent
from ai_core.missing_fields import MissingField
from api.schemas.conversation import BookingContext


def test_book_decision_asks_user_when_required_information_is_missing():
    context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
    )

    decision = make_decision(
        Intent.BOOK,
        context,
    )

    assert decision.intent == Intent.BOOK
    assert decision.next_action == NextAction.ASK_USER
    assert decision.missing_fields == (
        MissingField.CUSTOMER_PHONE,
        MissingField.BOOKING_DATETIME,
    )


def test_book_decision_calls_tool_when_context_is_complete():
    context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
        customer_phone="0501234567",
        booking_datetime=datetime(2026, 8, 24, 17, 0),
    )

    decision = make_decision(
        Intent.BOOK,
        context,
    )

    assert decision.intent == Intent.BOOK
    assert decision.next_action == NextAction.CALL_TOOL
    assert decision.missing_fields == ()


def test_decision_engine_rejects_unsupported_intent():
    with pytest.raises(
        ValueError,
        match="Decision logic is not defined",
    ):
        make_decision(
            Intent.CANCEL,
            BookingContext(),
        )


def test_book_decision_preserves_extracted_entities():
    from ai_core.entities import ExtractedEntities

    entities = ExtractedEntities(
        service_name="Haircut",
        customer_phone="0501234567",
    )

    decision = make_decision(
        Intent.BOOK,
        BookingContext(),
        entities=entities,
    )

    assert decision.entities == entities
    assert decision.entities.service_name == "Haircut"
    assert decision.entities.customer_phone == "0501234567"
