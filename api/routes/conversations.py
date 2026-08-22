from fastapi import APIRouter, HTTPException

from ai_core.conversation_service import (
    get_conversation,
    start_conversation,
)

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