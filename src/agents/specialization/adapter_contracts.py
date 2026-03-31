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

"""Data contracts for specialization adapter runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SpecializationDescriptor:
    """Validated specialization descriptor loaded from manifest.

    Args:
        specialization_id: Stable specialization identifier.
        adapter_contract_version: Contract version string.
        core_contract: Core target name.
        capability_set: Immutable capability tuple.
        policy_profile: Policy profile identifier.
        telemetry_profile: Telemetry profile identifier.

    """

    specialization_id: str
    adapter_contract_version: str
    core_contract: str
    capability_set: tuple[str, ...]
    policy_profile: str
    telemetry_profile: str


@dataclass(frozen=True)
class ShellExecutionRequest:
    """Canonical shell execution request built by adapter.

    Args:
        request_id: Stable request id.
        specialization_id: Specialization identifier.
        capability_action: Requested capability action.
        core_target: Core target name.
        policy_profile: Policy profile identifier.
        correlation_id: Correlation id for telemetry lineage.

    """

    request_id: str
    specialization_id: str
    capability_action: str
    core_target: str
    policy_profile: str
    correlation_id: str


@dataclass(frozen=True)
class PolicyDecision:
    """Policy authorization outcome and evidence fields.

    Args:
        authorized: Authorization flag.
        matched_rules: Rules that matched during evaluation.
        deny_reason: Denial reason when unauthorized.
        policy_version: Effective policy version.

    """

    authorized: bool
    matched_rules: tuple[str, ...]
    deny_reason: str | None
    policy_version: str


@dataclass(frozen=True)
class CoreInvocationPlan:
    """Resolved core invocation plan for shell requests.

    Args:
        core_target: Core target name.
        handler: Resolved callable handler.

    """

    core_target: str
    handler: Any


@dataclass(frozen=True)
class FallbackDecision:
    """Deterministic fail-closed fallback decision.

    Args:
        outcome: Fallback outcome value.
        route: Route selected by fallback policy.
        reason: Stable fallback reason taxonomy value.
        fail_closed: Whether fallback is fail-closed.

    """

    outcome: str
    route: str
    reason: str
    fail_closed: bool


@dataclass(frozen=True)
class SpecializationDecisionRecord:
    """Telemetry provenance record emitted after specialization decision.

    Args:
        request_id: Stable request id.
        specialization_id: Specialization identifier.
        adapter_contract_version: Adapter contract version.
        final_outcome: Final decision outcome.
        fallback_used: Whether fallback path was used.
        policy_version: Effective policy version.
        correlation_id: Correlation identifier.
        metadata: Optional redaction-managed metadata.

    """

    request_id: str
    specialization_id: str
    adapter_contract_version: str
    final_outcome: str
    fallback_used: bool
    policy_version: str
    correlation_id: str
    metadata: dict[str, Any]


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when contract dataclasses are importable.

    """
    return True


__all__ = [
    "CoreInvocationPlan",
    "FallbackDecision",
    "PolicyDecision",
    "ShellExecutionRequest",
    "SpecializationDecisionRecord",
    "SpecializationDescriptor",
    "validate",
]
