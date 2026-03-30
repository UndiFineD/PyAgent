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

"""Data contracts for smart prompt routing."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PromptRoutingRequest:
    """Normalized request shape consumed by routing stages.

    Args:
        request_id: Stable request identifier.
        tenant_id: Tenant identifier used for policy checks.
        intent_hint: Optional intent hint from caller.
        risk_class: Risk class label.
        tool_requirement: Optional tool requirement label.
        latency_budget_ms: Per-request latency budget.
        cost_budget_class: Cost budget label.
        context_summary: Redacted context summary for classification.

    """

    request_id: str
    tenant_id: str
    intent_hint: str | None
    risk_class: str
    tool_requirement: str | None
    latency_budget_ms: int
    cost_budget_class: str
    context_summary: str


@dataclass(frozen=True)
class RouteCandidate:
    """Candidate route produced by classifier or tie-break.

    Args:
        route: Candidate route name.
        score: Candidate confidence-like score.

    """

    route: str
    score: float


@dataclass(frozen=True)
class ClassifierResult:
    """Classifier output with candidates and calibrated confidence inputs.

    Args:
        candidate_routes: Ordered candidates, highest score first.
        confidence: Confidence estimate in [0.0, 1.0].
        feature_tags: Deterministic feature attribution labels.
        model_version: Classifier model version string.

    """

    candidate_routes: list[RouteCandidate]
    confidence: float
    feature_tags: list[str] = field(default_factory=list)
    model_version: str = "deterministic-v1"


@dataclass(frozen=True)
class GuardrailOutcome:
    """Deterministic guardrail evaluation output.

    Args:
        is_resolved: True when a final route was decided by guardrails.
        route: Resolved route when available.
        policy_rules_matched: Names of matched guardrail rules.
        deny_reason: Optional deny reason when route is blocked/fallback.

    """

    is_resolved: bool
    route: str | None = None
    policy_rules_matched: list[str] = field(default_factory=list)
    deny_reason: str | None = None


@dataclass(frozen=True)
class RouteDecisionRecord:
    """Canonical route decision payload emitted by routing facade.

    Args:
        request_id: Request identifier.
        final_route: Final selected route.
        decision_stage: Stage that produced the final route.
        guardrail_hit: Whether guardrails resolved the route.
        classifier_confidence: Calibrated confidence value.
        tie_break_used: Whether tie-break stage was used.
        fallback_reason: Optional fallback reason taxonomy value.
        policy_version: Policy version applied to the decision.
        correlation_id: Correlation identifier for telemetry.

    """

    request_id: str
    final_route: str
    decision_stage: str
    guardrail_hit: bool
    classifier_confidence: float
    tie_break_used: bool
    fallback_reason: str | None
    policy_version: str
    correlation_id: str


def validate() -> bool:
    """Validate routing data model construction.

    Returns:
        True when canonical model instances can be created with expected values.

    """
    request = PromptRoutingRequest(
        request_id="validate-models",
        tenant_id="tenant",
        intent_hint=None,
        risk_class="low",
        tool_requirement=None,
        latency_budget_ms=50,
        cost_budget_class="standard",
        context_summary="validate",
    )
    candidate = RouteCandidate(route="core", score=0.9)
    result = ClassifierResult(candidate_routes=[candidate], confidence=0.9)
    outcome = GuardrailOutcome(is_resolved=False)
    record = RouteDecisionRecord(
        request_id=request.request_id,
        final_route="core",
        decision_stage="classifier",
        guardrail_hit=False,
        classifier_confidence=result.confidence,
        tie_break_used=False,
        fallback_reason=None,
        policy_version="spr-v1",
        correlation_id="corr-validate",
    )
    return (
        request.tenant_id == "tenant"
        and result.candidate_routes[0].route == "core"
        and not outcome.is_resolved
        and record.final_route == "core"
    )
