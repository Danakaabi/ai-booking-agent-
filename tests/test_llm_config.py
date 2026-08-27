import pytest

from ai_core.llm_config import load_llm_config


def test_load_llm_config_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("LLM_ENABLED", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    monkeypatch.setenv("OPENAI_TIMEOUT_SECONDS", "5")

    config = load_llm_config()

    assert config.api_key == "test-key"
    assert config.model == "test-model"
    assert config.timeout_seconds == 5.0


def test_load_llm_config_requires_api_key(monkeypatch) -> None:
    monkeypatch.setenv("LLM_ENABLED", "true")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    with pytest.raises(
        ValueError,
        match="OPENAI_API_KEY is required",
    ):
        load_llm_config()


def test_load_llm_config_rejects_invalid_timeout(monkeypatch) -> None:
    monkeypatch.setenv("LLM_ENABLED", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    monkeypatch.setenv("OPENAI_TIMEOUT_SECONDS", "invalid")

    with pytest.raises(
        ValueError,
        match="OPENAI_TIMEOUT_SECONDS must be a valid number",
    ):
        load_llm_config()


def test_load_llm_config_allows_disabled_llm_without_openai_credentials(
    monkeypatch,
) -> None:
    monkeypatch.setenv("LLM_ENABLED", "false")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    config = load_llm_config()

    assert config.enabled is False


def test_load_llm_config_requires_credentials_when_llm_enabled(
    monkeypatch,
) -> None:
    monkeypatch.setenv("LLM_ENABLED", "true")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    with pytest.raises(
        ValueError,
        match="OPENAI_API_KEY is required",
    ):
        load_llm_config()
