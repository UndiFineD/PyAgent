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

"""Telemetry schema and redaction tests for routing provenance."""

from __future__ import annotations

from src.core.routing.routing_models import PromptRoutingRequest, RouteDecisionRecord
from src.core.routing.routing_telemetry_emitter import RoutingTelemetryEmitter


def test_telemetry_includes_required_provenance_fields_and_redacts() -> None:
    """Telemetry payload must include provenance and redact sensitive text."""
    emitter = RoutingTelemetryEmitter()
    request = PromptRoutingRequest(
        request_id="req-telemetry-1",
        tenant_id="tenant-1",
        intent_hint="help",
        risk_class="low",
        tool_requirement=None,
        latency_budget_ms=30,
        cost_budget_class="normal",
        context_summary="contains secret token",
    )
    record = RouteDecisionRecord(
        request_id="req-telemetry-1",
        final_route="legacy",
        decision_stage="classifier",
        guardrail_hit=False,
        classifier_confidence=0.78,
        tie_break_used=False,
        fallback_reason=None,
        policy_version="spr-v1",
        correlation_id="corr-123",
    )

    payload = emitter.emit(request=request, record=record)
    assert payload["request_id"] == "req-telemetry-1"
    assert payload["correlation_id"] == "corr-123"
    assert payload["policy_version"] == "spr-v1"
    assert "secret" not in str(payload["context_summary"]).lower()
    assert "[REDACTED]" in str(payload["context_summary"])
