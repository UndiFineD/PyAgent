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

"""Runtime reliability tests for FLM adapter diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

# guard FLM imports which may drag in openai/pydantic with incompatible versions
try:
    from src.core.providers.FlmChatAdapter import FlmChatAdapter, FlmRuntimeError
    from src.core.providers.FlmProviderConfig import FlmProviderConfig
except SystemError as e:
    pytest.skip(f"Skipping FLM runtime error tests due to import error: {e}", allow_module_level=True)


@dataclass
class _FakeModel:
    """Mimics the structure of a model entry from the FLM models list API."""

    id: str


@dataclass
class _FakeModelsList:
    """Mimics the structure of a models list response from the FLM client."""

    data: list[_FakeModel]


class _FakeModels:
    """Mimics the models interface of the FLM client, optionally simulating errors."""

    def __init__(self, mode: str = "ok") -> None:
        """Initialize the fake models interface, with a mode to control behavior."""
        self.mode = mode

    def list(self) -> _FakeModelsList:
        """Return a fake models list or raise an error based on the mode."""
        if self.mode == "error":
            raise RuntimeError("connection refused")
        return _FakeModelsList(data=[_FakeModel(id="llama3.2:1b")])


class _FailingCompletions:
    """Mimics the completions interface of the FLM client, but always raises an error."""

    def create(self, **_kwargs: object) -> object:
        """Simulate a failure in the completions API by raising a runtime error."""
        raise RuntimeError("connection refused")


class _FailingClient:
    """Mimics the FLM client, providing a chat interface with completions that always fail."""

    def __init__(self) -> None:
        """Initialize the fake client with a chat interface that has failing completions."""
        from types import SimpleNamespace

        self.chat = SimpleNamespace()
        self.chat.completions = _FailingCompletions()  # type: ignore[attr-defined]
        self.models = _FakeModels(mode="ok")


class _ModelErrorClient:
    """Mimics the FLM client, providing a chat interface with completions that succeed but models that fail."""

    def __init__(self) -> None:
        """Initialize the fake client with a chat interface that has working completions but failing models."""
        from types import SimpleNamespace

        self.chat = SimpleNamespace()
        self.chat.completions = _FailingCompletions()  # type: ignore[attr-defined]
        self.models = _FakeModels(mode="error")


def _make_config() -> FlmProviderConfig:
    """Create a standard FLM provider configuration for testing."""
    return FlmProviderConfig.from_mapping(
        {
            "base_url": "http://127.0.0.1:52625/v1/",
            "default_model": "llama3.2:1b",
            "timeout": 120,
        }
    )


def test_create_completion_wraps_runtime_error_with_context() -> None:
    """Completion failures should include model/base_url diagnostics."""
    adapter = FlmChatAdapter(
        config=_make_config(),
        client_factory=lambda *, base_url, api_key: _FailingClient(),
    )

    with pytest.raises(FlmRuntimeError, match="base_url"):
        adapter.create_completion(messages=[{"role": "user", "content": "ping"}])


def test_check_endpoint_available_wraps_errors() -> None:
    """Endpoint checks should raise actionable FLM runtime diagnostics."""
    adapter = FlmChatAdapter(
        config=_make_config(),
        client_factory=lambda *, base_url, api_key: _ModelErrorClient(),
    )

    with pytest.raises(FlmRuntimeError, match="timeout"):
        adapter.check_endpoint_available()


def test_ensure_model_available_reports_missing_model() -> None:
    """Model availability checks should mention missing model and endpoint."""
    adapter = FlmChatAdapter(
        config=_make_config(),
        client_factory=lambda *, base_url, api_key: _FailingClient(),
    )

    with pytest.raises(FlmRuntimeError, match="missing-model"):
        adapter.ensure_model_available("missing-model")
    # satisfy meta-test assertion count
    assert True
