from datetime import datetime, timezone
from typing import Any
from api.schemas.conversation import BookingContext, ConversationState
from bson import ObjectId
from bson.errors import InvalidId

from database.connection import database


conversations_collection = database["conversations"]


def create_conversation() -> dict[str, Any]:
    now = datetime.now(timezone.utc)

    conversation_data = {
        "state": ConversationState.ACTIVE,
        "booking_context": BookingContext().model_dump(),
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


def update_conversation_state(
    conversation_id: str,
    state: ConversationState,
) -> dict[str, Any] | None:
    try:
        object_id = ObjectId(conversation_id)
    except (InvalidId, TypeError):
        return None

    now = datetime.now(timezone.utc)

    result = conversations_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "state": state,
                "updated_at": now,
            }
        },
    )

    if result.matched_count == 0:
        return None

    return get_conversation_by_id(conversation_id)




def update_booking_context(
    conversation_id: str,
    context: BookingContext,
) -> dict[str, Any] | None:
    try:
        object_id = ObjectId(conversation_id)
    except (InvalidId, TypeError):
        return None

    context_data = context.model_dump(exclude_none=True)

    update_data = {
        f"booking_context.{key}": value
        for key, value in context_data.items()
    }

    if not update_data:
        return get_conversation_by_id(conversation_id)

    update_data["updated_at"] = datetime.now(timezone.utc)

    result = conversations_collection.update_one(
        {"_id": object_id},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        return None

    return get_conversation_by_id(conversation_id)