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

"""Deterministic fail-closed fallback policy for specialization runtime."""

from __future__ import annotations

from src.agents.specialization.adapter_contracts import FallbackDecision


class AdapterFallbackPolicy:
    """Apply deterministic fail-closed fallback routes by reason taxonomy."""

    _KNOWN_REASON_MAP = {
        "descriptor_schema_missing_field": "schema_fault",
        "descriptor_schema_invalid_string": "schema_fault",
        "descriptor_schema_invalid_capabilities": "schema_fault",
        "unsupported_contract_major": "version_fault",
        "invalid_contract_version": "version_fault",
        "capability_not_allowlisted": "policy_fault",
        "core_target_unresolved": "binding_fault",
        "timeout": "timeout_fault",
    }

    def apply(self, failure_reason: str, runtime_context: dict[str, str]) -> FallbackDecision:
        """Apply fail-closed fallback decision.

        Args:
            failure_reason: Typed failure reason code.
            runtime_context: Runtime context metadata.

        Returns:
            Deterministic fail-closed fallback decision.

        """
        _ = runtime_context
        mapped = self._KNOWN_REASON_MAP.get(failure_reason, "unknown_fault")
        return FallbackDecision(
            outcome="denied",
            route="fail_closed",
            reason=mapped,
            fail_closed=True,
        )


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when fallback policy is importable.

    """
    return True


__all__ = ["AdapterFallbackPolicy", "validate"]
