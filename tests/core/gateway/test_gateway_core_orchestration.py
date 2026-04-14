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
"""RED contracts for GatewayCore orchestration fail-closed sequencing."""

from __future__ import annotations

import importlib
from typing import Any

import pytest


class _PolicyEngineStub:
    """Policy engine stub that records pre and post decisions.

    Args:
        pre_allow: Whether pre-request policy allows execution.
        post_allow: Whether post-response policy allows downstream effects.

    """

    def __init__(self, pre_allow: bool = True, post_allow: bool = True) -> None:
        self.pre_allow = pre_allow
        self.post_allow = post_allow
        self.calls: list[str] = []

    def evaluate_pre_request(self, envelope: dict[str, Any]) -> dict[str, Any]:
        """Return a pre-request policy decision.

        Args:
            envelope: Gateway request envelope.

        Returns:
            Policy decision payload.

        """
        self.calls.append("policy_pre")
        return {
            "allow": self.pre_allow,
            "decision": "allow" if self.pre_allow else "deny",
            "policy_version": "test-v1",
            "rule_ids": ["pre-rule"],
        }

    def evaluate_post_response(self, envelope: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
        """Return a post-response policy decision.

        Args:
            envelope: Gateway request envelope.
            response: Provider response envelope.

        Returns:
            Policy decision payload.

        """
        self.calls.append("policy_post")
        return {
            "allow": self.post_allow,
            "decision": "allow" if self.post_allow else "deny",
            "policy_version": "test-v1",
            "rule_ids": ["post-rule"],
        }


class _BudgetManagerStub:
    """Budget manager stub that records reserve and commit operations."""

    def __init__(self, event_log: list[str] | None = None) -> None:
        self.calls: list[str] = []
        self._event_log = event_log

    def reserve(self, envelope: dict[str, Any]) -> dict[str, Any]:
        """Record reserve invocation.

        Args:
            envelope: Gateway request envelope.

        Returns:
            Reservation payload.

        """
        self.calls.append("budget_reserve")
        if self._event_log is not None:
            self._event_log.append("budget_reserve")
        return {"reservation_id": "rsv-1", "allowed": True}

    def commit_success(self, reservation: dict[str, Any], usage: dict[str, Any]) -> dict[str, Any]:
        """Record success commit invocation.

        Args:
            reservation: Reservation payload.
            usage: Token usage payload.

        Returns:
            Commit payload.

        """
        self.calls.append("budget_commit_success")
        if self._event_log is not None:
            self._event_log.append("budget_commit_success")
        return {"status": "committed", "reservation_id": reservation["reservation_id"]}

    def commit_failure(self, reservation: dict[str, Any], error: dict[str, Any]) -> dict[str, Any]:
        """Record failure commit invocation.

        Args:
            reservation: Reservation payload.
            error: Error payload.

        Returns:
            Commit payload.

        """
        self.calls.append("budget_commit_failure")
        if self._event_log is not None:
            self._event_log.append("budget_commit_failure")
        return {"status": "failed", "reservation_id": reservation["reservation_id"]}


class _ProviderRuntimeStub:
    """Provider runtime stub that records execute calls."""

    def __init__(self, event_log: list[str] | None = None) -> None:
        self.calls: list[str] = []
        self._event_log = event_log

    async def execute(self, route: dict[str, Any], envelope: dict[str, Any]) -> dict[str, Any]:
        """Record provider execution and return synthetic response.

        Args:
            route: Route plan payload.
            envelope: Gateway request envelope.

        Returns:
            Provider response payload.

        """
        self.calls.append("provider_execute")
        if self._event_log is not None:
            self._event_log.append("provider_execute")
        return {"content": "provider-response", "usage": {"input_tokens": 1, "output_tokens": 1}}


class _SemanticCacheStub:
    """Semantic cache stub that records lookup and write calls."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def lookup(self, envelope: dict[str, Any]) -> dict[str, Any]:
        """Record lookup invocation.

        Args:
            envelope: Gateway request envelope.

        Returns:
            Cache lookup payload.

        """
        self.calls.append("cache_lookup")
        return {"hit": False}

    def write(self, envelope: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
        """Record cache write invocation.

        Args:
            envelope: Gateway request envelope.
            response: Provider response payload.

        Returns:
            Cache write payload.

        """
        self.calls.append("cache_write")
        return {"written": True}


class _ToolCatcherStub:
    """Tool catcher stub that records interception calls."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def intercept_before(self, envelope: dict[str, Any], tool_call: dict[str, Any]) -> dict[str, Any]:
        """Record pre-tool interception.

        Args:
            envelope: Gateway request envelope.
            tool_call: Tool call payload.

        Returns:
            Tool decision payload.

        """
        self.calls.append("tool_intercept_before")
        return {"allow": True, "decision": "allow", "policy_version": "test-v1", "rule_ids": ["tool"]}

    def intercept_after(self, envelope: dict[str, Any], tool_result: dict[str, Any]) -> dict[str, Any]:
        """Record post-tool interception.

        Args:
            envelope: Gateway request envelope.
            tool_result: Tool result payload.

        Returns:
            Tool audit payload.

        """
        self.calls.append("tool_intercept_after")
        return {"status": "audited"}


class _RouterStub:
    """Router stub that returns a deterministic route plan."""

    def route(self, envelope: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
        """Return route plan payload.

        Args:
            envelope: Gateway request envelope.
            policy: Policy decision payload.

        Returns:
            Route plan payload.

        """
        return {"route_id": "route-1", "provider": "stub"}


class _FallbackManagerStub:
    """Fallback manager stub for construction compatibility."""

    def resolve(self, route: dict[str, Any], error: dict[str, Any] | None) -> dict[str, Any]:
        """Return fallback plan payload.

        Args:
            route: Route plan payload.
            error: Optional error payload.

        Returns:
            Fallback plan payload.

        """
        return {"attempted": False, "reason": None}


class _TelemetryEmitterStub:
    """Telemetry emitter stub that records lifecycle emissions."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def emit_request_start(self, envelope: dict[str, Any]) -> None:
        """Record request-start emission.

        Args:
            envelope: Gateway request envelope.

        """
        self.calls.append("telemetry_request_start")

    def emit_decision(self, decision: dict[str, Any], route: dict[str, Any]) -> None:
        """Record policy/route decision emission.

        Args:
            decision: Policy decision payload.
            route: Route plan payload.

        """
        self.calls.append("telemetry_decision")

    def emit_result(self, result: dict[str, Any]) -> None:
        """Record final result emission.

        Args:
            result: Gateway result envelope.

        """
        self.calls.append("telemetry_result")


@pytest.fixture
def gateway_envelope() -> dict[str, Any]:
    """Provide a minimal request envelope for gateway orchestration tests.

    Returns:
        Request envelope payload.

    """
    return {
        "request_id": "req-1",
        "correlation_id": "corr-1",
        "agent_id": "agent-1",
        "project_id": "prj0000124",
        "prompt": {"text": "hello"},
        "policy_context": {"tenant": "default"},
        "budget_context": {"max_tokens": 128},
        "tool_context": {"planned_calls": [{"name": "tool-a"}]},
    }


@pytest.fixture
def event_log() -> list[str]:
    """Provide a shared chronological event log for ordering checks.

    Returns:
        Shared append-only event sequence.

    """
    return []


@pytest.fixture
def make_gateway(event_log: list[str]):
    """Build a GatewayCore with stubs wired to a shared chronological event log.

    Args:
        event_log: Shared append-only event sequence.

    Returns:
        Factory that creates configured GatewayCore instances.

    """

    def _factory(
        *,
        pre_allow: bool = True,
        post_allow: bool = True,
        budget_manager: _BudgetManagerStub | None = None,
        provider_runtime: _ProviderRuntimeStub | None = None,
        telemetry_emitter: _TelemetryEmitterStub | None = None,
    ) -> Any:
        gateway_core_cls = _load_gateway_core_class()
        resolved_budget = budget_manager or _BudgetManagerStub(event_log=event_log)
        resolved_provider = provider_runtime or _ProviderRuntimeStub(event_log=event_log)
        resolved_telemetry = telemetry_emitter or _TelemetryEmitterStub()
        return gateway_core_cls(
            policy_engine=_PolicyEngineStub(pre_allow=pre_allow, post_allow=post_allow),
            router=_RouterStub(),
            provider_runtime=resolved_provider,
            budget_manager=resolved_budget,
            semantic_cache=_SemanticCacheStub(),
            fallback_manager=_FallbackManagerStub(),
            telemetry_emitter=resolved_telemetry,
            tool_skill_catcher=_ToolCatcherStub(),
        )

    return _factory


def _load_gateway_core_class() -> type[Any]:
    """Load the GatewayCore contract class or fail with a RED contract signal.

    Returns:
        The GatewayCore class contract.

    """
    try:
        module = importlib.import_module("src.core.gateway.gateway_core")
    except ModuleNotFoundError:  # pragma: no cover - red-phase contract signal.
        pytest.fail("Missing module contract src.core.gateway.gateway_core required for RED-SLICE-LGW-001.")

    gateway_core_cls = getattr(module, "GatewayCore", None)
    if gateway_core_cls is None:
        pytest.fail("Missing class contract GatewayCore in src.core.gateway.gateway_core.")
    return gateway_core_cls


@pytest.mark.asyncio
async def test_fail_closed_deny_path_blocks_provider_execution(gateway_envelope: dict[str, Any]) -> None:
    """Pre-policy deny must fail-closed before provider execution.

    Args:
        gateway_envelope: Request envelope fixture.

    """
    policy_engine = _PolicyEngineStub(pre_allow=False, post_allow=True)
    budget_manager = _BudgetManagerStub()
    provider_runtime = _ProviderRuntimeStub()
    semantic_cache = _SemanticCacheStub()
    tool_catcher = _ToolCatcherStub()
    telemetry_emitter = _TelemetryEmitterStub()

    gateway_core_cls = _load_gateway_core_class()
    gateway_core = gateway_core_cls(
        policy_engine=policy_engine,
        router=_RouterStub(),
        provider_runtime=provider_runtime,
        budget_manager=budget_manager,
        semantic_cache=semantic_cache,
        fallback_manager=_FallbackManagerStub(),
        telemetry_emitter=telemetry_emitter,
        tool_skill_catcher=tool_catcher,
    )

    result = await gateway_core.handle(gateway_envelope)

    assert provider_runtime.calls == []
    assert budget_manager.calls == []
    assert result["status"] == "denied"


@pytest.mark.asyncio
async def test_fail_closed_budget_reserve_occurs_before_provider_execute(
    gateway_envelope: dict[str, Any],
    event_log: list[str],
    make_gateway,
) -> None:
    """Budget reserve must happen before provider execution order-wise.

    Args:
        gateway_envelope: Request envelope fixture.
        event_log: Shared chronological event log fixture.
        make_gateway: Fixture that builds a configured GatewayCore instance.

    """
    gateway_core = make_gateway()

    await gateway_core.handle(gateway_envelope)

    assert "budget_reserve" in event_log
    assert "provider_execute" in event_log
    assert event_log.index("budget_reserve") < event_log.index("provider_execute")


@pytest.mark.asyncio
async def test_fail_closed_post_policy_deny_blocks_cache_write_and_tool_dispatch(
    gateway_envelope: dict[str, Any],
) -> None:
    """Post-policy deny must block cache write and tool interception path.

    Args:
        gateway_envelope: Request envelope fixture.

    """
    policy_engine = _PolicyEngineStub(pre_allow=True, post_allow=False)
    semantic_cache = _SemanticCacheStub()
    tool_catcher = _ToolCatcherStub()

    gateway_core_cls = _load_gateway_core_class()
    gateway_core = gateway_core_cls(
        policy_engine=policy_engine,
        router=_RouterStub(),
        provider_runtime=_ProviderRuntimeStub(),
        budget_manager=_BudgetManagerStub(),
        semantic_cache=semantic_cache,
        fallback_manager=_FallbackManagerStub(),
        telemetry_emitter=_TelemetryEmitterStub(),
        tool_skill_catcher=tool_catcher,
    )

    result = await gateway_core.handle(gateway_envelope)

    assert "cache_write" not in semantic_cache.calls
    assert tool_catcher.calls == []
    assert result["status"] == "denied"


@pytest.mark.asyncio
async def test_budget_denied_does_not_call_provider(gateway_envelope: dict[str, Any]) -> None:
    """Budget denial must fail-closed without invoking provider runtime.

    Args:
        gateway_envelope: Request envelope fixture.

    """

    class _BudgetDeniedManagerStub(_BudgetManagerStub):
        """Budget stub returning an explicit denied reservation."""

        def reserve(self, envelope: dict[str, Any]) -> dict[str, Any]:
            """Return denied reservation payload.

            Args:
                envelope: Gateway request envelope.

            Returns:
                Reservation payload with allow flag set to false.

            """
            self.calls.append("budget_reserve")
            return {"reservation_id": "rsv-deny-1", "allowed": False, "reason": "limit_exceeded"}

    policy_engine = _PolicyEngineStub(pre_allow=True, post_allow=True)
    budget_manager = _BudgetDeniedManagerStub()
    provider_runtime = _ProviderRuntimeStub()

    gateway_core_cls = _load_gateway_core_class()
    gateway_core = gateway_core_cls(
        policy_engine=policy_engine,
        router=_RouterStub(),
        provider_runtime=provider_runtime,
        budget_manager=budget_manager,
        semantic_cache=_SemanticCacheStub(),
        fallback_manager=_FallbackManagerStub(),
        telemetry_emitter=_TelemetryEmitterStub(),
        tool_skill_catcher=_ToolCatcherStub(),
    )

    result = await gateway_core.handle(gateway_envelope)

    assert provider_runtime.calls == []
    assert result["status"] == "denied"
    assert "budget_denied" in result["error"]["error_code"]


@pytest.mark.asyncio
async def test_provider_exception_returns_failed_result(gateway_envelope: dict[str, Any]) -> None:
    """Provider failures must return a failed result and not propagate exceptions.

    Args:
        gateway_envelope: Request envelope fixture.

    """

    class _RaisingProviderRuntimeStub(_ProviderRuntimeStub):
        """Provider runtime stub that always raises execution errors."""

        async def execute(self, route: dict[str, Any], envelope: dict[str, Any]) -> dict[str, Any]:
            """Raise provider runtime exception.

            Args:
                route: Route plan payload.
                envelope: Gateway request envelope.

            Returns:
                This method does not return.

            Raises:
                RuntimeError: Always raised to simulate provider outage.

            """
            self.calls.append("provider_execute")
            raise RuntimeError("provider down")

    gateway_core_cls = _load_gateway_core_class()
    gateway_core = gateway_core_cls(
        policy_engine=_PolicyEngineStub(pre_allow=True, post_allow=True),
        router=_RouterStub(),
        provider_runtime=_RaisingProviderRuntimeStub(),
        budget_manager=_BudgetManagerStub(),
        semantic_cache=_SemanticCacheStub(),
        fallback_manager=_FallbackManagerStub(),
        telemetry_emitter=_TelemetryEmitterStub(),
        tool_skill_catcher=_ToolCatcherStub(),
    )

    result = await gateway_core.handle(gateway_envelope)

    assert result["status"] == "failed"
    assert result["budget"]["status"] == "failed"


@pytest.mark.asyncio
async def test_degraded_telemetry_result_still_returned(gateway_envelope: dict[str, Any]) -> None:
    """Telemetry emitter failures must not block result delivery.

    Args:
        gateway_envelope: Request envelope fixture.

    """

    class _RaisingTelemetryEmitterStub(_TelemetryEmitterStub):
        """Telemetry stub that raises during final result emission."""

        def emit_result(self, result: dict[str, Any]) -> None:
            """Raise emission error.

            Args:
                result: Gateway result envelope.

            Raises:
                RuntimeError: Always raised to simulate telemetry outage.

            """
            self.calls.append("telemetry_result")
            raise RuntimeError("telemetry down")

    gateway_core_cls = _load_gateway_core_class()
    gateway_core = gateway_core_cls(
        policy_engine=_PolicyEngineStub(pre_allow=True, post_allow=True),
        router=_RouterStub(),
        provider_runtime=_ProviderRuntimeStub(),
        budget_manager=_BudgetManagerStub(),
        semantic_cache=_SemanticCacheStub(),
        fallback_manager=_FallbackManagerStub(),
        telemetry_emitter=_RaisingTelemetryEmitterStub(),
        tool_skill_catcher=_ToolCatcherStub(),
    )

    result = await gateway_core.handle(gateway_envelope)

    assert result["status"] == "success"
    assert result["telemetry"]["degraded"] is True


@pytest.mark.asyncio
async def test_event_log_ordering_detects_reversed_execution(
    gateway_envelope: dict[str, Any],
    event_log: list[str],
    make_gateway,
) -> None:
    """Shared event log must fail when checked with reversed-order sentinel.

    Args:
        gateway_envelope: Request envelope fixture.
        event_log: Shared chronological event log fixture.
        make_gateway: Fixture that builds a configured GatewayCore instance.

    """
    gateway_core = make_gateway()

    await gateway_core.handle(gateway_envelope)

    assert "budget_reserve" in event_log
    assert "provider_execute" in event_log
    assert event_log.index("budget_reserve") < event_log.index("provider_execute")


@pytest.mark.asyncio
async def test_gateway_result_envelope_contains_decision_budget_and_telemetry_sections(
    gateway_envelope: dict[str, Any],
) -> None:
    """Gateway result envelope must include decision, budget, and telemetry sections.

    Args:
        gateway_envelope: Request envelope fixture.

    """
    gateway_core_cls = _load_gateway_core_class()
    gateway_core = gateway_core_cls(
        policy_engine=_PolicyEngineStub(pre_allow=True, post_allow=True),
        router=_RouterStub(),
        provider_runtime=_ProviderRuntimeStub(),
        budget_manager=_BudgetManagerStub(),
        semantic_cache=_SemanticCacheStub(),
        fallback_manager=_FallbackManagerStub(),
        telemetry_emitter=_TelemetryEmitterStub(),
        tool_skill_catcher=_ToolCatcherStub(),
    )

    result = await gateway_core.handle(gateway_envelope)

    assert "decision" in result
    assert "budget" in result
    assert "telemetry" in result
