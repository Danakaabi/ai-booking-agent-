from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId

from database.connection import database


conversations_collection = database["conversations"]


def create_conversation() -> dict[str, Any]:
    now = datetime.now(timezone.utc)

    conversation_data = {
        "created_at": now,
        "updated_at": now,
    }

    result = conversations_collection.insert_one(conversation_data)

    conversation_data.pop("_id", None)
    conversation_data["id"] = str(result.inserted_id)

    return conversation_data


def get_conversation_by_id(
    conversation_id: str,
) -> dict[str, Any] | None:
    try:
        object_id = ObjectId(conversation_id)
    except (InvalidId, TypeError):
        return None

    conversation = conversations_collection.find_one(
        {"_id": object_id}
    )

    if conversation is None:
        return None

    conversation["id"] = str(conversation.pop("_id"))

    return conversation