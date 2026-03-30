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

"""Routing telemetry emission with provenance and redaction."""

from __future__ import annotations

from src.core.routing.routing_models import PromptRoutingRequest, RouteDecisionRecord


class RoutingTelemetryEmitter:
    """Emit redacted telemetry envelopes for routing decisions."""

    def emit(self, *, request: PromptRoutingRequest, record: RouteDecisionRecord) -> dict[str, object]:
        """Build telemetry payload for one decision.

        Args:
            request: Original routing request.
            record: Route decision record.

        Returns:
            Redacted telemetry payload suitable for assertions and audit logs.

        """
        redacted_summary = request.context_summary.replace("secret", "[REDACTED]")
        return {
            "request_id": record.request_id,
            "final_route": record.final_route,
            "decision_stage": record.decision_stage,
            "guardrail_hit": record.guardrail_hit,
            "classifier_confidence": record.classifier_confidence,
            "tie_break_used": record.tie_break_used,
            "fallback_reason": record.fallback_reason,
            "policy_version": record.policy_version,
            "correlation_id": record.correlation_id,
            "tenant_id": request.tenant_id,
            "context_summary": redacted_summary,
        }
