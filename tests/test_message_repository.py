from bson import ObjectId

from api.schemas.conversation import MessageCreate, MessageRole
from database.repositories.messages import (
    create_message,
    messages_collection,
    get_messages_by_conversation_id,
)


def test_create_message():
    message = MessageCreate(
        role=MessageRole.USER,
        content="I want to book a haircut",
    )

    created = create_message(
        conversation_id="test-conversation-id",
        message=message,
    )

    try:
        assert "id" in created
        assert created["conversation_id"] == "test-conversation-id"
        assert created["role"] == MessageRole.USER
        assert created["content"] == "I want to book a haircut"
        assert "created_at" in created
    finally:
        messages_collection.delete_one(
            {"_id": ObjectId(created["id"])}
        )


def test_get_messages_by_conversation_id_returns_history_in_order():
    conversation_id = "history-test-conversation"

    messages_collection.delete_many(
        {"conversation_id": conversation_id}
    )

    try:
        create_message(
            conversation_id,
            MessageCreate(
                role=MessageRole.USER,
                content="Hello",
            ),
        )

        create_message(
            conversation_id,
            MessageCreate(
                role=MessageRole.ASSISTANT,
                content="Hi, how can I help?",
            ),
        )

        create_message(
            conversation_id,
            MessageCreate(
                role=MessageRole.USER,
                content="I want to book a haircut",
            ),
        )

        history = get_messages_by_conversation_id(
            conversation_id
        )

        assert len(history) == 3
        assert history[0]["content"] == "Hello"
        assert history[1]["content"] == "Hi, how can I help?"
        assert history[2]["content"] == "I want to book a haircut"

    finally:
        messages_collection.delete_many(
            {"conversation_id": conversation_id}
        )


def test_get_messages_only_returns_requested_conversation():
    conversation_a = "conversation-a"
    conversation_b = "conversation-b"

    messages_collection.delete_many(
        {
            "conversation_id": {
                "$in": [conversation_a, conversation_b]
            }
        }
    )

    try:
        create_message(
            conversation_a,
            MessageCreate(
                role=MessageRole.USER,
                content="Message from A",
            ),
        )

        create_message(
            conversation_b,
            MessageCreate(
                role=MessageRole.USER,
                content="Message from B",
            ),
        )

        history = get_messages_by_conversation_id(
            conversation_a
        )

        assert len(history) == 1
        assert history[0]["conversation_id"] == conversation_a
        assert history[0]["content"] == "Message from A"

    finally:
        messages_collection.delete_many(
            {
                "conversation_id": {
                    "$in": [conversation_a, conversation_b]
                }
            }
        )