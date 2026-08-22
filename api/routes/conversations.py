from fastapi import APIRouter, HTTPException
from ai_core.conversation_service import (
    add_message_to_conversation,
    execute_booking_from_conversation,
    get_conversation,
    get_conversation_history,
    start_conversation,
    update_conversation_booking_context,

)
from api.http_errors import raise_booking_http_error
from api.schemas.conversation import BookingContext, MessageCreate



router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post("")
def create_conversation_route() -> dict:
    return start_conversation()


@router.get("/{conversation_id}")
def get_conversation_route(conversation_id: str) -> dict:
    conversation = get_conversation(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return conversation



@router.post("/{conversation_id}/messages")
def add_message_route(
    conversation_id: str,
    message: MessageCreate,
) -> dict:
    created_message = add_message_to_conversation(
        conversation_id=conversation_id,
        message=message,
    )

    if created_message is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return created_message


@router.get("/{conversation_id}/messages")
def get_conversation_messages_route(
    conversation_id: str,
) -> list[dict]:
    history = get_conversation_history(conversation_id)

    if history is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return history



@router.patch("/{conversation_id}/booking-context")
def update_booking_context_route(
    conversation_id: str,
    context: BookingContext,
) -> dict:
    updated = update_conversation_booking_context(
        conversation_id=conversation_id,
        context=context,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return updated



@router.post("/{conversation_id}/bookings")
def create_booking_from_conversation_route(
    conversation_id: str,
) -> dict:
    booking, error = execute_booking_from_conversation(
        conversation_id
    )

    if error == "Conversation not found":
        raise HTTPException(
            status_code=404,
            detail=error,
        )

    if error == "Booking context is incomplete":
        raise HTTPException(
            status_code=422,
            detail=error,
        )

    raise_booking_http_error(error)

    return booking


