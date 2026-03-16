#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for FLM OpenAI-compatible chat adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

import pytest

# importing FlmChatAdapter may transitively import openai/pydantic and
# raise a SystemError when pydantic-core version mismatches.  Skip entire
# module on such errors so the rest of the suite can proceed.
try:
    from src.core.providers.FlmChatAdapter import FlmChatAdapter
    from src.core.providers.FlmProviderConfig import FlmProviderConfig
except SystemError as e:
    pytest.skip(f"Skipping FLM adapter tests due to import error: {e}", allow_module_level=True)


@dataclass
class _FakeFunction:
    """Mimics the structure of a tool call function in the FLM response."""

    name: str
    arguments: str


@dataclass
class _FakeToolCall:
    """Mimics the structure of a tool call in the FLM response."""

    id: str
    type: str
    function: _FakeFunction


@dataclass
class _FakeMessage:
    """Mimics the structure of a message in the FLM response."""

    content: str | None
    tool_calls: list[_FakeToolCall] | None


@dataclass
class _FakeChoice:
    """Mimics the structure of a choice in the FLM response."""

    message: _FakeMessage


@dataclass
class _FakeResponse:
    """Mimics the structure of a response from the FLM completions API."""

    choices: list[_FakeChoice]


class _FakeCompletions:
    """Mimics the completions interface of the FLM client, recording calls for verification."""

    def __init__(self, responses: list[_FakeResponse]) -> None:
        """Initialize with a list of responses to return on create calls."""
        self._responses = responses
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs: object) -> _FakeResponse:
        """Record the call arguments and return the next response."""
        self.calls.append(kwargs)
        return self._responses.pop(0)


class _FakeClient:
    """Mimics the FLM client, providing a chat interface with completions."""

    def __init__(self, responses: list[_FakeResponse]) -> None:
        """Initialize the fake client with a list of responses for the completions API."""
        self.chat = type("Chat", (), {})()
        self.chat.completions = _FakeCompletions(responses)


def test_create_completion_uses_default_model() -> None:
    """Adapter should pass default model when no override is supplied."""
    response = _FakeResponse(choices=[_FakeChoice(message=_FakeMessage(content="ok", tool_calls=None))])
    fake_client = _FakeClient([response])

    config = FlmProviderConfig.from_mapping(
        {
            "base_url": "http://127.0.0.1:52625/v1/",
            "default_model": "llama3.2:1b",
        }
    )

    def _client_factory(*, base_url: str, api_key: str) -> _FakeClient:
        del base_url, api_key
        return fake_client

    adapter = FlmChatAdapter(config=config, client_factory=cast(Any, _client_factory))
    messages: list[dict[str, Any]] = [{"role": "system", "content": "you are helpful"}]

    result = adapter.create_completion(messages=messages, max_tokens=1024)

    assert result is response
    assert fake_client.chat.completions.calls[0]["model"] == "llama3.2:1b"
    assert fake_client.chat.completions.calls[0]["messages"] == messages
    assert fake_client.chat.completions.calls[0]["max_tokens"] == 1024


def test_run_until_terminal_returns_final_content() -> None:
    """Adapter should return terminal assistant content when no tool calls are present."""
    response = _FakeResponse(choices=[_FakeChoice(message=_FakeMessage(content="terminal answer", tool_calls=None))])
    fake_client = _FakeClient([response])

    config = FlmProviderConfig.from_mapping(
        {
            "base_url": "http://127.0.0.1:52625/v1/",
            "default_model": "llama3.2:1b",
        }
    )

    def _client_factory(*, base_url: str, api_key: str) -> _FakeClient:
        del base_url, api_key
        return fake_client

    adapter = FlmChatAdapter(config=config, client_factory=cast(Any, _client_factory))
    messages: list[dict[str, Any]] = [{"role": "user", "content": "are you listening?"}]

    import asyncio

    answer = asyncio.run(adapter.run_until_terminal(messages=messages))

    assert answer == "terminal answer"
