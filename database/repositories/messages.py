from datetime import datetime, timezone
from typing import Any

from api.schemas.conversation import MessageCreate
from database.connection import database


messages_collection = database["messages"]


def create_message(
    conversation_id: str,
    message: MessageCreate,
) -> dict[str, Any]:
    message_data = message.model_dump()

    message_data["conversation_id"] = conversation_id
    message_data["created_at"] = datetime.now(timezone.utc)

    result = messages_collection.insert_one(message_data)

    message_data.pop("_id", None)
    message_data["id"] = str(result.inserted_id)

    return message_data

def get_messages_by_conversation_id(
    conversation_id: str,
) -> list[dict[str, Any]]:
    messages = list(
        messages_collection.find(
            {"conversation_id": conversation_id}
        ).sort("created_at", 1)
    )

    for message in messages:
        message["id"] = str(message.pop("_id"))

    return messages