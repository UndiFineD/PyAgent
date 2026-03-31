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

"""Redacted telemetry bridge for specialization provenance."""

from __future__ import annotations

from typing import Any, Callable

from src.agents.specialization.adapter_contracts import SpecializationDecisionRecord


class SpecializationTelemetryBridge:
    """Emit redacted specialization provenance envelopes.

    Args:
        sink: Callable sink receiving telemetry payload dictionaries.

    """

    def __init__(self, sink: Callable[[dict[str, Any]], None]) -> None:
        """Initialize telemetry sink.

        Args:
            sink: Callable sink for emitted telemetry payloads.

        """
        self._sink = sink

    def emit(self, decision_record: SpecializationDecisionRecord) -> None:
        """Emit redacted telemetry payload for a decision record.

        Args:
            decision_record: Specialization decision provenance record.

        """
        payload = {
            "request_id": decision_record.request_id,
            "specialization_id": decision_record.specialization_id,
            "adapter_contract_version": decision_record.adapter_contract_version,
            "final_outcome": decision_record.final_outcome,
            "fallback_used": decision_record.fallback_used,
            "policy_version": decision_record.policy_version,
            "correlation_id": decision_record.correlation_id,
            "metadata": self._redact(decision_record.metadata),
        }
        self._sink(payload)

    def _redact(self, metadata: dict[str, Any]) -> dict[str, Any]:
        """Redact secret-bearing metadata keys.

        Args:
            metadata: Raw metadata payload.

        Returns:
            Redacted metadata payload.

        """
        return dict(filter(lambda item: not self._is_blocked_key(item[0]), metadata.items()))

    def _is_blocked_key(self, key: str) -> bool:
        """Return whether a metadata key should be filtered from telemetry.

        Args:
            key: Metadata key name.

        Returns:
            True when key includes a secret-bearing marker.

        """
        lower = key.lower()
        return (
            "secret" in lower or "token" in lower or "password" in lower or "prompt" in lower or "tool_input" in lower
        )


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when telemetry bridge class is importable.

    """
    return True


__all__ = ["SpecializationTelemetryBridge", "validate"]
