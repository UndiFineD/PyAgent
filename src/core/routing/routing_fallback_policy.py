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

"""Fail-closed fallback policy for routing failures."""

from __future__ import annotations

from src.core.routing.fallback_reason_taxonomy import normalize_fallback_reason
from src.core.routing.routing_models import PromptRoutingRequest, RouteDecisionRecord


class RoutingFallbackPolicy:
    """Apply deterministic fail-closed decisions for routing faults."""

    def __init__(self, safe_route: str = "safe_default") -> None:
        """Initialize fallback policy.

        Args:
            safe_route: Route used whenever fail-closed fallback is required.

        """
        self._safe_route = safe_route

    def apply(
        self,
        *,
        reason: str | None,
        request: PromptRoutingRequest,
        policy_version: str,
        correlation_id: str,
    ) -> RouteDecisionRecord:
        """Create fail-closed decision record.

        Args:
            reason: Reason taxonomy value.
            request: Request being routed.
            policy_version: Policy version string.
            correlation_id: Correlation identifier for telemetry.

        Returns:
            RouteDecisionRecord representing safe fallback.

        """
        return RouteDecisionRecord(
            request_id=request.request_id,
            final_route=self._safe_route,
            decision_stage="fallback",
            guardrail_hit=False,
            classifier_confidence=0.0,
            tie_break_used=False,
            fallback_reason=normalize_fallback_reason(reason),
            policy_version=policy_version,
            correlation_id=correlation_id,
        )
