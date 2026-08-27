import openai
from openai import OpenAI

from ai_core.llm_errors import LLMOutputValidationError, LLMProviderError
from ai_core.llm_output import LLMInterpretation


SYSTEM_PROMPT = """
You are the natural-language interpreter for an AI booking system.

Your only responsibility is to identify:
1. The user's intent.
2. Entities explicitly provided or reasonably extractable from the message.

Allowed intent values:
- book
- reschedule
- cancel
- check_availability
- get_services
- get_staff
- unknown

Entity fields:
- service_name
- customer_name
- customer_phone
- booking_datetime
- staff_name

Rules:
- Use unknown when the user's intent cannot be determined reliably.
- Do not invent service names, staff names, customer details, dates, or phone numbers.
- Do not execute bookings.
- Do not call or select tools.
- Do not access databases.
- Do not choose BusinessAction or NextAction.
- Do not make business-rule decisions.
- Return only the structured output requested by the schema.
""".strip()


class OpenAILLMProvider:
    """OpenAI-backed implementation of the LLM provider contract."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        timeout_seconds: float = 10.0,
    ) -> None:
        if not api_key.strip():
            raise ValueError("api_key must not be empty")

        if not model.strip():
            raise ValueError("model must not be empty")

        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")

        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._timeout_seconds = timeout_seconds

    def interpret(self, message: str) -> LLMInterpretation:
        try:
            response = self._client.responses.parse(
                model=self._model,
                instructions=SYSTEM_PROMPT,
                input=message,
                text_format=LLMInterpretation,
                temperature=0,
                timeout=self._timeout_seconds,
            )
        except openai.APIError as exc:
            raise LLMProviderError("LLM provider request failed") from exc

        parsed = response.output_parsed

        if parsed is None:
            raise LLMOutputValidationError(
                "LLM provider returned no structured output"
            )

        return parsed
