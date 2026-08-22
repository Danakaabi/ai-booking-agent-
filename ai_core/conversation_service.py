from typing import Any

from api.schemas.conversation import (
    BookingContext,
    ConversationState,
    MessageCreate,
)


from ai_core.booking_engine import execute_booking_request

from database.repositories.conversations import(
    get_conversation_by_id,
    update_booking_context,
    update_conversation_state,


)
from api.schemas.booking import BookingCreate

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

def build_booking_from_context(
    context: BookingContext,
) -> BookingCreate | None:
    required_fields = (
        context.service_id,
        context.customer_name,
        context.customer_phone,
        context.booking_datetime,
    )

    if any(value is None for value in required_fields):
        return None

    return BookingCreate(
        service_id=context.service_id,
        customer_name=context.customer_name,
        customer_phone=context.customer_phone,
        booking_datetime=context.booking_datetime,
        staff_id=context.staff_id,
    )


def execute_booking_from_conversation(
    conversation_id: str,
) -> tuple[dict | None, str | None]:
    conversation = get_conversation_by_id(conversation_id)

    if conversation is None:
        return None, "Conversation not found"

    context = BookingContext(
        **conversation["booking_context"]
    )

    booking = build_booking_from_context(context)

    if booking is None:
        return None, "Booking context is incomplete"

    return execute_booking_request(booking)