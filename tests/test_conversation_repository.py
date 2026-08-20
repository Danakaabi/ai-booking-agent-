from database.repositories.conversations import (
    conversations_collection,
    create_conversation,
    get_conversation_by_id,
)
from bson import ObjectId

def test_create_conversation():
    conversation = create_conversation()

    try:
        assert "id" in conversation
        assert "created_at" in conversation
        assert "updated_at" in conversation
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