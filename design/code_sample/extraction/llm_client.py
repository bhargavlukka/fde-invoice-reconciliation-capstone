import os
from dataclasses import dataclass, field

import anthropic
from dotenv import load_dotenv

load_dotenv()


@dataclass
class LLMResponse:
    text: str | None
    tool_calls: list[dict] = field(default_factory=list)
    stop_reason: str = ""
    input_tokens: int = 0
    output_tokens: int = 0


def get_anthropic_client() -> anthropic.Anthropic:
    base_url = os.environ["ANTHROPIC_BASE_URL"]
    api_key = os.environ["ANTHROPIC_API_KEY"]
    return anthropic.Anthropic(base_url=base_url, api_key=api_key)


def complete(
    client: anthropic.Anthropic,
    system: str,
    messages: list[dict],
    tools: list[dict] | None = None,
    model: str | None = None,
) -> LLMResponse:
    model = model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    kwargs = {
        "model": model,
        "max_tokens": 1024,
        "system": system,
        "messages": messages,
    }
    if tools:
        kwargs["tools"] = tools

    response = client.messages.create(**kwargs)

    text_parts = [block.text for block in response.content if block.type == "text"]
    tool_calls = [
        {"id": block.id, "name": block.name, "input": block.input}
        for block in response.content
        if block.type == "tool_use"
    ]

    return LLMResponse(
        text="\n".join(text_parts) if text_parts else None,
        tool_calls=tool_calls,
        stop_reason=response.stop_reason,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
    )
