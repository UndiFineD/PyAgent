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

"""Redaction invariants for specialization telemetry bridge."""

from __future__ import annotations

from src.agents.specialization.adapter_contracts import SpecializationDecisionRecord
from src.agents.specialization.specialization_telemetry_bridge import SpecializationTelemetryBridge


def test_emit_redacts_secret_and_prompt_fields() -> None:
    """Telemetry emission should remove secret-bearing metadata keys."""
    captured: list[dict[str, object]] = []
    bridge = SpecializationTelemetryBridge(sink=captured.append)

    bridge.emit(
        SpecializationDecisionRecord(
            request_id="req-1",
            specialization_id="support",
            adapter_contract_version="1.0.0",
            final_outcome="authorized",
            fallback_used=False,
            policy_version="2026.03",
            correlation_id="corr-1",
            metadata={
                "safe_key": "safe",
                "api_token": "secret",
                "prompt_text": "should be removed",
            },
        )
    )

    payload = captured[0]
    metadata = payload["metadata"]

    assert payload["correlation_id"] == "corr-1"
    assert isinstance(metadata, dict)
    assert "safe_key" in metadata
    assert "api_token" not in metadata
    assert "prompt_text" not in metadata
