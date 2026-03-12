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

"""Tests for FLM tool-call loop behavior."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

import pytest

# FLM imports transitively depend on openai/pydantic which may raise a
# SystemError if the pydantic-core version is incompatible.  Skip all
# tests in this module when that happens.
try:
    from src.core.providers.flm_chat_adapter import FlmChatAdapter, FlmRuntimeError
    from src.core.providers.FlmProviderConfig import FlmProviderConfig
except SystemError as e:
    pytest.skip(f"Skipping FLM tool loop tests due to import error: {e}", allow_module_level=True)


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


def _make_config() -> FlmProviderConfig:
    """Create a standard FLM provider configuration for testing."""
    return FlmProviderConfig.from_mapping(
        {
            "base_url": "http://127.0.0.1:52625/v1/",
            "default_model": "llama3.2:1b",
        }
    )


@pytest.mark.asyncio
async def test_tool_loop_executes_and_returns_terminal_answer() -> None:
    """Adapter should process a tool call then return terminal model response."""
    tool_response = _FakeResponse(
        choices=[
            _FakeChoice(
                message=_FakeMessage(
                    content="calling tool",
                    tool_calls=[
                        _FakeToolCall(
                            id="call_1",
                            type="function",
                            function=_FakeFunction(name="echo", arguments='{"x": 1}'),
                        )
                    ],
                )
            )
        ]
    )
    final_response = _FakeResponse(
        choices=[_FakeChoice(message=_FakeMessage(content="done", tool_calls=None))]
    )
    fake_client = _FakeClient([tool_response, final_response])

    def _client_factory(*, base_url: str, api_key: str) -> _FakeClient:
        del base_url, api_key
        return fake_client

    adapter = FlmChatAdapter(config=_make_config(), client_factory=cast(Any, _client_factory))
    messages: list[dict[str, Any]] = [{"role": "user", "content": "hello"}]

    answer = await adapter.run_until_terminal(
        messages=messages,
        tool_executor=lambda _tool_call: "Tool call processed",
    )

    assert answer == "done"
    assert len(fake_client.chat.completions.calls) == 2

    second_call_messages = fake_client.chat.completions.calls[1]["messages"]
    assert any(message.get("role") == "assistant" for message in second_call_messages)
    assert any(message.get("role") == "tool" for message in second_call_messages)


@pytest.mark.asyncio
async def test_tool_loop_raises_when_iterations_exceeded() -> None:
    """Adapter should stop and fail when max_tool_iterations is exceeded."""
    looping_response = _FakeResponse(
        choices=[
            _FakeChoice(
                message=_FakeMessage(
                    content="calling tool",
                    tool_calls=[
                        _FakeToolCall(
                            id="call_1",
                            type="function",
                            function=_FakeFunction(name="echo", arguments='{}'),
                        )
                    ],
                )
            )
        ]
    )
    fake_client = _FakeClient([looping_response])

    def _client_factory(*, base_url: str, api_key: str) -> _FakeClient:
        del base_url, api_key
        return fake_client

    adapter = FlmChatAdapter(config=_make_config(), client_factory=cast(Any, _client_factory))

    with pytest.raises(FlmRuntimeError, match="Exceeded max tool iterations"):
        await adapter.run_until_terminal(
            messages=[{"role": "user", "content": "hello"}],
            max_tool_iterations=0,
            tool_executor=lambda _tool_call: "Tool call processed",
        )
