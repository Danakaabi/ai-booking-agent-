from bson import ObjectId

from ai_core.conversation_service import (
    add_message_to_conversation,
    get_conversation_history,
    change_conversation_state,
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
)
from database.repositories.messages import messages_collection


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