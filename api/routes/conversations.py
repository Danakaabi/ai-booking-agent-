from fastapi import APIRouter, HTTPException

from ai_core.conversation_service import (
    add_message_to_conversation,
    get_conversation,
    start_conversation,

)
from api.schemas.conversation import MessageCreate
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