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
"""GatewayCore minimal fail-closed orchestration for RED-SLICE-LGW-001."""

from __future__ import annotations

from typing import Any


def validate() -> bool:
    """Validate that the gateway core module contract is available.

    Returns:
        True when the module can provide the `GatewayCore` orchestration contract.

    """
    return True


class GatewayCore:
    """Coordinate policy, budget, provider, and side-effect sequencing.

    This first green slice intentionally implements only the orchestration behavior
    required by `tests/core/gateway/test_gateway_core_orchestration.py`.

    Args:
        policy_engine: Pre/post response policy evaluator.
        router: Route planner.
        provider_runtime: Provider runtime adapter.
        budget_manager: Budget reserve/commit manager.
        semantic_cache: Semantic cache adapter.
        fallback_manager: Fallback adapter placeholder for constructor parity.
        telemetry_emitter: Telemetry emitter.
        tool_skill_catcher: Tool interception adapter.

    """

    def __init__(
        self,
        *,
        policy_engine: Any,
        router: Any,
        provider_runtime: Any,
        budget_manager: Any,
        semantic_cache: Any,
        fallback_manager: Any,
        telemetry_emitter: Any,
        tool_skill_catcher: Any,
    ) -> None:
        """Store orchestration dependencies.

        Args:
            policy_engine: Pre/post response policy evaluator.
            router: Route planner.
            provider_runtime: Provider runtime adapter.
            budget_manager: Budget reserve/commit manager.
            semantic_cache: Semantic cache adapter.
            fallback_manager: Fallback adapter placeholder.
            telemetry_emitter: Telemetry emitter.
            tool_skill_catcher: Tool interception adapter.

        """
        self._policy_engine = policy_engine
        self._router = router
        self._provider_runtime = provider_runtime
        self._budget_manager = budget_manager
        self._semantic_cache = semantic_cache
        self._fallback_manager = fallback_manager
        self._telemetry_emitter = telemetry_emitter
        self._tool_skill_catcher = tool_skill_catcher

    async def handle(self, envelope: dict[str, Any]) -> dict[str, Any]:
        """Execute the fail-closed request orchestration flow.

        Args:
            envelope: Request payload.

        Returns:
            Minimal result envelope with decision, budget, and telemetry sections.

        """
        self._telemetry_emitter.emit_request_start(envelope)
        pre_decision = self._policy_engine.evaluate_pre_request(envelope)
        if not pre_decision.get("allow", False):
            result = self._build_denied_result(
                envelope=envelope,
                decision=pre_decision,
                budget={"status": "not_reserved"},
                telemetry={"degraded": False},
            )
            self._telemetry_emitter.emit_result(result)
            return result

        reservation = self._budget_manager.reserve(envelope)
        cache_lookup = self._semantic_cache.lookup(envelope)
        route = self._router.route(envelope, pre_decision)
        self._telemetry_emitter.emit_decision(pre_decision, route)

        response = await self._provider_runtime.execute(route, envelope)
        post_decision = self._policy_engine.evaluate_post_response(envelope, response)
        if not post_decision.get("allow", False):
            budget_commit = self._budget_manager.commit_failure(
                reservation,
                {"error_code": "post_policy_denied", "category": "policy"},
            )
            result = self._build_denied_result(
                envelope=envelope,
                decision=post_decision,
                budget=budget_commit,
                telemetry={"degraded": False},
            )
            result["cache"] = cache_lookup
            self._telemetry_emitter.emit_result(result)
            return result

        budget_commit = self._budget_manager.commit_success(
            reservation,
            response.get("usage", {}),
        )
        cache_write = self._semantic_cache.write(envelope, response)

        tool_audit: list[dict[str, Any]] = []
        planned_calls = envelope.get("tool_context", {}).get("planned_calls", [])
        for tool_call in planned_calls:
            tool_decision = self._tool_skill_catcher.intercept_before(envelope, tool_call)
            tool_audit.append(tool_decision)

        result: dict[str, Any] = {
            "request_id": envelope.get("request_id"),
            "correlation_id": envelope.get("correlation_id"),
            "status": "success",
            "decision": post_decision,
            "route": route,
            "provider_response": response,
            "error": None,
            "budget": budget_commit,
            "cache": cache_write,
            "tool_audit": tool_audit,
            "telemetry": {"degraded": False},
        }
        self._telemetry_emitter.emit_result(result)
        return result

    def _build_denied_result(
        self,
        *,
        envelope: dict[str, Any],
        decision: dict[str, Any],
        budget: dict[str, Any],
        telemetry: dict[str, Any],
    ) -> dict[str, Any]:
        """Build the minimal deny-path result envelope.

        Args:
            envelope: Request payload.
            decision: Policy decision payload.
            budget: Budget section payload.
            telemetry: Telemetry section payload.

        Returns:
            Denied result envelope.

        """
        return {
            "request_id": envelope.get("request_id"),
            "correlation_id": envelope.get("correlation_id"),
            "status": "denied",
            "decision": decision,
            "route": None,
            "provider_response": None,
            "error": {"error_code": "policy_denied", "category": "policy"},
            "budget": budget,
            "cache": {"hit": False},
            "tool_audit": [],
            "telemetry": telemetry,
        }
