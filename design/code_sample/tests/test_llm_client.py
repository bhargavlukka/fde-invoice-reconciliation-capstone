# design/code_sample/tests/test_llm_client.py
from extraction.llm_client import get_anthropic_client


def test_get_anthropic_client_uses_env_base_url(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://sharedllm.com/v1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    client = get_anthropic_client()
    assert str(client.base_url).rstrip("/") == "https://sharedllm.com/v1"


def test_get_anthropic_client_never_defaults_to_public_anthropic_api(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://sharedllm.com/v1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    client = get_anthropic_client()
    assert "api.anthropic.com" not in str(client.base_url)
