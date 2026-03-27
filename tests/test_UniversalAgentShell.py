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

"""Red-phase contract tests for src/core/universal/UniversalAgentShell.py."""

from __future__ import annotations

import asyncio
import importlib
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

import pytest


def _import_or_fail(module_name: str) -> Any:
    """Import a module or fail with a red-phase behavioral message.

    Args:
        module_name: Fully-qualified module path to import.

    Returns:
        Imported module object.

    """
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        pytest.fail(
            (
                f"Missing implementation for shell behavior contract: {module_name}. "
                "This red-phase failure is expected before @6code implementation."
            ),
            pytrace=False,
        )


@dataclass
class _FakeRouter:
    """Router double that returns a deterministic routing decision."""

    route: str
    intent: str
    reason: str

    def classify(self, envelope: Any) -> Any:
        """Return a deterministic decision based on configured route.

        Args:
            envelope: Task envelope under dispatch.

        Returns:
            Object exposing normalized_intent, preferred_route, and reason.

        """
        _ = envelope
        return SimpleNamespace(
            normalized_intent=self.intent,
            preferred_route=self.route,
            reason=self.reason,
        )


@dataclass
class _FakeHandler:
    """Core handler double with configurable async behavior."""

    mode: str
    payload: dict[str, Any]
    exc_mod: Any

    async def execute(self, envelope: Any) -> dict[str, Any]:
        """Execute configured behavior for shell route testing.

        Args:
            envelope: Envelope routed to core execution.

        Returns:
            Payload when configured for successful execution.

        Raises:
            CoreExecutionError: When configured for execution failure mode.

        """
        _ = envelope
        if self.mode == "success":
            return self.payload
        if self.mode == "error":
            raise self.exc_mod.CoreExecutionError("core failed")
        if self.mode == "timeout":
            await asyncio.sleep(0.05)
            return self.payload
        raise AssertionError(f"Unknown fake mode: {self.mode}")


@dataclass
class _FakeRegistry:
    """Registry double with configurable resolve behavior."""

    exc_mod: Any
    handler_mode: str
    resolve_mode: str = "ok"

    def resolve(self, intent: str) -> _FakeHandler:
        """Resolve a fake handler or raise expected registry exception.

        Args:
            intent: Normalized intent key requested by shell.

        Returns:
            Fake handler configured for the requested behavior.

        Raises:
            CoreNotRegisteredError: If resolve mode is missing.

        """
        _ = intent
        if self.resolve_mode == "missing":
            raise self.exc_mod.CoreNotRegisteredError("no core")
        return _FakeHandler(
            mode=self.handler_mode,
            payload={"source": "core"},
            exc_mod=self.exc_mod,
        )


def _make_envelope(router_mod: Any, *, intent: str | None = "summarize") -> Any:
    """Create a canonical task envelope for shell contract tests.

    Args:
        router_mod: Imported router module exposing TaskEnvelope.
        intent: Intent value to attach to the envelope.

    Returns:
        TaskEnvelope instance.

    """
    return router_mod.TaskEnvelope(
        task_id="task-shell-1",
        intent=intent,
        payload={"message": "hello"},
        metadata={"source": "unit-test"},
    )


@pytest.mark.asyncio
async def test_dispatch_routes_allowlisted_intent_to_core() -> None:
    """Dispatch should return core route result when router selects core."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    shell = shell_mod.UniversalAgentShell(
        intent_router=_FakeRouter(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_FakeRegistry(exc_mod=exc_mod, handler_mode="success"),
        legacy_dispatcher=lambda envelope: asyncio.sleep(0, result={"source": "legacy"}),
        core_timeout_seconds=0.2,
    )
    result = await shell.dispatch(_make_envelope(router_mod, intent="summarize"))

    assert result.route == "core"
    assert result.intent == "summarize"
    assert result.payload == {"source": "core"}


@pytest.mark.asyncio
async def test_dispatch_routes_non_allowlisted_intent_to_legacy() -> None:
    """Dispatch should use legacy path when router selects legacy route."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    exc_mod = _import_or_fail("src.core.universal.exceptions")
    _ = exc_mod

    async def _legacy(envelope: Any) -> dict[str, str]:
        """Return deterministic legacy payload.

        Args:
            envelope: Task envelope routed to legacy path.

        Returns:
            Legacy payload marker.

        """
        _ = envelope
        return {"source": "legacy"}

    shell = shell_mod.UniversalAgentShell(
        intent_router=_FakeRouter(route="legacy", intent="unknown", reason="not_allowlisted"),
        core_registry=_FakeRegistry(exc_mod=_import_or_fail("src.core.universal.exceptions"), handler_mode="success"),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.2,
    )
    result = await shell.dispatch(_make_envelope(router_mod, intent="translate"))

    assert result.route == "legacy"
    assert result.intent == "unknown"
    assert result.payload == {"source": "legacy"}


@pytest.mark.asyncio
async def test_dispatch_falls_back_on_registry_miss_once() -> None:
    """Dispatch should fallback once to legacy when registry resolve misses."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    exc_mod = _import_or_fail("src.core.universal.exceptions")
    calls = {"legacy": 0}

    async def _legacy(envelope: Any) -> dict[str, str]:
        """Track and return legacy payload for fallback validation.

        Args:
            envelope: Task envelope routed to legacy fallback.

        Returns:
            Legacy payload marker.

        """
        _ = envelope
        calls["legacy"] += 1
        return {"source": "legacy"}

    shell = shell_mod.UniversalAgentShell(
        intent_router=_FakeRouter(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_FakeRegistry(exc_mod=exc_mod, handler_mode="success", resolve_mode="missing"),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.2,
    )
    result = await shell.dispatch(_make_envelope(router_mod, intent="summarize"))

    assert result.route == "legacy"
    assert calls["legacy"] == 1


@pytest.mark.asyncio
async def test_dispatch_falls_back_on_core_execution_error() -> None:
    """Dispatch should fallback once when core handler raises execution error."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    async def _legacy(envelope: Any) -> dict[str, str]:
        """Return deterministic legacy payload.

        Args:
            envelope: Task envelope routed to legacy fallback.

        Returns:
            Legacy payload marker.

        """
        _ = envelope
        return {"source": "legacy"}

    shell = shell_mod.UniversalAgentShell(
        intent_router=_FakeRouter(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_FakeRegistry(exc_mod=exc_mod, handler_mode="error"),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.2,
    )
    result = await shell.dispatch(_make_envelope(router_mod, intent="summarize"))

    assert result.route == "legacy"
    assert result.payload == {"source": "legacy"}


@pytest.mark.asyncio
async def test_dispatch_falls_back_on_core_timeout() -> None:
    """Dispatch should fallback once when core execution exceeds timeout."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    async def _legacy(envelope: Any) -> dict[str, str]:
        """Return deterministic legacy payload.

        Args:
            envelope: Task envelope routed to legacy fallback.

        Returns:
            Legacy payload marker.

        """
        _ = envelope
        return {"source": "legacy"}

    shell = shell_mod.UniversalAgentShell(
        intent_router=_FakeRouter(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_FakeRegistry(exc_mod=exc_mod, handler_mode="timeout"),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.01,
    )
    result = await shell.dispatch(_make_envelope(router_mod, intent="summarize"))

    assert result.route == "legacy"
    assert result.payload == {"source": "legacy"}


@pytest.mark.asyncio
async def test_dispatch_raises_envelope_validation_error_for_invalid_envelope() -> None:
    """Dispatch should raise validation error when envelope violates contract."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    shell = shell_mod.UniversalAgentShell(
        intent_router=_FakeRouter(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_FakeRegistry(exc_mod=exc_mod, handler_mode="success"),
        legacy_dispatcher=lambda envelope: asyncio.sleep(0, result={"source": "legacy"}),
        core_timeout_seconds=0.2,
    )

    with pytest.raises(exc_mod.EnvelopeValidationError):
        await shell.dispatch(None)


@pytest.mark.asyncio
async def test_dispatch_does_not_retry_fallback_when_legacy_dispatch_fails() -> None:
    """Dispatch should call legacy once and surface legacy failure without retry."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    exc_mod = _import_or_fail("src.core.universal.exceptions")
    calls = {"legacy": 0}

    async def _legacy(envelope: Any) -> dict[str, str]:
        """Raise deterministic legacy failure and track call count.

        Args:
            envelope: Task envelope routed to legacy fallback.

        Raises:
            RuntimeError: Raised to validate no second fallback attempt.

        """
        _ = envelope
        calls["legacy"] += 1
        raise RuntimeError("legacy failed")

    shell = shell_mod.UniversalAgentShell(
        intent_router=_FakeRouter(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_FakeRegistry(exc_mod=exc_mod, handler_mode="error"),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.2,
    )

    with pytest.raises((RuntimeError, exc_mod.LegacyDispatchError)):
        await shell.dispatch(_make_envelope(router_mod, intent="summarize"))

    assert calls["legacy"] == 1


@pytest.mark.asyncio
async def test_dispatch_result_includes_route_intent_and_fallback_reason() -> None:
    """Dispatch result should expose telemetry fields required by contract."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    async def _legacy(envelope: Any) -> dict[str, str]:
        """Return deterministic legacy payload.

        Args:
            envelope: Task envelope routed to legacy fallback.

        Returns:
            Legacy payload marker.

        """
        _ = envelope
        return {"source": "legacy"}

    shell = shell_mod.UniversalAgentShell(
        intent_router=_FakeRouter(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_FakeRegistry(exc_mod=exc_mod, handler_mode="error"),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.2,
    )
    result = await shell.dispatch(_make_envelope(router_mod, intent="summarize"))

    assert hasattr(result, "route")
    assert hasattr(result, "intent")
    assert hasattr(result, "fallback_reason")
    assert result.route == "legacy"
    assert result.intent == "summarize"
    assert result.fallback_reason is not None
