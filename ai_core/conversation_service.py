from typing import Any

from api.schemas.conversation import (
    BookingContext,
    ConversationState,
    MessageCreate,
    MessageRole,
)


from ai_core.booking_engine import execute_booking_request
from ai_core.business_tools import get_available_times
from ai_core.decision import AIDecision, NextAction
from ai_core.orchestrator import process_message
from ai_core.response_generator import generate_response
from ai_core.intent import Intent
from ai_core.llm_provider import LLMProvider

from database.repositories.conversations import(
    create_conversation,
    get_conversation_by_id,
    update_booking_context,
    update_conversation_state,
    update_active_intent,


)
from api.schemas.booking import BookingCreate

from api.schemas.conversation import ConversationState

from database.repositories.services import get_active_services_by_id
from database.repositories.staff import get_all_staff

from database.repositories.messages import (
    create_message,
    get_messages_by_conversation_id,
)

def start_conversation() -> dict[str, Any]:
    return create_conversation()


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



def execute_available_times_from_conversation(
    conversation_id: str,
) -> tuple[list | None, str | None]:
    conversation = get_conversation_by_id(conversation_id)

    if conversation is None:
        return None, "Conversation not found"

    context = BookingContext(
        **conversation["booking_context"]
    )

    if (
        context.service_id is None
        or context.staff_id is None
        or context.booking_datetime is None
    ):
        return None, "Availability context is incomplete"

    slots = get_available_times(
        staff_id=context.staff_id,
        service_id=context.service_id,
        target_date=context.booking_datetime.date(),
    )

    return slots, None



def get_conversation(
    conversation_id: str,
) -> dict[str, Any] | None:
    return get_conversation_by_id(conversation_id)

def process_conversation_message(
    conversation_id: str,
    message: str,
    *,
    llm_provider: LLMProvider | None = None,
) -> AIDecision | None:
    """Process a user message through the AI core and persist context updates."""

    conversation = get_conversation_by_id(conversation_id)

    if conversation is None:
        return None

    current_context = BookingContext(
        **conversation["booking_context"]
    )

    stored_active_intent = conversation.get("active_intent")

    active_intent = (
        Intent(stored_active_intent)
        if stored_active_intent is not None
        else None
    )

    decision, context_update = process_message(
        message,
        current_context=current_context,
        services_by_id=get_active_services_by_id(),
        staff_members=get_all_staff(),
        active_intent=active_intent,
        llm_provider=llm_provider,
    )

    if (
        decision.intent in (
            Intent.BOOK,
            Intent.CHECK_AVAILABILITY,
        )
        and active_intent != decision.intent
    ):
        update_active_intent(
            conversation_id=conversation_id,
            intent=decision.intent,
        )

    if context_update.model_dump(exclude_none=True):
        update_booking_context(
            conversation_id=conversation_id,
            context=context_update,
        )

    if decision.next_action in (
        NextAction.ASK_USER,
        NextAction.UNKNOWN,
    ):
        create_message(
            conversation_id=conversation_id,
            message=MessageCreate(
                role=MessageRole.ASSISTANT,
                content=generate_response(decision),
            ),
        )

    return decision
