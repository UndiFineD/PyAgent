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

"""Fail-closed behavior tests for timeout and unresolved tie-break paths."""

from __future__ import annotations

import pytest

from src.core.routing.prompt_routing_facade import PromptRoutingFacade
from src.core.routing.routing_models import ClassifierResult, PromptRoutingRequest, RouteCandidate


class _LowConfidenceClassifier:
    """Low-confidence classifier forcing tie-break path."""

    def classify(self, request: PromptRoutingRequest) -> ClassifierResult:
        """Return ambiguous low-confidence candidates.

        Args:
            request: Routing request.

        Returns:
            Ambiguous classifier result.

        """
        _ = request
        return ClassifierResult(
            candidate_routes=[RouteCandidate(route="legacy", score=0.5), RouteCandidate(route="core", score=0.5)],
            confidence=0.40,
            feature_tags=["ambiguous"],
        )


def _request() -> PromptRoutingRequest:
    """Build canonical request for fail-closed fallback tests.

    Returns:
        PromptRoutingRequest fixture instance.

    """
    return PromptRoutingRequest(
        request_id="req-fallback-1",
        tenant_id="tenant-1",
        intent_hint="unknown",
        risk_class="low",
        tool_requirement=None,
        latency_budget_ms=30,
        cost_budget_class="normal",
        context_summary="fallback context",
    )


@pytest.mark.asyncio
async def test_fail_closed_on_tie_break_timeout() -> None:
    """Tie-break timeout should fail closed with explicit timeout reason."""
    facade = PromptRoutingFacade(
        classifier=_LowConfidenceClassifier(),
        policy={"policy_version": "spr-v1", "confidence_threshold": 0.75, "tie_break_timeout_ms": 0},
    )

    record = await facade.route(_request())
    assert record.decision_stage == "fallback"
    assert record.final_route == "safe_default"
    assert record.fallback_reason == "tie_break_timeout"
