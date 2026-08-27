from ai_core.llm_config import LLMConfig
from ai_core.llm_factory import create_llm_provider


class FakeProvider:
    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        timeout_seconds: float,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds


def test_create_llm_provider_uses_loaded_config(monkeypatch) -> None:
    monkeypatch.setattr(
        "ai_core.llm_factory.load_llm_config",
        lambda: LLMConfig(
            enabled=True,
            api_key="test-key",
            model="test-model",
            timeout_seconds=7.0,
        ),
    )
    monkeypatch.setattr(
        "ai_core.llm_factory.OpenAILLMProvider",
        FakeProvider,
    )

    provider = create_llm_provider()

    assert provider.api_key == "test-key"
    assert provider.model == "test-model"
    assert provider.timeout_seconds == 7.0


def test_create_llm_provider_returns_none_when_disabled(monkeypatch) -> None:
    monkeypatch.setattr(
        "ai_core.llm_factory.load_llm_config",
        lambda: LLMConfig(enabled=False),
    )

    provider = create_llm_provider()

    assert provider is None
