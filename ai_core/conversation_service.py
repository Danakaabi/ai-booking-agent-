from typing import Any

from api.schemas.conversation import (
    BookingContext,
    ConversationState,
    MessageCreate,
)
from database.repositories.conversations import(
    get_conversation_by_id,
    update_booking_context,
    update_conversation_state,


)

from api.schemas.conversation import ConversationState

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



def change_conversation_state(
    conversation_id: str,
    state: ConversationState,
) -> dict[str, Any] | None:
    conversation = get_conversation_by_id(conversation_id)

    if conversation is None:
        return None

    return update_conversation_state(
        conversation_id=conversation_id,
        state=state,
    )


def update_conversation_booking_context(
    conversation_id: str,
    context: BookingContext,
) -> dict[str, Any] | None:
    conversation = get_conversation_by_id(conversation_id)

    if conversation is None:
        return None

    return update_booking_context(
        conversation_id=conversation_id,
        context=context,
    )