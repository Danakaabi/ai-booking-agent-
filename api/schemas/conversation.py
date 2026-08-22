from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ConversationState(str,Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class BookingContext(BaseModel):
    service_id: str | None = Field(default=None, min_length=1)
    customer_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    customer_phone: str | None = Field(
        default=None,
        min_length=8,
        max_length=20,
    )
    booking_datetime: datetime | None = None
    staff_id: str | None = None
    
class ConversationCreate(BaseModel):
    """Data required to start a new conversation."""

    pass

class Conversation(BaseModel):
    """Public representation of a stored conversation."""

    id: str
    state: ConversationState
    booking_context: BookingContext
    created_at: datetime
    updated_at: datetime


class MessageCreate(BaseModel):
    """Data required to add a message to a conversation."""

    role: MessageRole
    content: str = Field(min_length=1, max_length=10_000)


class Message(BaseModel):
    """Public representation of a stored conversation message."""

    id: str
    conversation_id: str
    role: MessageRole
    content: str
    created_at: datetime
