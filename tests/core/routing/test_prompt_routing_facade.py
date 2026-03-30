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

"""Facade behavior tests for threshold and fallback contracts."""

from __future__ import annotations

import pytest

from src.core.routing.prompt_routing_facade import PromptRoutingFacade
from src.core.routing.routing_models import ClassifierResult, PromptRoutingRequest, RouteCandidate


class _LowConfidenceClassifier:
    """Classifier test double returning low-confidence ambiguous routes."""

    def classify(self, request: PromptRoutingRequest) -> ClassifierResult:
        """Return a deterministic low-confidence result.

        Args:
            request: Routing request.

        Returns:
            Low-confidence classifier result.

        """
        _ = request
        return ClassifierResult(
            candidate_routes=[RouteCandidate(route="legacy", score=0.5), RouteCandidate(route="core", score=0.5)],
            confidence=0.50,
            feature_tags=["ambiguous"],
        )


class _InvalidSchemaClassifier:
    """Classifier test double returning schema-invalid payload."""

    def classify(self, request: PromptRoutingRequest) -> ClassifierResult:
        """Return invalid schema classifier result.

        Args:
            request: Routing request.

        Returns:
            Schema-invalid result.

        """
        _ = request
        return ClassifierResult(candidate_routes=[], confidence=0.30, feature_tags=[])


class _ExplodingClassifier:
    """Classifier test double that simulates provider failure."""

    def classify(self, request: PromptRoutingRequest) -> ClassifierResult:
        """Raise provider-like exception.

        Args:
            request: Routing request.

        Raises:
            RuntimeError: Always raised for test coverage.

        """
        _ = request
        raise RuntimeError("provider unavailable")


def _request(request_id: str = "req-facade") -> PromptRoutingRequest:
    """Build canonical routing request for facade tests.

    Args:
        request_id: Request identifier.

    Returns:
        PromptRoutingRequest fixture instance.

    """
    return PromptRoutingRequest(
        request_id=request_id,
        tenant_id="tenant-1",
        intent_hint="analyze",
        risk_class="low",
        tool_requirement=None,
        latency_budget_ms=30,
        cost_budget_class="normal",
        context_summary="no secret here",
    )


@pytest.mark.asyncio
async def test_confidence_threshold_uses_classifier_when_above_threshold() -> None:
    """Classifier winner should be used when confidence meets threshold."""
    facade = PromptRoutingFacade(policy={"policy_version": "spr-v1", "confidence_threshold": 0.75})

    record = await facade.route(_request("req-threshold-high"))
    assert record.decision_stage == "classifier"
    assert record.tie_break_used is False
    assert record.final_route == "core"


@pytest.mark.asyncio
async def test_confidence_threshold_invokes_tie_break_when_below_threshold() -> None:
    """Tie-break should be used when confidence is below threshold."""
    facade = PromptRoutingFacade(
        classifier=_LowConfidenceClassifier(),
        policy={"policy_version": "spr-v1", "confidence_threshold": 0.75},
    )

    record = await facade.route(_request("req-threshold-low"))
    assert record.decision_stage == "tie_break"
    assert record.tie_break_used is True


@pytest.mark.asyncio
async def test_fail_closed_on_schema_violation() -> None:
    """Schema-invalid classifier result must trigger fail-closed fallback."""
    facade = PromptRoutingFacade(
        classifier=_InvalidSchemaClassifier(),
        policy={"policy_version": "spr-v1", "confidence_threshold": 0.75},
    )

    record = await facade.route(_request("req-schema-fail"))
    assert record.decision_stage == "fallback"
    assert record.final_route == "safe_default"
    assert record.fallback_reason == "schema_validation_failed"


@pytest.mark.asyncio
async def test_fail_closed_on_classifier_provider_error() -> None:
    """Classifier exceptions must trigger fail-closed fallback."""
    facade = PromptRoutingFacade(
        classifier=_ExplodingClassifier(),
        policy={"policy_version": "spr-v1", "confidence_threshold": 0.75},
    )

    record = await facade.route(_request("req-provider-fail"))
    assert record.decision_stage == "fallback"
    assert record.final_route == "safe_default"
    assert record.fallback_reason == "classifier_provider_error"
