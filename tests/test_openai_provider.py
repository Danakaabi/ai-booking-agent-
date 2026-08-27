from types import SimpleNamespace

from ai_core.intent import Intent
from ai_core.llm_output import LLMInterpretation
from ai_core.openai_provider import OpenAILLMProvider


class FakeResponses:
    def parse(self, **kwargs):
        return SimpleNamespace(
            output_parsed=LLMInterpretation(
                intent=Intent.BOOK,
                entities={
                    "service_name": "Haircut",
                    "customer_name": "Dana",
                },
            )
        )


class FakeOpenAIClient:
    def __init__(self, *, api_key: str):
        self.responses = FakeResponses()


def test_openai_provider_returns_structured_interpretation(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "ai_core.openai_provider.OpenAI",
        FakeOpenAIClient,
    )

    provider = OpenAILLMProvider(
        api_key="test-key",
        model="test-model",
    )

    result = provider.interpret(
        "I want to book a haircut for Dana"
    )

    assert result.intent is Intent.BOOK
    assert result.entities.service_name == "Haircut"
    assert result.entities.customer_name == "Dana"


import pytest

from ai_core.llm_errors import LLMOutputValidationError


class EmptyResponses:
    def parse(self, **kwargs):
        return SimpleNamespace(output_parsed=None)


class EmptyOpenAIClient:
    def __init__(self, *, api_key: str):
        self.responses = EmptyResponses()


def test_openai_provider_rejects_missing_structured_output(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "ai_core.openai_provider.OpenAI",
        EmptyOpenAIClient,
    )

    provider = OpenAILLMProvider(
        api_key="test-key",
        model="test-model",
    )

    with pytest.raises(
        LLMOutputValidationError,
        match="LLM provider returned no structured output",
    ):
        provider.interpret("Book a haircut")


from ai_core.llm_errors import LLMProviderError


class FakeAPIError(Exception):
    pass


class FailingResponses:
    def parse(self, **kwargs):
        raise FakeAPIError("provider unavailable")


class FailingOpenAIClient:
    def __init__(self, *, api_key: str):
        self.responses = FailingResponses()


def test_openai_provider_converts_api_error_to_provider_error(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "ai_core.openai_provider.OpenAI",
        FailingOpenAIClient,
    )
    monkeypatch.setattr(
        "ai_core.openai_provider.openai.APIError",
        FakeAPIError,
    )

    provider = OpenAILLMProvider(
        api_key="test-key",
        model="test-model",
    )

    with pytest.raises(
        LLMProviderError,
        match="LLM provider request failed",
    ):
        provider.interpret("Book a haircut")


class FakeTimeoutError(Exception):
    pass


class TimeoutResponses:
    def parse(self, **kwargs):
        raise FakeTimeoutError("request timed out")


class TimeoutOpenAIClient:
    def __init__(self, *, api_key: str):
        self.responses = TimeoutResponses()


def test_openai_provider_converts_timeout_to_provider_error(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "ai_core.openai_provider.OpenAI",
        TimeoutOpenAIClient,
    )
    monkeypatch.setattr(
        "ai_core.openai_provider.openai.APIError",
        FakeTimeoutError,
    )

    provider = OpenAILLMProvider(
        api_key="test-key",
        model="test-model",
        timeout_seconds=3.0,
    )

    with pytest.raises(
        LLMProviderError,
        match="LLM provider request failed",
    ):
        provider.interpret("Book a haircut")
