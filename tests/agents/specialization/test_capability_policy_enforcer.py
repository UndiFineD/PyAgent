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

"""Authorization matrix tests for deny-by-default capability policy."""

from __future__ import annotations

from src.agents.specialization.adapter_contracts import ShellExecutionRequest
from src.agents.specialization.capability_policy_enforcer import CapabilityPolicyEnforcer
from src.agents.specialization.policy_matrix import PolicyMatrix


def _request(action: str) -> ShellExecutionRequest:
    """Build a canonical shell request fixture.

    Args:
        action: Capability action value.

    Returns:
        Shell execution request fixture.

    """
    return ShellExecutionRequest(
        request_id="req-1",
        specialization_id="support",
        capability_action=action,
        core_target="summarize",
        policy_profile="default",
        correlation_id="corr-1",
    )


def test_authorize_allows_allowlisted_capability() -> None:
    """Allowlisted capabilities should return authorized policy decisions."""
    matrix = PolicyMatrix(rules={"default": ("summarize",)})
    decision = CapabilityPolicyEnforcer(matrix, policy_version="2026.03").authorize(
        _request("summarize"),
        actor_context={"role": "agent"},
    )

    assert decision.authorized is True
    assert decision.deny_reason is None
    assert decision.policy_version == "2026.03"
    assert decision.matched_rules == ("allow:default:summarize",)


def test_authorize_denies_non_allowlisted_capability_by_default() -> None:
    """Non-allowlisted capabilities should be denied with evidence fields."""
    matrix = PolicyMatrix(rules={"default": ("summarize",)})
    decision = CapabilityPolicyEnforcer(matrix, policy_version="2026.03").authorize(
        _request("delete"),
        actor_context={"role": "agent"},
    )

    assert decision.authorized is False
    assert decision.deny_reason == "capability_not_allowlisted"
    assert decision.policy_version == "2026.03"
    assert decision.matched_rules == tuple()
