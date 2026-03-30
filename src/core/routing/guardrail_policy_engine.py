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

"""Deterministic guardrail evaluation for smart prompt routing."""

from __future__ import annotations

from src.core.routing.routing_models import GuardrailOutcome, PromptRoutingRequest


class GuardrailPolicyEngine:
    """Evaluate hard routing constraints before classifier stages."""

    def evaluate(self, request: PromptRoutingRequest) -> GuardrailOutcome:
        """Evaluate guardrails for one request.

        Args:
            request: Normalized routing request.

        Returns:
            GuardrailOutcome representing either resolution or unresolved state.

        """
        risk_class = request.risk_class.strip().lower()
        tool_requirement = (request.tool_requirement or "").strip().lower()

        if risk_class in {"critical", "high"}:
            return GuardrailOutcome(
                is_resolved=True,
                route="safe_default",
                policy_rules_matched=["risk_high_safe_default"],
                deny_reason="guardrail_deny",
            )

        if tool_requirement == "legacy_only":
            return GuardrailOutcome(
                is_resolved=True,
                route="legacy",
                policy_rules_matched=["tool_legacy_only"],
                deny_reason=None,
            )

        return GuardrailOutcome(is_resolved=False)


def validate() -> bool:
    """Validate deterministic guardrail resolution behavior.

    Returns:
        True when high-risk requests are resolved to safe_default.

    """
    outcome = GuardrailPolicyEngine().evaluate(
        PromptRoutingRequest(
            request_id="validate-guardrail",
            tenant_id="tenant",
            intent_hint=None,
            risk_class="high",
            tool_requirement=None,
            latency_budget_ms=50,
            cost_budget_class="standard",
            context_summary="validate",
        )
    )
    return outcome.is_resolved and outcome.route == "safe_default"
