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

"""Tie-break unresolved fallback contract tests."""

from __future__ import annotations

import pytest

from src.core.routing.prompt_routing_facade import PromptRoutingFacade
from src.core.routing.routing_models import ClassifierResult, PromptRoutingRequest, RouteCandidate


class _LowConfidenceClassifier:
    """Classifier forcing tie-break with low confidence."""

    def classify(self, request: PromptRoutingRequest) -> ClassifierResult:
        """Return ambiguous result to enter tie-break path.

        Args:
            request: Routing request.

        Returns:
            Ambiguous classifier result.

        """
        _ = request
        return ClassifierResult(
            candidate_routes=[RouteCandidate(route="legacy", score=0.5), RouteCandidate(route="core", score=0.5)],
            confidence=0.45,
            feature_tags=["ambiguous"],
        )


class _UnresolvedTieBreakResolver:
    """Tie-break test double returning unresolved decision."""

    def resolve(self, candidates: list[RouteCandidate], *, timeout_ms: int, seed: str) -> RouteCandidate | None:
        """Return None to force unresolved fallback path.

        Args:
            candidates: Candidate list.
            timeout_ms: Timeout budget.
            seed: Deterministic seed.

        Returns:
            None to simulate unresolved tie-break.

        """
        _ = candidates
        _ = timeout_ms
        _ = seed
        return None


@pytest.mark.asyncio
async def test_tie_break_unresolved_triggers_fail_closed_fallback() -> None:
    """Unresolved tie-break must return fail-closed fallback decision."""
    facade = PromptRoutingFacade(
        classifier=_LowConfidenceClassifier(),
        tie_break_resolver=_UnresolvedTieBreakResolver(),
        policy={"policy_version": "spr-v1", "confidence_threshold": 0.75, "tie_break_timeout_ms": 20},
    )
    request = PromptRoutingRequest(
        request_id="req-unresolved",
        tenant_id="tenant-1",
        intent_hint="unknown",
        risk_class="low",
        tool_requirement=None,
        latency_budget_ms=30,
        cost_budget_class="normal",
        context_summary="fallback context",
    )

    record = await facade.route(request)
    assert record.decision_stage == "fallback"
    assert record.final_route == "safe_default"
    assert record.fallback_reason == "tie_break_unresolved"
