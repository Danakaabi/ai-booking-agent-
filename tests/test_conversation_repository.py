from ai_core.intent import Intent
from database.repositories.conversations import (
    conversations_collection,
    create_conversation,
    get_conversation_by_id,
    update_conversation_state,
    update_booking_context,
    update_active_intent,

)
from api.schemas.conversation import(
    BookingContext,
    ConversationState,
)

from bson import ObjectId

def test_create_conversation():
    conversation = create_conversation()

    try:
        assert "id" in conversation
        assert conversation["state"] == ConversationState.ACTIVE
        assert conversation["active_intent"] is None
        assert "created_at" in conversation
        assert "updated_at" in conversation
        assert "booking_context" in conversation
        assert conversation["booking_context"] == {
            "service_id": None,
            "customer_name": None,
            "customer_phone": None,
            "booking_datetime": None,
            "staff_id": None,
        }
    finally:
        conversations_collection.delete_one(
            {"id_ ":ObjectId(conversation["id"])}
        )


def test_get_conversation_by_id():
    created = create_conversation()

    try:
        conversation = get_conversation_by_id(created["id"])

        assert conversation is not None
        assert conversation["id"] == created["id"]
        assert "created_at" in conversation
        assert "updated_at" in conversation
    finally:
        conversations_collection.delete_one(
          {"id_": ObjectId(created["id"])}
        )


def test_get_conversation_by_invalid_id_returns_none():
    conversation = get_conversation_by_id("invalid-id")

    assert conversation is None


def test_update_conversation_state():
    conversation = create_conversation()

    try:
        updated = update_conversation_state(
            conversation["id"],
            ConversationState.COMPLETED,
        )

        assert updated is not None
        assert updated["id"] == conversation["id"]
        assert updated["state"] == ConversationState.COMPLETED

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )

def test_update_conversation_state_returns_none_for_invalid_id():
    result = update_conversation_state(
        "invalid-id",
        ConversationState.COMPLETED,
    )

    assert result is None


def test_update_conversation_state_returns_none_for_missing_conversation():
    result = update_conversation_state(
        "000000000000000000000000",
        ConversationState.COMPLETED,
    )

    assert result is None



def test_update_booking_context_preserves_existing_data():
    conversation = create_conversation()

    try:
        first_update = update_booking_context(
            conversation["id"],
            BookingContext(
                service_id="service-123",
            ),
        )

        assert first_update is not None
        assert first_update["booking_context"]["service_id"] == "service-123"

        second_update = update_booking_context(
            conversation["id"],
            BookingContext(
                customer_name="Dana",
            ),
        )

        assert second_update is not None
        assert second_update["booking_context"]["service_id"] == "service-123"
        assert second_update["booking_context"]["customer_name"] == "Dana"

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )

def test_update_booking_context_returns_none_for_invalid_id():
    result = update_booking_context(
        "invalid-id",
        BookingContext(
            customer_name="Dana",
        ),
    )

    assert result is None

def test_update_booking_context_returns_none_for_missing_conversation():
    result = update_booking_context(
        "000000000000000000000000",
        BookingContext(
            customer_name="Dana",
        ),
    )

    assert result is None

def test_update_active_intent():
    conversation = create_conversation()

    try:
        updated = update_active_intent(
            conversation["id"],
            Intent.BOOK,
        )

        assert updated is not None
        assert updated["active_intent"] == Intent.BOOK

    finally:
        conversations_collection.delete_one(
            {"_id": ObjectId(conversation["id"])}
        )
