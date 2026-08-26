from datetime import datetime

import pytest

from ai_core.business_action import BusinessAction
from ai_core.decision import NextAction
from ai_core.decision_engine import make_decision
from ai_core.intent import Intent
from ai_core.missing_fields import MissingField
from api.schemas.conversation import BookingContext


def test_book_calls_create_booking_when_context_is_complete():
    context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
        customer_phone="0501234567",
        booking_datetime=datetime(2026, 8, 26, 10, 0),
    )

    decision = make_decision(Intent.BOOK, context)

    assert decision.missing_fields == ()
    assert decision.next_action == NextAction.CALL_TOOL
    assert decision.business_action == BusinessAction.CREATE_BOOKING


def test_book_asks_user_when_context_is_incomplete():
    context = BookingContext(
        service_id="service-123",
    )

    decision = make_decision(Intent.BOOK, context)

    assert decision.next_action == NextAction.ASK_USER
    assert decision.business_action is None
    assert MissingField.CUSTOMER_NAME in decision.missing_fields
    assert MissingField.CUSTOMER_PHONE in decision.missing_fields
    assert MissingField.BOOKING_DATETIME in decision.missing_fields


def test_check_availability_calls_available_times_when_context_is_complete():
    context = BookingContext(
        service_id="service-123",
        staff_id="staff-123",
        booking_datetime=datetime(2026, 8, 26, 10, 0),
    )

    decision = make_decision(
        Intent.CHECK_AVAILABILITY,
        context,
    )

    assert decision.missing_fields == ()
    assert decision.next_action == NextAction.CALL_TOOL
    assert (
        decision.business_action
        == BusinessAction.GET_AVAILABLE_TIMES
    )


def test_check_availability_asks_for_missing_context():
    context = BookingContext(
        service_id="service-123",
    )

    decision = make_decision(
        Intent.CHECK_AVAILABILITY,
        context,
    )

    assert decision.next_action == NextAction.ASK_USER
    assert decision.business_action is None
    assert decision.missing_fields == (
        MissingField.STAFF_ID,
        MissingField.BOOKING_DATETIME,
    )


def test_get_services_calls_get_services_tool():
    decision = make_decision(
        Intent.GET_SERVICES,
        BookingContext(),
    )

    assert decision.missing_fields == ()
    assert decision.next_action == NextAction.CALL_TOOL
    assert decision.business_action == BusinessAction.GET_SERVICES


def test_get_staff_calls_get_staff_tool():
    decision = make_decision(
        Intent.GET_STAFF,
        BookingContext(),
    )

    assert decision.missing_fields == ()
    assert decision.next_action == NextAction.CALL_TOOL
    assert decision.business_action == BusinessAction.GET_STAFF


@pytest.mark.parametrize(
    "intent",
    (
        Intent.CANCEL,
        Intent.RESCHEDULE,
        Intent.UNKNOWN,
    ),
)
def test_unsupported_intents_are_rejected(intent):
    with pytest.raises(
        ValueError,
        match="Decision logic is not defined",
    ):
        make_decision(
            intent,
            BookingContext(),
        )
