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

"""Deterministic semantic classifier for ambiguous routing."""

from __future__ import annotations

from src.core.routing.routing_models import ClassifierResult, PromptRoutingRequest, RouteCandidate


class PromptSemanticClassifier:
    """Classify request intent into route candidates with deterministic confidence."""

    def classify(self, request: PromptRoutingRequest) -> ClassifierResult:
        """Classify one routing request.

        Args:
            request: Normalized routing request.

        Returns:
            Deterministic classifier result.

        """
        hint = (request.intent_hint or "").strip().lower()

        if "analyze" in hint or "code" in hint:
            return ClassifierResult(
                candidate_routes=[RouteCandidate(route="core", score=0.82), RouteCandidate(route="legacy", score=0.18)],
                confidence=0.82,
                feature_tags=["intent:analysis"],
            )

        if "chat" in hint or "help" in hint:
            return ClassifierResult(
                candidate_routes=[RouteCandidate(route="legacy", score=0.78), RouteCandidate(route="core", score=0.22)],
                confidence=0.78,
                feature_tags=["intent:assistant"],
            )

        return ClassifierResult(
            candidate_routes=[RouteCandidate(route="core", score=0.50), RouteCandidate(route="legacy", score=0.50)],
            confidence=0.50,
            feature_tags=["intent:ambiguous"],
        )


def validate() -> bool:
    """Validate classifier deterministic output envelope.

    Returns:
        True when classifier returns bounded confidence and candidates.

    """
    result = PromptSemanticClassifier().classify(
        PromptRoutingRequest(
            request_id="validate-classifier",
            tenant_id="tenant",
            intent_hint="analyze code",
            risk_class="low",
            tool_requirement=None,
            latency_budget_ms=50,
            cost_budget_class="standard",
            context_summary="validate",
        )
    )
    return bool(result.candidate_routes) and 0.0 <= result.confidence <= 1.0
