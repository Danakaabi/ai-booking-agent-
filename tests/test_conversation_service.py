from bson import ObjectId
from ai_core.decision import NextAction
from ai_core.intent import Intent
from datetime import date, datetime, timezone

from ai_core.conversation_service import (
    add_message_to_conversation,
    get_conversation_history,
    build_booking_from_context,
    change_conversation_state,
    execute_available_times_from_conversation,
    execute_booking_from_conversation,
    process_conversation_message,
    update_conversation_booking_context,
)
from api.schemas.conversation import (
     BookingContext,
     ConversationState, 
     MessageCreate,
     MessageRole,
)
from database.repositories.conversations import (
    conversations_collection,
    create_conversation,
    get_conversation_by_id,
)
from database.repositories.messages import messages_collection

from database.repositories.bookings import bookings_collection
from database.repositories.services import get_active_services_by_id

def test_add_message_to_existing_conversation():
    conversation = create_conversation()

    try:
        message = MessageCreate(
            role=MessageRole.USER,
            content="I want to book a haircut",
        )

        created_message = add_message_to_conversation(
            conversation_id=conversation["id"],
            message=message,
        )

        assert created_message is not None
        assert created_message["conversation_id"] == conversation["id"]
        assert created_message["content"] == "I want to book a haircut"

    finally:
        messages_collection.delete_many(
            {"conversation_id": conversation["id"]}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_add_message_to_non_existing_conversation_returns_none():
    message = MessageCreate(
        role=MessageRole.USER,
        content="Hello",
    )

    result = add_message_to_conversation(
        conversation_id="000000000000000000000000",
        message=message,
    )

    assert result is None



def test_get_conversation_history():
    conversation = create_conversation()

    try:
        # Existing conversation with no messages
        empty_history = get_conversation_history(
            conversation["id"]
        )

        assert empty_history == []

        # Add two messages
        add_message_to_conversation(
            conversation["id"],
            MessageCreate(
                role=MessageRole.USER,
                content="Hello",
            ),
        )

        add_message_to_conversation(
            conversation["id"],
            MessageCreate(
                role=MessageRole.ASSISTANT,
                content="Hi, how can I help?",
            ),
        )

        # Existing conversation with messages
        history = get_conversation_history(
            conversation["id"]
        )

        assert history is not None
        assert len(history) == 2
        assert history[0]["content"] == "Hello"
        assert history[1]["content"] == "Hi, how can I help?"

        # Missing conversation
        missing_history = get_conversation_history(
            "000000000000000000000000"
        )

        assert missing_history is None

    finally:
        messages_collection.delete_many(
            {"conversation_id": conversation["id"]}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_change_conversation_state():
    conversation = create_conversation()

    try:
        assert conversation["state"] == ConversationState.ACTIVE

        updated = change_conversation_state(
            conversation_id=conversation["id"],
            state=ConversationState.COMPLETED,
        )

        assert updated is not None
        assert updated["state"] == ConversationState.COMPLETED

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )

def test_update_conversation_booking_context_preserves_existing_data():
    conversation = create_conversation()

    try:
        first_update = update_conversation_booking_context(
            conversation_id=conversation["id"],
            context=BookingContext(
                service_id="service-123",
            ),
        )

        assert first_update is not None
        assert (
            first_update["booking_context"]["service_id"]
            == "service-123"
        )

        second_update = update_conversation_booking_context(
            conversation_id=conversation["id"],
            context=BookingContext(
                customer_name="Dana",
            ),
        )

        assert second_update is not None
        assert (
            second_update["booking_context"]["service_id"]
            == "service-123"
        )
        assert (
            second_update["booking_context"]["customer_name"]
            == "Dana"
        )

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_build_booking_from_partial_context_returns_none():
    context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
    )

    booking = build_booking_from_context(context)

    assert booking is None


def test_build_booking_from_complete_context_returns_booking_create():
    booking_datetime = datetime(
        2026,
        8,
        25,
        17,
        0,
        tzinfo=timezone.utc,
    )

    context = BookingContext(
        service_id="service-123",
        customer_name="Dana",
        customer_phone="0500000000",
        booking_datetime=booking_datetime,
        staff_id="staff-123",
    )

    booking = build_booking_from_context(context)

    assert booking is not None
    assert booking.service_id == "service-123"
    assert booking.customer_name == "Dana"
    assert booking.customer_phone == "0500000000"
    assert booking.booking_datetime == booking_datetime
    assert booking.staff_id == "staff-123"


def test_execute_booking_from_missing_conversation():
    booking, error = execute_booking_from_conversation(
        "000000000000000000000000"
    )

    assert booking is None
    assert error == "Conversation not found"

def test_execute_booking_from_incomplete_context():
    conversation = create_conversation()

    try:
        booking, error = execute_booking_from_conversation(
            conversation["id"]
        )

        assert booking is None
        assert error == "Booking context is incomplete"

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_execute_booking_from_complete_context_creates_booking():
    conversation = create_conversation()
    customer_name = "Conversation Booking Test"

    bookings_collection.delete_many(
        {"customer_name": customer_name}
    )

    try:
        update_conversation_booking_context(
            conversation_id=conversation["id"],
            context=BookingContext(
                service_id="6a779ed59b6b145fcfe108ab",
                customer_name=customer_name,
                customer_phone="0500000200",
                booking_datetime=datetime(
                    2026,
                    8,
                    20,
                    10,
                    0,
                ),
            ),
        )

        booking, error = execute_booking_from_conversation(
            conversation["id"]
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

def test_execute_booking_from_conversation_returns_booking_engine_error():
    conversation = create_conversation()

    try:
        update_conversation_booking_context(
            conversation_id=conversation["id"],
            context=BookingContext(
                service_id="000000000000000000000000",
                customer_name="Conversation Invalid Service Test",
                customer_phone="0500000300",
                booking_datetime=datetime(
                    2026,
                    8,
                    20,
                    10,
                    0,
                ),
            ),
        )

        booking, error = execute_booking_from_conversation(
            conversation["id"]
        )

        assert booking is None
        assert error == "Service not found"

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )

def test_process_conversation_message_persists_ai_context_update():
    conversation = create_conversation()
    services_by_id = get_active_services_by_id()

    haircut_service_id = next(
        service_id
        for service_id, service in services_by_id.items()
        if service["name"] == "Haircut"
    )

    try:
        decision = process_conversation_message(
            conversation_id=conversation["id"],
            message="I want to book Haircut",
        )

        assert decision is not None
        assert decision.intent == Intent.BOOK
        assert decision.next_action == NextAction.ASK_USER

        updated_conversation = get_conversation_by_id(
            conversation["id"]
        )

        assert updated_conversation is not None
        assert (
            updated_conversation["booking_context"]["service_id"]
            == haircut_service_id
        )

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_process_conversation_message_preserves_existing_context():
    conversation = create_conversation()
    services_by_id = get_active_services_by_id()

    haircut_service_id = next(
        service_id
        for service_id, service in services_by_id.items()
        if service["name"] == "Haircut"
    )

    try:
        update_conversation_booking_context(
            conversation_id=conversation["id"],
            context=BookingContext(
                customer_name="Dana",
            ),
        )

        decision = process_conversation_message(
            conversation_id=conversation["id"],
            message="I want to book Haircut",
        )

        assert decision is not None
        assert decision.intent == Intent.BOOK
        assert decision.next_action == NextAction.ASK_USER

        updated_conversation = get_conversation_by_id(
            conversation["id"]
        )

        assert updated_conversation is not None
        assert (
            updated_conversation["booking_context"]["service_id"]
            == haircut_service_id
        )
        assert (
            updated_conversation["booking_context"]["customer_name"]
            == "Dana"
        )

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_process_conversation_message_continues_booking_across_messages():
    conversation = create_conversation()

    try:
        first_decision = process_conversation_message(
            conversation_id=conversation["id"],
            message="I want to book Haircut",
        )

        assert first_decision is not None
        assert first_decision.intent == Intent.BOOK
        assert first_decision.next_action == NextAction.ASK_USER

        after_first_message = get_conversation_by_id(
            conversation["id"]
        )

        assert after_first_message is not None
        assert after_first_message["active_intent"] == Intent.BOOK
        assert (
            after_first_message["booking_context"]["service_id"]
            is not None
        )

        second_decision = process_conversation_message(
            conversation_id=conversation["id"],
            message="0501234567",
        )

        assert second_decision is not None
        assert second_decision.intent == Intent.BOOK
        assert second_decision.next_action == NextAction.ASK_USER

        after_second_message = get_conversation_by_id(
            conversation["id"]
        )

        assert after_second_message is not None
        assert (
            after_second_message["booking_context"]["service_id"]
            is not None
        )
        assert (
            after_second_message["booking_context"]["customer_phone"]
            == "0501234567"
        )

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_process_conversation_message_creates_assistant_clarification():
    conversation = create_conversation()

    try:
        decision = process_conversation_message(
            conversation_id=conversation["id"],
            message="I want to book Haircut",
        )

        assert decision is not None
        assert decision.intent == Intent.BOOK
        assert decision.next_action == NextAction.ASK_USER

        history = get_conversation_history(
            conversation["id"]
        )

        assert history is not None
        assert len(history) == 1
        assert history[0]["role"] == MessageRole.ASSISTANT
        assert (
            history[0]["content"]
            == "What name should I use for the booking?"
        )

    finally:
        messages_collection.delete_many(
            {"conversation_id": conversation["id"]}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_process_conversation_message_creates_unknown_assistant_response():
    conversation = create_conversation()

    try:
        decision = process_conversation_message(
            conversation_id=conversation["id"],
            message="Something completely unrelated",
        )

        assert decision is not None
        assert decision.intent == Intent.UNKNOWN
        assert decision.next_action == NextAction.UNKNOWN

        history = get_conversation_history(
            conversation["id"]
        )

        assert history is not None
        assert len(history) == 1
        assert history[0]["role"] == MessageRole.ASSISTANT
        assert (
            history[0]["content"]
            == "I could not understand your request. Please try again."
        )

    finally:
        messages_collection.delete_many(
            {"conversation_id": conversation["id"]}
        )

        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_execute_available_times_from_conversation_reuses_business_tool(
    monkeypatch,
):
    conversation = create_conversation()

    try:
        update_conversation_booking_context(
            conversation_id=conversation["id"],
            context=BookingContext(
                service_id="service-123",
                staff_id="staff-123",
                booking_datetime=datetime(
                    2026,
                    8,
                    24,
                    10,
                    0,
                ),
            ),
        )

        expected_slots = [
            datetime(2026, 8, 24, 9, 0),
            datetime(2026, 8, 24, 9, 30),
        ]

        def fake_get_available_times(
            staff_id: str,
            service_id: str,
            target_date: date,
        ):
            assert staff_id == "staff-123"
            assert service_id == "service-123"
            assert target_date == date(2026, 8, 24)
            return expected_slots

        monkeypatch.setattr(
            "ai_core.conversation_service.get_available_times",
            fake_get_available_times,
        )

        slots, error = execute_available_times_from_conversation(
            conversation["id"]
        )

        assert error is None
        assert slots == expected_slots

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


def test_process_conversation_message_continues_availability_across_messages():
    conversation = create_conversation()

    try:
        first_decision = process_conversation_message(
            conversation_id=conversation["id"],
            message="check availability",
        )

        assert first_decision is not None
        assert first_decision.intent == Intent.CHECK_AVAILABILITY
        assert first_decision.next_action == NextAction.ASK_USER

        after_first_message = get_conversation_by_id(
            conversation["id"]
        )

        assert after_first_message is not None
        assert (
            after_first_message["active_intent"]
            == Intent.CHECK_AVAILABILITY
        )

        second_decision = process_conversation_message(
            conversation_id=conversation["id"],
            message="Haircut",
        )

        assert second_decision is not None
        assert second_decision.intent == Intent.CHECK_AVAILABILITY
        assert second_decision.next_action == NextAction.ASK_USER

        after_second_message = get_conversation_by_id(
            conversation["id"]
        )

        assert after_second_message is not None
        assert (
            after_second_message["booking_context"]["service_id"]
            is not None
        )
        assert (
            after_second_message["active_intent"]
            == Intent.CHECK_AVAILABILITY
        )

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )


from ai_core.llm_output import LLMInterpretation


class FakeConversationLLMProvider:
    def interpret(self, message: str) -> LLMInterpretation:
        return LLMInterpretation(
            intent=Intent.BOOK,
            entities={
                "service_name": "Haircut",
                "customer_name": "Dana",
                "customer_phone": "0501234567",
                "booking_datetime": datetime(2026, 8, 24, 17, 0),
            },
        )


def test_process_conversation_message_can_use_llm_provider():
    conversation = create_conversation()

    try:
        decision = process_conversation_message(
            conversation_id=conversation["id"],
            message="Arrange my appointment please",
            llm_provider=FakeConversationLLMProvider(),
        )

        assert decision is not None
        assert decision.intent == Intent.BOOK
        assert decision.next_action == NextAction.CALL_TOOL

        updated_conversation = get_conversation_by_id(
            conversation["id"]
        )

        assert updated_conversation is not None
        assert (
            updated_conversation["booking_context"]["customer_name"]
            == "Dana"
        )
        assert (
            updated_conversation["booking_context"]["customer_phone"]
            == "0501234567"
        )

    finally:
        messages_collection.delete_many(
            {"conversation_id": conversation["id"]}
        )
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )
