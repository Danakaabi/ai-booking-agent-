import pytest
from pydantic import ValidationError

from api.schemas.conversation import MessageCreate, MessageRole


def test_message_create_accepts_valid_user_message():
    message = MessageCreate(
        role=MessageRole.USER,
        content="I want to book a haircut",
    )

    assert message.role == MessageRole.USER
    assert message.content == "I want to book a haircut"


def test_message_create_rejects_empty_content():
    with pytest.raises(ValidationError):
        MessageCreate(
            role=MessageRole.USER,
            content="",
        )


def test_message_create_rejects_invalid_role():
    with pytest.raises(ValidationError):
        MessageCreate(
            role="invalid-role",
            content="Hello",
        )