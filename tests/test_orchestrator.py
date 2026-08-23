from datetime import datetime

from ai_core.business_action import BusinessAction
from ai_core.decision import NextAction
from ai_core.intent import Intent
from ai_core.orchestrator import process_message
from api.schemas.conversation import BookingContext
from ai_core.missing_fields import MissingField

def test_process_message_combines_new_entities_with_existing_context():
    current_context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
        booking_datetime=datetime(2026, 8, 24, 17, 0),
    )

    decision, context_update = process_message(
        "I want to book, my phone is 0501234567",
        current_context=current_context,
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[],
    )

    assert decision.intent == Intent.BOOK
    assert decision.entities.customer_phone == "0501234567"
    assert decision.missing_fields == ()
    assert decision.next_action == NextAction.CALL_TOOL


def test_process_message_asks_user_when_context_is_still_incomplete():
    current_context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
    )

    decision, context_update = process_message(
        "I want to book, my phone is 0501234567",
        current_context=current_context,
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[],
    )

    assert decision.intent == Intent.BOOK
    assert decision.entities.customer_phone == "0501234567"
    assert decision.missing_fields == (
        MissingField.BOOKING_DATETIME,
    )
    assert decision.next_action == NextAction.ASK_USER


def test_process_message_resolves_service_name_during_full_flow():
    current_context = BookingContext(
        customer_name="Dana",
        customer_phone="0501234567",
        booking_datetime=datetime(2026, 8, 24, 17, 0),
    )

    decision, context_update = process_message(
        "I want to book Haircut",
        current_context=current_context,
        services_by_id={
            "service-123": {
                "name": "Haircut",
            }
        },
        staff_members=[],
    )

    assert decision.intent == Intent.BOOK
    assert decision.entities.service_name == "Haircut"
    assert decision.missing_fields == ()
    assert decision.next_action == NextAction.CALL_TOOL
    assert decision.business_action == BusinessAction.CREATE_BOOKING

    assert context_update.service_id == "service-123"
    assert context_update.customer_name is None
    assert context_update.customer_phone is None
    assert context_update.booking_datetime is None
    assert context_update.staff_id is None


def test_process_message_returns_unknown_decision_for_unknown_intent():
    decision, context_update = process_message(
        "Hello there",
        current_context=BookingContext(),
        services_by_id={},
        staff_members=[],
    )

    assert decision.intent == Intent.UNKNOWN
    assert decision.missing_fields == ()
    assert decision.next_action == NextAction.UNKNOWN
