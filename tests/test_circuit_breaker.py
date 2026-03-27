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

"""Tests for src.core.resilience circuit-breaker behavior (TDD red phase).

This file contains the 20 contract tests defined in the prj0000083 plan:
U1-U9, R1-R4, M1-M5, and I1-I2.
"""

from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable

import pytest

import src.core.resilience as resilience_pkg
from src.core.resilience import (  # type: ignore[import]
    AllCircuitsOpenError,
    CircuitBreakerConfig,
    CircuitBreakerCore,
    CircuitBreakerMixin,
    CircuitBreakerRegistry,
    CircuitBreakerState,
    CircuitOpenError,
    CircuitState,
)
from src.core.resilience.CircuitBreakerConfig import validate as validate_config
from src.core.resilience.CircuitBreakerCore import validate as validate_core
from src.core.resilience.CircuitBreakerMixin import validate as validate_mixin
from src.core.resilience.CircuitBreakerRegistry import validate as validate_registry
from src.core.resilience.CircuitBreakerState import validate as validate_state
from src.core.resilience.exceptions import validate as validate_exceptions


class _Agent(CircuitBreakerMixin):
    """Minimal concrete mixin host used by mixin contract tests."""

    def __init__(self, registry: CircuitBreakerRegistry) -> None:
        """Initialize with an injected circuit-breaker registry."""
        self._circuit_breaker_registry = registry


# ===========================================================================
# Unit tests — CircuitBreakerCore (U1-U9)
# ===========================================================================


def test_core_initial_state_closed() -> None:
    """Verify a fresh provider state starts CLOSED with zero counters."""
    state = CircuitBreakerState(provider_key="p")
    assert state.state == CircuitState.CLOSED
    assert state.consecutive_failures == 0
    assert state.probe_in_flight is False


def test_core_record_failure_increments_consecutive() -> None:
    """Verify one failure increments counters but stays CLOSED below threshold."""
    core = CircuitBreakerCore()
    config = CircuitBreakerConfig(provider_key="p", failure_threshold=5)
    state = CircuitBreakerState(provider_key="p")

    core.record_failure(state, config)

    assert state.consecutive_failures == 1
    assert state.total_failures == 1
    assert state.state == CircuitState.CLOSED


def test_core_opens_after_failure_threshold(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify reaching threshold transitions CLOSED to OPEN and records failure time."""
    core = CircuitBreakerCore()
    config = CircuitBreakerConfig(provider_key="p", failure_threshold=3)
    state = CircuitBreakerState(provider_key="p")

    monkeypatch.setattr("src.core.resilience.CircuitBreakerCore.time.monotonic", lambda: 123.0)

    core.record_failure(state, config)
    core.record_failure(state, config)
    core.record_failure(state, config)

    assert state.state == CircuitState.OPEN
    assert state.consecutive_failures == 3
    assert state.last_failure_time == 123.0


def test_core_half_open_after_recovery_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify OPEN transitions to HALF_OPEN and grants exactly one probe after timeout."""
    core = CircuitBreakerCore()
    config = CircuitBreakerConfig(provider_key="p", recovery_timeout=30.0)
    state = CircuitBreakerState(provider_key="p", state=CircuitState.OPEN, last_failure_time=10.0)

    monkeypatch.setattr("src.core.resilience.CircuitBreakerCore.time.monotonic", lambda: 50.0)

    allowed = core.should_allow(state, config)

    assert allowed is True
    assert state.state == CircuitState.HALF_OPEN
    assert state.probe_in_flight is True


def test_core_probe_success_transitions_to_closed() -> None:
    """Verify a successful HALF_OPEN probe closes the circuit and clears probe flag."""
    core = CircuitBreakerCore()
    state = CircuitBreakerState(
        provider_key="p",
        state=CircuitState.HALF_OPEN,
        probe_in_flight=True,
        consecutive_failures=3,
    )

    core.record_success(state)

    assert state.state == CircuitState.CLOSED
    assert state.consecutive_failures == 0
    assert state.probe_in_flight is False
    assert state.total_successes == 1


def test_core_probe_failure_resets_to_open(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify a failed HALF_OPEN probe moves back to OPEN and refreshes failure time."""
    core = CircuitBreakerCore()
    config = CircuitBreakerConfig(provider_key="p", failure_threshold=5)
    state = CircuitBreakerState(provider_key="p", state=CircuitState.HALF_OPEN, probe_in_flight=True)

    monkeypatch.setattr("src.core.resilience.CircuitBreakerCore.time.monotonic", lambda: 321.0)

    core.record_failure(state, config)

    assert state.state == CircuitState.OPEN
    assert state.probe_in_flight is False
    assert state.last_failure_time == 321.0


def test_core_half_open_probe_exclusivity() -> None:
    """Verify only one in-flight probe is allowed while HALF_OPEN."""
    core = CircuitBreakerCore()
    config = CircuitBreakerConfig(provider_key="p", recovery_timeout=30.0)
    state = CircuitBreakerState(provider_key="p", state=CircuitState.HALF_OPEN, probe_in_flight=True)

    allowed = core.should_allow(state, config)

    assert allowed is False
    assert state.probe_in_flight is True
    assert state.state == CircuitState.HALF_OPEN


def test_core_reset_forces_closed() -> None:
    """Verify reset clears failures and forces CLOSED from OPEN."""
    core = CircuitBreakerCore()
    state = CircuitBreakerState(
        provider_key="p",
        state=CircuitState.OPEN,
        consecutive_failures=10,
        probe_in_flight=False,
    )

    core.reset(state)

    assert state.state == CircuitState.CLOSED
    assert state.consecutive_failures == 0
    assert state.probe_in_flight is False


def test_core_record_success_increments_counters() -> None:
    """Verify success increments success counter and does not create failures."""
    core = CircuitBreakerCore()
    state = CircuitBreakerState(provider_key="p", state=CircuitState.CLOSED, total_successes=0)

    core.record_success(state)

    assert state.total_successes == 1
    assert state.consecutive_failures == 0
    assert state.state == CircuitState.CLOSED


def test_core_should_allow_denies_open_before_recovery(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify OPEN state denies calls until recovery timeout has elapsed."""
    core = CircuitBreakerCore()
    config = CircuitBreakerConfig(provider_key="p", recovery_timeout=30.0)
    state = CircuitBreakerState(provider_key="p", state=CircuitState.OPEN, last_failure_time=10.0)

    monkeypatch.setattr("src.core.resilience.CircuitBreakerCore.time.monotonic", lambda: 20.0)

    allowed = core.should_allow(state, config)

    assert allowed is False
    assert state.state == CircuitState.OPEN


def test_core_check_state_returns_existing_non_open_state() -> None:
    """Verify check_state keeps CLOSED state unchanged when not OPEN."""
    core = CircuitBreakerCore()
    config = CircuitBreakerConfig(provider_key="p")
    state = CircuitBreakerState(provider_key="p", state=CircuitState.CLOSED)

    current = core.check_state(state, config)

    assert current == CircuitState.CLOSED


# ===========================================================================
# Unit tests — CircuitBreakerRegistry (R1-R4)
# ===========================================================================


@pytest.mark.asyncio
async def test_registry_get_or_create_same_key_returns_same_object() -> None:
    """Verify get_or_create returns object-identity stable state for same key."""
    registry = CircuitBreakerRegistry()
    config = CircuitBreakerConfig(provider_key="k")

    s1 = await registry.get_or_create("k", config)
    s2 = await registry.get_or_create("k", config)

    assert s1 is s2


@pytest.mark.asyncio
async def test_registry_get_fallback_returns_first_closed_provider() -> None:
    """Verify fallback selection skips OPEN providers and returns first CLOSED candidate."""
    registry = CircuitBreakerRegistry()
    primary_cfg = CircuitBreakerConfig(provider_key="primary", fallback_providers=["a", "b"])
    fallback_a_cfg = CircuitBreakerConfig(provider_key="a")
    fallback_b_cfg = CircuitBreakerConfig(provider_key="b")

    state_a = await registry.get_or_create("a", fallback_a_cfg)
    state_b = await registry.get_or_create("b", fallback_b_cfg)
    state_a.state = CircuitState.OPEN
    state_b.state = CircuitState.CLOSED

    chosen = await registry.get_fallback("primary", primary_cfg)

    assert chosen == "b"


@pytest.mark.asyncio
async def test_registry_get_fallback_returns_none_when_all_open() -> None:
    """Verify fallback selection returns None when every configured fallback is OPEN."""
    registry = CircuitBreakerRegistry()
    primary_cfg = CircuitBreakerConfig(provider_key="primary", fallback_providers=["a"])
    fallback_cfg = CircuitBreakerConfig(provider_key="a")

    state_a = await registry.get_or_create("a", fallback_cfg)
    state_a.state = CircuitState.OPEN

    chosen = await registry.get_fallback("primary", primary_cfg)

    assert chosen is None


@pytest.mark.asyncio
async def test_registry_record_and_allow_delegate_to_core() -> None:
    """Verify record_failure and should_allow produce OPEN behavior after threshold."""
    registry = CircuitBreakerRegistry()
    config = CircuitBreakerConfig(provider_key="p", failure_threshold=3)

    await registry.get_or_create("p", config)
    await registry.record_failure("p", config)
    await registry.record_failure("p", config)
    await registry.record_failure("p", config)

    allowed = await registry.should_allow("p", config)

    assert allowed is False


@pytest.mark.asyncio
async def test_registry_state_creation_and_config_resolution_paths() -> None:
    """Verify registry methods create missing states and resolve default and cached configs."""
    registry = CircuitBreakerRegistry()

    await registry.record_success("s")
    await registry.record_failure("f")
    await registry.reset("r")

    assert "s" in registry._states
    assert "f" in registry._states
    assert "r" in registry._states

    primary_cfg = CircuitBreakerConfig(provider_key="primary", fallback_providers=["missing-fb"])
    chosen = await registry.get_fallback("primary", primary_cfg)
    assert chosen == "missing-fb"
    assert "missing-fb" in registry._states

    seeded_cfg = CircuitBreakerConfig(provider_key="seeded", failure_threshold=2)
    await registry.get_or_create("seeded", seeded_cfg)
    await registry.should_allow("seeded")
    assert registry._configs["seeded"].failure_threshold == 2


# ===========================================================================
# Unit tests — CircuitBreakerMixin (M1-M5)
# ===========================================================================


@pytest.mark.asyncio
async def test_mixin_cb_call_returns_coro_result_on_success() -> None:
    """Verify cb_call returns result and records success on happy path."""
    registry = CircuitBreakerRegistry()
    config = CircuitBreakerConfig(provider_key="p")
    agent = _Agent(registry)

    async def _ok() -> int:
        """Return a deterministic integer payload."""
        return 42

    result = await agent.cb_call("p", _ok, config)

    state = await registry.get_or_create("p", config)
    assert result == 42
    assert state.total_successes == 1


@pytest.mark.asyncio
async def test_mixin_cb_call_records_failure_and_reraises() -> None:
    """Verify cb_call records a failure and propagates the original exception."""
    registry = CircuitBreakerRegistry()
    config = CircuitBreakerConfig(provider_key="p")
    agent = _Agent(registry)

    async def _boom() -> int:
        """Raise a deterministic runtime error for failure-path testing."""
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        await agent.cb_call("p", _boom, config)

    state = await registry.get_or_create("p", config)
    assert state.total_failures == 1


@pytest.mark.asyncio
async def test_mixin_cb_call_open_circuit_raises_circuit_open_error_without_calling_coro() -> None:
    """Verify OPEN primary raises CircuitOpenError and does not await the call coroutine."""
    registry = CircuitBreakerRegistry()
    config = CircuitBreakerConfig(provider_key="p", failure_threshold=1)
    agent = _Agent(registry)

    await registry.get_or_create("p", config)
    await registry.record_failure("p", config)

    was_called = {"value": False}

    async def _should_not_run() -> int:
        """Mark execution and return an integer if unexpectedly awaited."""
        was_called["value"] = True
        return 1

    with pytest.raises(CircuitOpenError):
        await agent.cb_call("p", _should_not_run, config)

    assert was_called["value"] is False


@pytest.mark.asyncio
async def test_mixin_cb_call_routes_to_fallback_when_primary_open() -> None:
    """Verify cb_call uses fallback provider when primary circuit is OPEN."""
    registry = CircuitBreakerRegistry()
    primary_cfg = CircuitBreakerConfig(provider_key="primary", failure_threshold=1, fallback_providers=["fallback"])
    fallback_cfg = CircuitBreakerConfig(provider_key="fallback")
    agent = _Agent(registry)

    await registry.get_or_create("primary", primary_cfg)
    await registry.get_or_create("fallback", fallback_cfg)
    await registry.record_failure("primary", primary_cfg)

    async def _ok() -> str:
        """Return a deterministic response when fallback path is selected."""
        return "ok"

    result = await agent.cb_call("primary", _ok, primary_cfg)

    fallback_state = await registry.get_or_create("fallback", fallback_cfg)
    assert result == "ok"
    assert fallback_state.total_successes == 1


@pytest.mark.asyncio
async def test_mixin_cb_call_raises_all_circuits_open_when_exhausted() -> None:
    """Verify cb_call raises AllCircuitsOpenError when primary and fallbacks are OPEN."""
    registry = CircuitBreakerRegistry()
    primary_cfg = CircuitBreakerConfig(provider_key="primary", failure_threshold=1, fallback_providers=["f1", "f2"])
    fallback_cfg_1 = CircuitBreakerConfig(provider_key="f1", failure_threshold=1)
    fallback_cfg_2 = CircuitBreakerConfig(provider_key="f2", failure_threshold=1)
    agent = _Agent(registry)

    await registry.get_or_create("primary", primary_cfg)
    await registry.get_or_create("f1", fallback_cfg_1)
    await registry.get_or_create("f2", fallback_cfg_2)
    await registry.record_failure("primary", primary_cfg)
    await registry.record_failure("f1", fallback_cfg_1)
    await registry.record_failure("f2", fallback_cfg_2)

    async def _never() -> int:
        """Return a deterministic value if unexpectedly executed."""
        return 0

    with pytest.raises(AllCircuitsOpenError) as exc_info:
        await agent.cb_call("primary", _never, primary_cfg)

    assert exc_info.value.tried_keys == ["primary", "f1", "f2"]


# ===========================================================================
# Integration tests (I1-I2)
# ===========================================================================


@pytest.mark.asyncio
async def test_integration_open_then_half_open_then_closed_full_cycle(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify OPEN -> HALF_OPEN -> CLOSED transition cycle for one provider."""
    registry = CircuitBreakerRegistry()
    config = CircuitBreakerConfig(provider_key="p", failure_threshold=3, recovery_timeout=0.05)

    await registry.get_or_create("p", config)
    await registry.record_failure("p", config)
    await registry.record_failure("p", config)
    await registry.record_failure("p", config)

    allowed_while_open = await registry.should_allow("p", config)
    assert allowed_while_open is False

    await asyncio.sleep(0.06)

    allowed_probe = await registry.should_allow("p", config)
    assert allowed_probe is True

    await registry.record_success("p", config)

    state = await registry.get_or_create("p", config)
    assert state.state == CircuitState.CLOSED
    assert state.total_failures == 3
    assert state.total_successes == 1


@pytest.mark.asyncio
async def test_integration_concurrent_half_open_only_one_probe_passes() -> None:
    """Verify concurrent HALF_OPEN checks allow exactly one probe task."""
    registry = CircuitBreakerRegistry()
    config = CircuitBreakerConfig(provider_key="p")
    state = await registry.get_or_create("p", config)
    state.state = CircuitState.HALF_OPEN
    state.probe_in_flight = False

    async def _attempt() -> bool:
        """Attempt to acquire HALF_OPEN probe permission once."""
        return await registry.should_allow("p", config)

    results = await asyncio.gather(*[_attempt() for _ in range(10)])

    assert sum(1 for value in results if value) == 1
    assert sum(1 for value in results if not value) == 9


def test_module_validate_helpers_and_exception_attributes() -> None:
    """Verify package helper validation hooks and exception payload attributes."""
    assert resilience_pkg.validate() is True
    assert validate_config() is True
    assert validate_core() is True
    assert validate_mixin() is True
    assert validate_registry() is True
    assert validate_state() is True
    assert validate_exceptions() is True

    err = CircuitOpenError("provider-a", CircuitState.OPEN)
    assert err.provider_key == "provider-a"
    assert err.state == CircuitState.OPEN
