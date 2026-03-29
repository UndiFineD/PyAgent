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

"""Core contract tests for the Universal Shell facade public surface."""

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
                f"Missing implementation for facade behavior contract: {module_name}. "
                "This red-phase failure is expected before @6code implementation."
            ),
            pytrace=False,
        )


def test_public_exports_include_stable_symbols() -> None:
    """Verify the facade exports the stable contract symbols.

    The contract is defined in the design artifact and must be available from
    the package root once implemented.
    """
    facade = _import_or_fail("src.core.universal")

    required = {
        "TaskEnvelope",
        "RoutingDecision",
        "DispatchResult",
        "UniversalIntentRouter",
        "UniversalCoreRegistry",
        "UniversalAgentShell",
        "UniversalShellError",
        "EnvelopeValidationError",
        "RoutingContractError",
        "CoreRegistrationError",
        "CoreNotRegisteredError",
        "CoreExecutionError",
        "CoreTimeoutError",
        "LegacyDispatchError",
    }

    missing = sorted(symbol for symbol in required if not hasattr(facade, symbol))
    assert not missing, f"Facade exports are incomplete: {missing}"


def test_exception_hierarchy_matches_design_contract() -> None:
    """Verify exception hierarchy follows the defined universal shell contract."""
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    root_error = exc_mod.UniversalShellError
    leaf_errors = [
        exc_mod.EnvelopeValidationError,
        exc_mod.RoutingContractError,
        exc_mod.CoreRegistrationError,
        exc_mod.CoreNotRegisteredError,
        exc_mod.CoreExecutionError,
        exc_mod.CoreTimeoutError,
        exc_mod.LegacyDispatchError,
    ]

    for error_type in leaf_errors:
        assert issubclass(error_type, root_error), f"{error_type.__name__} must inherit UniversalShellError"


def test_task_envelope_and_dispatch_result_have_required_fields() -> None:
    """Verify dataclass-like contract fields exist on key facade value objects."""
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")

    envelope = router_mod.TaskEnvelope(
        task_id="task-1",
        intent="summarize",
        payload={"message": "hello"},
        metadata={"source": "unit-test"},
    )
    result = shell_mod.DispatchResult(
        route="legacy",
        intent="unknown",
        payload={"ok": False},
        fallback_reason="core_missing",
    )

    for field_name in ("task_id", "intent", "payload", "metadata"):
        assert hasattr(envelope, field_name), f"TaskEnvelope missing field: {field_name}"

    for field_name in ("route", "intent", "payload", "fallback_reason"):
        assert hasattr(result, field_name), f"DispatchResult missing field: {field_name}"


def test_router_classify_rejects_non_envelope() -> None:
    """Verify router rejects non-TaskEnvelope inputs with contract error."""
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    exc_mod = _import_or_fail("src.core.universal.exceptions")
    router = router_mod.UniversalIntentRouter(core_allowlist={"Summarize", "  EXTRACT  "})

    with pytest.raises(exc_mod.EnvelopeValidationError):
        router.classify({"intent": "summarize"})


def test_router_allowlist_normalization_and_validate() -> None:
    """Verify router normalizes allowlist values and exposes module validate."""
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    router = router_mod.UniversalIntentRouter(core_allowlist={"Summarize", "  EXTRACT  "})

    envelope = router_mod.TaskEnvelope(
        task_id="task-router-1",
        intent="extract",
        payload={"message": "hi"},
        metadata={"source": "unit-test"},
    )
    decision = router.classify(envelope)

    assert decision.preferred_route == "core"
    assert decision.reason == "allowlisted"
    assert router_mod.validate() is True


@dataclass
class _ValidHandler:
    """Provide an async execute method that satisfies registry contract checks."""

    async def execute(self, envelope: Any) -> dict[str, Any]:
        """Return deterministic payload for shell and registry tests.

        Args:
            envelope: Routed envelope passed by caller.

        Returns:
            Static payload used by tests.

        """
        _ = envelope
        return {"status": "ok"}


class _MissingExecuteHandler:
    """Represent an invalid handler that lacks execute()."""


class _SyncExecuteHandler:
    """Represent an invalid handler where execute() is not async."""

    def execute(self, envelope: Any) -> dict[str, Any]:
        """Return value from a sync method to trigger contract rejection.

        Args:
            envelope: Routed envelope passed by caller.

        Returns:
            Static payload.

        """
        _ = envelope
        return {"status": "sync"}


def test_registry_validation_and_lifecycle_paths() -> None:
    """Cover registry contract validation, lookup, and lifecycle behaviors."""
    registry_mod = _import_or_fail("src.core.universal.UniversalCoreRegistry")
    exc_mod = _import_or_fail("src.core.universal.exceptions")
    registry = registry_mod.UniversalCoreRegistry()

    with pytest.raises(exc_mod.CoreRegistrationError):
        registry.register("summarize", "not-callable")

    with pytest.raises(exc_mod.CoreRegistrationError):
        registry.register("summarize", lambda: _MissingExecuteHandler())

    with pytest.raises(exc_mod.CoreRegistrationError):
        registry.register("summarize", lambda: _SyncExecuteHandler())

    registry.register("  SUMMARIZE ", lambda: _ValidHandler())
    assert registry.has_intent("summarize") is True
    assert registry.has_intent("missing") is False
    assert registry.list_intents() == ("summarize",)

    handler = registry.resolve(" summarize ")
    assert hasattr(handler, "execute")

    with pytest.raises(exc_mod.CoreRegistrationError):
        registry.register("summarize", lambda: _ValidHandler())

    with pytest.raises(exc_mod.CoreNotRegisteredError):
        registry.resolve("missing")

    with pytest.raises(exc_mod.CoreRegistrationError):
        registry.unregister("  ")

    assert registry.unregister("summarize") is True
    assert registry.unregister("summarize") is False
    assert registry_mod.validate() is True


@dataclass
class _RouterDouble:
    """Return a deterministic routing decision object for shell tests."""

    route: str
    intent: str
    reason: str

    def classify(self, envelope: Any) -> Any:
        """Return a decision object with configured values.

        Args:
            envelope: Envelope candidate passed to router.

        Returns:
            Decision-like object consumed by shell validation.

        """
        _ = envelope
        return SimpleNamespace(
            normalized_intent=self.intent,
            preferred_route=self.route,
            reason=self.reason,
        )


class _RouterBrokenDecision:
    """Return an incomplete decision to exercise shell contract validation."""

    def classify(self, envelope: Any) -> Any:
        """Return an object missing required fields.

        Args:
            envelope: Envelope candidate passed to router.

        Returns:
            Incomplete object intentionally missing route fields.

        """
        _ = envelope
        return object()


@dataclass
class _CoreHandlerDouble:
    """Core handler with deterministic success, error, or timeout behavior."""

    mode: str
    exc_mod: Any

    async def execute(self, envelope: Any) -> dict[str, Any]:
        """Execute deterministic behavior for shell branch coverage.

        Args:
            envelope: Task envelope routed by shell.

        Returns:
            Deterministic payload when mode is success.

        Raises:
            CoreExecutionError: For error mode.

        """
        _ = envelope
        if self.mode == "success":
            return {"source": "core"}
        if self.mode == "error":
            raise self.exc_mod.CoreExecutionError("core failed")
        if self.mode == "timeout":
            await asyncio.sleep(0.02)
            return {"source": "core"}
        raise AssertionError(f"unexpected mode: {self.mode}")


@dataclass
class _CoreRegistryDouble:
    """Resolve core handlers or raise missing-core exceptions."""

    mode: str
    exc_mod: Any

    def resolve(self, intent: str) -> _CoreHandlerDouble:
        """Resolve handler for intent or raise missing-core failure.

        Args:
            intent: Normalized intent key requested by shell.

        Returns:
            Deterministic handler configured by mode.

        Raises:
            CoreNotRegisteredError: For missing mode.

        """
        _ = intent
        if self.mode == "missing":
            raise self.exc_mod.CoreNotRegisteredError("missing")
        return _CoreHandlerDouble(mode=self.mode, exc_mod=self.exc_mod)


def _make_envelope() -> Any:
    """Create a canonical envelope for shell execution tests.

    Returns:
        TaskEnvelope from universal router module.

    """
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    return router_mod.TaskEnvelope(
        task_id="task-shell-1",
        intent="summarize",
        payload={"message": "hello"},
        metadata={"source": "unit-test"},
    )


@pytest.mark.asyncio
async def test_shell_constructor_and_decision_contract_errors() -> None:
    """Verify shell rejects invalid timeout and malformed router decisions."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    async def _legacy(envelope: Any) -> dict[str, Any]:
        """Return deterministic legacy payload.

        Args:
            envelope: Envelope routed to legacy path.

        Returns:
            Static legacy payload.

        """
        _ = envelope
        return {"source": "legacy"}

    with pytest.raises(exc_mod.RoutingContractError):
        shell_mod.UniversalAgentShell(
            intent_router=_RouterDouble(route="legacy", intent="unknown", reason="route"),
            core_registry=_CoreRegistryDouble(mode="success", exc_mod=exc_mod),
            legacy_dispatcher=_legacy,
            core_timeout_seconds=0,
        )

    shell = shell_mod.UniversalAgentShell(
        intent_router=_RouterBrokenDecision(),
        core_registry=_CoreRegistryDouble(mode="success", exc_mod=exc_mod),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.01,
    )

    with pytest.raises(exc_mod.RoutingContractError):
        await shell.dispatch(_make_envelope())


@pytest.mark.asyncio
async def test_shell_rejects_invalid_route_and_empty_intent() -> None:
    """Verify shell rejects invalid route and empty normalized intent values."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    async def _legacy(envelope: Any) -> dict[str, Any]:
        """Return deterministic legacy payload.

        Args:
            envelope: Envelope routed to legacy path.

        Returns:
            Static legacy payload.

        """
        _ = envelope
        return {"source": "legacy"}

    shell_invalid_route = shell_mod.UniversalAgentShell(
        intent_router=_RouterDouble(route="other", intent="summarize", reason="bad-route"),
        core_registry=_CoreRegistryDouble(mode="success", exc_mod=exc_mod),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.01,
    )

    with pytest.raises(exc_mod.RoutingContractError):
        await shell_invalid_route.dispatch(_make_envelope())

    shell_empty_intent = shell_mod.UniversalAgentShell(
        intent_router=_RouterDouble(route="legacy", intent="", reason="bad-intent"),
        core_registry=_CoreRegistryDouble(mode="success", exc_mod=exc_mod),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.01,
    )

    with pytest.raises(exc_mod.RoutingContractError):
        await shell_empty_intent.dispatch(_make_envelope())


@pytest.mark.asyncio
async def test_shell_core_success_legacy_path_and_fallback_paths() -> None:
    """Cover shell success, direct legacy route, and each recoverable fallback path."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    exc_mod = _import_or_fail("src.core.universal.exceptions")
    calls = {"legacy": 0}

    async def _legacy(envelope: Any) -> dict[str, Any]:
        """Track legacy calls and return deterministic payload.

        Args:
            envelope: Envelope routed to legacy path.

        Returns:
            Legacy payload.

        """
        _ = envelope
        calls["legacy"] += 1
        return {"source": "legacy"}

    shell_core = shell_mod.UniversalAgentShell(
        intent_router=_RouterDouble(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_CoreRegistryDouble(mode="success", exc_mod=exc_mod),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.1,
    )
    core_result = await shell_core.dispatch(_make_envelope())
    assert core_result.route == "core"
    assert core_result.payload == {"source": "core"}
    assert core_result.fallback_reason is None

    shell_direct_legacy = shell_mod.UniversalAgentShell(
        intent_router=_RouterDouble(route="legacy", intent="unknown", reason="not_allowlisted"),
        core_registry=_CoreRegistryDouble(mode="success", exc_mod=exc_mod),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.1,
    )
    direct_legacy_result = await shell_direct_legacy.dispatch(_make_envelope())
    assert direct_legacy_result.route == "legacy"
    assert direct_legacy_result.fallback_reason == "not_allowlisted"

    shell_missing = shell_mod.UniversalAgentShell(
        intent_router=_RouterDouble(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_CoreRegistryDouble(mode="missing", exc_mod=exc_mod),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.1,
    )
    missing_result = await shell_missing.dispatch(_make_envelope())
    assert missing_result.route == "legacy"
    assert missing_result.fallback_reason == "core_not_registered"

    shell_error = shell_mod.UniversalAgentShell(
        intent_router=_RouterDouble(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_CoreRegistryDouble(mode="error", exc_mod=exc_mod),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.1,
    )
    error_result = await shell_error.dispatch(_make_envelope())
    assert error_result.route == "legacy"
    assert error_result.fallback_reason == "core_execution_error"

    shell_timeout = shell_mod.UniversalAgentShell(
        intent_router=_RouterDouble(route="core", intent="summarize", reason="allowlisted"),
        core_registry=_CoreRegistryDouble(mode="timeout", exc_mod=exc_mod),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.001,
    )
    timeout_result = await shell_timeout.dispatch(_make_envelope())
    assert timeout_result.route == "legacy"
    assert timeout_result.fallback_reason == "core_timeout"

    assert calls["legacy"] >= 4


@pytest.mark.asyncio
async def test_shell_legacy_error_mapping_and_passthrough() -> None:
    """Verify shell maps generic legacy errors and preserves legacy contract errors."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    async def _legacy_generic_failure(envelope: Any) -> dict[str, Any]:
        """Raise generic error to validate LegacyDispatchError mapping.

        Args:
            envelope: Envelope routed to legacy path.

        Raises:
            RuntimeError: Generic legacy failure.

        """
        _ = envelope
        raise RuntimeError("legacy exploded")

    shell_generic_failure = shell_mod.UniversalAgentShell(
        intent_router=_RouterDouble(route="legacy", intent="unknown", reason="legacy-only"),
        core_registry=_CoreRegistryDouble(mode="success", exc_mod=exc_mod),
        legacy_dispatcher=_legacy_generic_failure,
        core_timeout_seconds=0.1,
    )

    with pytest.raises(exc_mod.LegacyDispatchError):
        await shell_generic_failure.dispatch(_make_envelope())

    async def _legacy_contract_failure(envelope: Any) -> dict[str, Any]:
        """Raise LegacyDispatchError to ensure passthrough behavior.

        Args:
            envelope: Envelope routed to legacy path.

        Raises:
            LegacyDispatchError: Explicit legacy contract failure.

        """
        _ = envelope
        raise exc_mod.LegacyDispatchError("known")

    shell_contract_failure = shell_mod.UniversalAgentShell(
        intent_router=_RouterDouble(route="legacy", intent="unknown", reason="legacy-only"),
        core_registry=_CoreRegistryDouble(mode="success", exc_mod=exc_mod),
        legacy_dispatcher=_legacy_contract_failure,
        core_timeout_seconds=0.1,
    )

    with pytest.raises(exc_mod.LegacyDispatchError, match="known"):
        await shell_contract_failure.dispatch(_make_envelope())


@pytest.mark.asyncio
async def test_shell_rejects_invalid_envelope_type() -> None:
    """Verify shell raises envelope validation error for non-TaskEnvelope input."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    async def _legacy(envelope: Any) -> dict[str, Any]:
        """Return deterministic legacy payload.

        Args:
            envelope: Envelope routed to legacy path.

        Returns:
            Legacy payload.

        """
        _ = envelope
        return {"source": "legacy"}

    shell = shell_mod.UniversalAgentShell(
        intent_router=_RouterDouble(route="legacy", intent="unknown", reason="legacy-only"),
        core_registry=_CoreRegistryDouble(mode="success", exc_mod=exc_mod),
        legacy_dispatcher=_legacy,
        core_timeout_seconds=0.1,
    )

    with pytest.raises(exc_mod.EnvelopeValidationError):
        await shell.dispatch("not-an-envelope")


def test_validate_helpers_for_shell_package_and_exceptions() -> None:
    """Verify validate helpers on shell, exceptions, and package modules."""
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")
    exc_mod = _import_or_fail("src.core.universal.exceptions")
    pkg_mod = _import_or_fail("src.core.universal")

    assert shell_mod.validate() is True
    assert exc_mod.validate() is True
    assert pkg_mod.validate() is True
