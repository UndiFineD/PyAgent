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

"""Schema and continuity tests for specialization telemetry payloads."""

from __future__ import annotations

from src.agents.specialization.adapter_contracts import SpecializationDecisionRecord
from src.agents.specialization.specialization_telemetry_bridge import SpecializationTelemetryBridge


def test_emit_includes_required_provenance_fields() -> None:
    """Telemetry bridge should include required provenance fields."""
    captured: list[dict[str, object]] = []
    bridge = SpecializationTelemetryBridge(sink=captured.append)

    bridge.emit(
        SpecializationDecisionRecord(
            request_id="req-2",
            specialization_id="finance",
            adapter_contract_version="1.0.0",
            final_outcome="denied",
            fallback_used=True,
            policy_version="2026.03",
            correlation_id="corr-2",
            metadata={"safe_key": "safe"},
        )
    )

    payload = captured[0]
    required = {
        "request_id",
        "specialization_id",
        "adapter_contract_version",
        "final_outcome",
        "fallback_used",
        "policy_version",
        "correlation_id",
        "metadata",
    }
    assert required.issubset(payload.keys())
    assert payload["correlation_id"] == "corr-2"
    assert payload["specialization_id"] == "finance"
