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

"""Deny-by-default capability authorization contract."""

from __future__ import annotations

from src.agents.specialization.adapter_contracts import PolicyDecision, ShellExecutionRequest
from src.agents.specialization.policy_matrix import PolicyMatrix


class CapabilityPolicyEnforcer:
    """Authorize specialization requests with explicit allowlist policy.

    Args:
        policy_matrix: Policy matrix evaluator.
        policy_version: Policy version emitted in evidence.

    """

    def __init__(self, policy_matrix: PolicyMatrix, policy_version: str) -> None:
        """Initialize enforcer dependencies.

        Args:
            policy_matrix: Policy matrix evaluator.
            policy_version: Policy version emitted in decisions.

        """
        self._policy_matrix = policy_matrix
        self._policy_version = policy_version

    def authorize(self, shell_request: ShellExecutionRequest, actor_context: dict[str, str]) -> PolicyDecision:
        """Authorize requests with deny-by-default semantics.

        Args:
            shell_request: Canonical shell execution request.
            actor_context: Actor identity context for future policy extensions.

        Returns:
            Policy decision with immutable evidence fields.

        """
        _ = actor_context
        matched = self._policy_matrix.matched_rules(
            policy_profile=shell_request.policy_profile,
            capability_action=shell_request.capability_action,
        )
        if matched:
            return PolicyDecision(
                authorized=True,
                matched_rules=matched,
                deny_reason=None,
                policy_version=self._policy_version,
            )

        return PolicyDecision(
            authorized=False,
            matched_rules=tuple(),
            deny_reason="capability_not_allowlisted",
            policy_version=self._policy_version,
        )


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when enforcer class is importable.

    """
    return True


__all__ = ["CapabilityPolicyEnforcer", "validate"]
