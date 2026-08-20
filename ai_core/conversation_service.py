from typing import Any

from api.schemas.conversation import MessageCreate
from database.repositories.conversations import get_conversation_by_id
from database.repositories.messages import (
    create_message,
    get_messages_by_conversation_id,
)

def add_message_to_conversation(
    conversation_id: str,
    message: MessageCreate,
) -> dict[str, Any] | None:
    conversation = get_conversation_by_id(conversation_id)

    if conversation is None:
        return None

    return create_message(
        conversation_id=conversation_id,
        message=message,
    )


def get_conversation_history(
    conversation_id: str,
) -> list[dict[str, Any]] | None:
    conversation = get_conversation_by_id(conversation_id)

    if conversation is None:
        return None

    return get_messages_by_conversation_id(conversation_id)