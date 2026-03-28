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

"""Fail-closed secret guardrail policy for PR and push workflows."""

from __future__ import annotations

from typing import Any

from .models.guardrail_decision import GuardrailDecision

_BLOCKING_SEVERITIES = {"HIGH", "CRITICAL"}


class SecretGuardrailPolicy:
    """Evaluate secret findings and produce allow/block decisions."""

    def validate_pr(self, findings: list[dict[str, Any]]) -> GuardrailDecision:
        """Validate pull-request findings against guardrail thresholds.

        Args:
            findings: Scanner finding dictionaries.

        Returns:
            Policy decision for pull request gate.

        """
        return self._evaluate(findings=findings, gate_name="PR")

    def validate_push(self, findings: list[dict[str, Any]]) -> GuardrailDecision:
        """Validate push findings against guardrail thresholds.

        Args:
            findings: Scanner finding dictionaries.

        Returns:
            Policy decision for push gate.

        """
        return self._evaluate(findings=findings, gate_name="PUSH")

    def _evaluate(self, findings: list[dict[str, Any]], gate_name: str) -> GuardrailDecision:
        """Evaluate findings and derive fail-closed policy status.

        Args:
            findings: Scanner finding dictionaries.
            gate_name: Label for decision message context.

        Returns:
            Guardrail decision object.

        """
        blocking_reasons: list[str] = [
            (
                f"{gate_name} blocked due to {str(item.get('severity', '')).upper()} finding: "
                f"{str(item.get('fingerprint', 'unknown'))}"
            )
            for item in findings
            if str(item.get("severity", "")).upper() in _BLOCKING_SEVERITIES
        ]

        if blocking_reasons:
            return GuardrailDecision(status="BLOCK", blocking_reasons=blocking_reasons)
        return GuardrailDecision(status="ALLOW", blocking_reasons=[])
