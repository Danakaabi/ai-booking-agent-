from pydantic import BaseModel, Field

from ai_core.entities import ExtractedEntities
from ai_core.intent import Intent


class LLMInterpretation(BaseModel):
    """Validated structured output produced by the LLM boundary."""

    intent: Intent
    entities: ExtractedEntities = Field(
        default_factory=ExtractedEntities
    )
