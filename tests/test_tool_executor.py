import pytest

from ai_core.business_action import BusinessAction
from ai_core.decision import AIDecision, NextAction
from ai_core.intent import Intent
from ai_core.tool_executor import execute_business_action


def test_executor_rejects_decision_that_does_not_request_tool_execution():
    decision = AIDecision(
        intent=Intent.BOOK,
        next_action=NextAction.ASK_USER,
        business_action=BusinessAction.CREATE_BOOKING,
    )

    with pytest.raises(
        ValueError,
        match="AI decision does not request tool execution",
    ):
        execute_business_action(
            decision,
            conversation_id="conversation-123",
        )


def test_executor_routes_create_booking_to_conversation_service(monkeypatch):
    decision = AIDecision(
        intent=Intent.BOOK,
        next_action=NextAction.CALL_TOOL,
        business_action=BusinessAction.CREATE_BOOKING,
    )

    expected_result = (
        {
            "id": "booking-123",
            "service_id": "service-123",
        },
        None,
    )

    def fake_execute_booking_from_conversation(
        conversation_id: str,
    ):
        assert conversation_id == "conversation-123"
        return expected_result

    monkeypatch.setattr(
        "ai_core.tool_executor.execute_booking_from_conversation",
        fake_execute_booking_from_conversation,
    )

    result = execute_business_action(
        decision,
        conversation_id="conversation-123",
    )

    assert result == expected_result


def test_executor_rejects_missing_business_action():
    decision = AIDecision(
        intent=Intent.BOOK,
        next_action=NextAction.CALL_TOOL,
        business_action=None,
    )

    with pytest.raises(
        ValueError,
        match="Unsupported AI business action",
    ):
        execute_business_action(
            decision,
            conversation_id="conversation-123",
        )

from datetime import datetime

from bson import ObjectId

from ai_core.conversation_service import (
    start_conversation,
    update_conversation_booking_context,
)
from api.schemas.conversation import BookingContext
from database.repositories.bookings import bookings_collection
from database.repositories.conversations import conversations_collection


def test_executor_creates_booking_through_existing_conversation_flow():
    conversation = start_conversation()
    customer_name = "AI Tool Executor Booking Test"

    bookings_collection.delete_many(
        {"customer_name": customer_name}
    )

    try:
        update_conversation_booking_context(
            conversation_id=conversation["id"],
            context=BookingContext(
                service_id="6a779ed59b6b145fcfe108ab",
                customer_name=customer_name,
                customer_phone="0500000400",
                booking_datetime=datetime(
                    2026,
                    8,
                    20,
                    12,
                    0,
                ),
            ),
        )

        decision = AIDecision(
            intent=Intent.BOOK,
            next_action=NextAction.CALL_TOOL,
            business_action=BusinessAction.CREATE_BOOKING,
        )

        booking, error = execute_business_action(
            decision,
            conversation_id=conversation["id"],
        )

        assert error is None
        assert booking is not None
        assert booking["customer_name"] == customer_name
        assert booking["service_id"] == "6a779ed59b6b145fcfe108ab"
        assert "id" in booking

    finally:
        bookings_collection.delete_many(
            {"customer_name": customer_name}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )
