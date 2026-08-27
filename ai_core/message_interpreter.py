from ai_core.entities import ExtractedEntities
from ai_core.entity_extractor import extract_entities
from ai_core.intent import Intent
from ai_core.intent_detector import detect_intent
from ai_core.llm_errors import LLMError
from ai_core.llm_interpreter import interpret_message
from ai_core.llm_provider import LLMProvider


def interpret_user_message(
    message: str,
    *,
    service_names: tuple[str, ...] = (),
    staff_names: tuple[str, ...] = (),
    llm_provider: LLMProvider | None = None,
) -> tuple[Intent, ExtractedEntities]:
    """Interpret a user message using LLM or deterministic extraction."""

    if llm_provider is not None:
        try:
            interpretation = interpret_message(
                message,
                provider=llm_provider,
            )
            return interpretation.intent, interpretation.entities
        except LLMError:
            pass

    intent = detect_intent(message)

    entities = extract_entities(
        message,
        service_names=service_names,
        staff_names=staff_names,
    )

    return intent, entities
