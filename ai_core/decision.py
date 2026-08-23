from enum import Enum

from pydantic import BaseModel, Field

from ai_core.entities import ExtractedEntities
from ai_core.intent import Intent
from ai_core.missing_fields import MissingField
from ai_core.missing_fields import MissingField


class NextAction(str, Enum):
    """Possible next steps selected by the AI core."""

    ASK_USER = "ask_user"
    UPDATE_CONTEXT = "update_context"
    CALL_TOOL = "call_tool"
    COMPLETE = "complete"
    UNKNOWN = "unknown"


class AIDecision(BaseModel):
    """Structured result produced by the AI decision layer."""

    intent: Intent
    entities: ExtractedEntities = Field(
        default_factory=ExtractedEntities
    )
    missing_fields: tuple[MissingField, ...] = ()
    next_action: NextAction
