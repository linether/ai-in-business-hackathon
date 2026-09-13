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
DEEPSEEK_BASE = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"


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


class OpenAICompatClient:
    """Any OpenAI-compatible chat-completions endpoint — DeepSeek, and others.

    Written against httpx rather than the openai SDK: the request is one POST,
    and the server has 1.6 GB of memory, so there is no reason to install a
    client library for it.

    The organisers place no restriction on models — "any technology can be used"
    — and the rubric rewards architectural depth, not a vendor. DeepSeek is
    markedly cheaper, which matters when the extraction runs over every contact
    in every scenario during tuning.

    ⚠️ Like every other client here, never exercised against the live API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEEPSEEK_MODEL,
        base_url: str = DEEPSEEK_BASE,
        env_var: str = "DEEPSEEK_API_KEY",
        timeout: int = 180,
    ) -> None:
        # Generous by default, because the evaluation harness would rather wait
        # than lose a run. The live web path passes something much shorter: a
        # visitor will not sit through three minutes, and a request held open
        # that long occupies a worker thread the prepared pages also need.
        self.timeout = timeout
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.name = "{}:{}".format(self.base_url.split("//")[-1].split(".")[0], model)
        self._env_var = env_var
        self._key = api_key or os.environ.get(env_var)

    def complete(self, system: str, user: str, max_tokens: int = 2000) -> str:
        if not self._key:
            raise RuntimeError(
                "{} is not set. Put it in .env (gitignored) or export it.".format(self._env_var)
            )
        import httpx

        resp = httpx.post(
            self.base_url + "/chat/completions",
            headers={
                "Authorization": "Bearer {}".format(self._key),
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": 0,  # extraction should be reproducible
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                # Both prompts here ask for a single JSON object, and the parser
                # copes with fences and prose regardless.
                "response_format": {"type": "json_object"},
            },
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"] or ""


def default_client() -> LLMClient:
    """Pick a client from whatever key is actually available.

    Checked in order so a team member with only one of them can just run it.
    """
    if os.environ.get("DEEPSEEK_API_KEY"):
        return OpenAICompatClient()
    if os.environ.get("ANTHROPIC_API_KEY"):
        return AnthropicClient()
    raise RuntimeError(
        "No LLM key found. Set DEEPSEEK_API_KEY or ANTHROPIC_API_KEY in .env "
        "(gitignored), or run with the labelled extractor, which needs neither."
    )


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
