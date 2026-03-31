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

"""Deny-by-default policy matrix utilities."""

from __future__ import annotations


class PolicyMatrix:
    """Evaluate capability authorization against allowlist rules.

    Args:
        rules: Mapping of policy profile to allowed capabilities.

    """

    def __init__(self, rules: dict[str, tuple[str, ...]]) -> None:
        """Initialize policy rules.

        Args:
            rules: Profile-to-capability allowlist mapping.

        """
        self._rules = rules

    def allowed(self, policy_profile: str, capability_action: str) -> bool:
        """Determine whether capability action is explicitly allowlisted.

        Args:
            policy_profile: Policy profile identifier.
            capability_action: Requested capability action.

        Returns:
            True when explicitly allowlisted, else False.

        """
        allowed_capabilities = self._rules.get(policy_profile, tuple())
        return capability_action in allowed_capabilities

    def matched_rules(self, policy_profile: str, capability_action: str) -> tuple[str, ...]:
        """Return matched policy evidence entries.

        Args:
            policy_profile: Policy profile identifier.
            capability_action: Requested capability action.

        Returns:
            Tuple containing the matched allow rule identifier or empty tuple.

        """
        if self.allowed(policy_profile, capability_action):
            return (f"allow:{policy_profile}:{capability_action}",)
        return tuple()


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when policy matrix class is importable.

    """
    return True


__all__ = ["PolicyMatrix", "validate"]
