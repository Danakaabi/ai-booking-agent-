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
    process_conversation_message,
    update_conversation_booking_context,
)
from api.schemas.conversation import BookingContext
from database.repositories.bookings import bookings_collection
from database.repositories.services import get_active_services_by_id
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


def test_ai_booking_flow_end_to_end():
    conversation = start_conversation()
    customer_name = "AI End To End Booking Test"

    services_by_id = get_active_services_by_id()

    haircut_service_id = next(
        service_id
        for service_id, service in services_by_id.items()
        if service["name"] == "Haircut"
    )

    bookings_collection.delete_many(
        {"customer_name": customer_name}
    )

    try:
        update_conversation_booking_context(
            conversation_id=conversation["id"],
            context=BookingContext(
                customer_name=customer_name,
                booking_datetime=datetime(
                    2026,
                    8,
                    20,
                    14,
                    0,
                ),
            ),
        )

        decision = process_conversation_message(
            conversation_id=conversation["id"],
            message="I want to book Haircut, my phone is 0500000500",
        )

        assert decision is not None
        assert decision.intent == Intent.BOOK
        assert decision.next_action == NextAction.CALL_TOOL
        assert (
            decision.business_action
            == BusinessAction.CREATE_BOOKING
        )

        booking, error = execute_business_action(
            decision,
            conversation_id=conversation["id"],
        )

        assert error is None
        assert booking is not None
        assert booking["customer_name"] == customer_name
        assert booking["service_id"] == haircut_service_id
        assert booking["customer_phone"] == "0500000500"
        assert "id" in booking

    finally:
        bookings_collection.delete_many(
            {"customer_name": customer_name}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_executor_routes_get_services_to_business_tool(monkeypatch):
    decision = AIDecision(
        intent=Intent.UNKNOWN,
        next_action=NextAction.CALL_TOOL,
        business_action=BusinessAction.GET_SERVICES,
    )

    expected_services = [
        {
            "id": "service-123",
            "name": "Haircut",
        }
    ]

    def fake_get_services():
        return expected_services

    monkeypatch.setattr(
        "ai_core.tool_executor.get_services",
        fake_get_services,
    )

    result = execute_business_action(
        decision,
        conversation_id="conversation-123",
    )

    assert result == (expected_services, None)


def test_executor_routes_get_staff_to_business_tool(monkeypatch):
    decision = AIDecision(
        intent=Intent.UNKNOWN,
        next_action=NextAction.CALL_TOOL,
        business_action=BusinessAction.GET_STAFF,
    )

    expected_staff = [
        {
            "id": "staff-123",
            "name": "Sara",
        }
    ]

    def fake_get_staff():
        return expected_staff

    monkeypatch.setattr(
        "ai_core.tool_executor.get_staff",
        fake_get_staff,
    )

    result = execute_business_action(
        decision,
        conversation_id="conversation-123",
    )

    assert result == (expected_staff, None)
