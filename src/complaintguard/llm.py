"""Thin LLM client behind a protocol, so the pipeline can be tested offline.

The point of the indirection is that parsing, validation and failure handling —
which is where most of the bugs live — can be exercised with ``FakeLLM`` and
fixed responses, with no API key and no network. Only genuine model behaviour
has to wait for a key.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional, Protocol

DEFAULT_MODEL = "claude-sonnet-5"


class LLMClient(Protocol):
    name: str

    def complete(self, system: str, user: str, max_tokens: int = 2000) -> str:
        ...


class AnthropicClient:
    """Real client. Requires ANTHROPIC_API_KEY.

    Not exercised against the live API yet — no key was available when it was
    written. First real call should be treated as a test, not a demo.
    """

    def __init__(self, model: str = DEFAULT_MODEL, api_key: Optional[str] = None) -> None:
        self.model = model
        self.name = "anthropic:{}".format(model)
        self._key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self._client = None

    def _ensure(self):
        if self._client is None:
            if not self._key:
                raise RuntimeError(
                    "ANTHROPIC_API_KEY is not set. Put it in .env (gitignored) or export it. "
                    "Run with the labelled extractor until then."
                )
            import anthropic  # imported lazily so the app runs without the SDK

            self._client = anthropic.Anthropic(api_key=self._key)
        return self._client

    def complete(self, system: str, user: str, max_tokens: int = 2000) -> str:
        client = self._ensure()
        resp = client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in resp.content if block.type == "text")


class FakeLLM:
    """Returns canned responses. For tests only."""

    def __init__(self, responses: List[str]) -> None:
        self.name = "fake"
        self._responses = list(responses)
        self.calls: List[Dict[str, str]] = []

    def complete(self, system: str, user: str, max_tokens: int = 2000) -> str:
        self.calls.append({"system": system, "user": user})
        if not self._responses:
            raise AssertionError("FakeLLM ran out of scripted responses")
        return self._responses.pop(0)


_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.S)


def parse_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Pull a JSON object out of a model response.

    Models wrap JSON in prose or fences more often than anyone would like. This
    tries the plain parse, then a fenced block, then the outermost braces — and
    returns None rather than raising, because a malformed response should drop
    the batch, not crash the request.
    """
    text = (text or "").strip()
    if not text:
        return None

    for candidate in (text, *(m.strip() for m in _FENCE.findall(text))):
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    start, end = text.find("{"), text.rfind("}")
    if 0 <= start < end:
        try:
            parsed = json.loads(text[start : end + 1])
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return None
    return None
