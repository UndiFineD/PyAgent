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

"""Public exports for specialization runtime contracts."""

from src.agents.specialization.adapter_contracts import (
    CoreInvocationPlan,
    FallbackDecision,
    PolicyDecision,
    ShellExecutionRequest,
    SpecializationDecisionRecord,
    SpecializationDescriptor,
)
from src.agents.specialization.adapter_fallback_policy import AdapterFallbackPolicy
from src.agents.specialization.capability_policy_enforcer import CapabilityPolicyEnforcer
from src.agents.specialization.manifest_loader import ManifestLoader
from src.agents.specialization.specialization_registry import SpecializationRegistry
from src.agents.specialization.specialization_telemetry_bridge import SpecializationTelemetryBridge
from src.agents.specialization.specialized_agent_adapter import SpecializedAgentAdapter
from src.agents.specialization.specialized_core_binding import SpecializedCoreBinding

__all__ = [
    "AdapterFallbackPolicy",
    "CapabilityPolicyEnforcer",
    "CoreInvocationPlan",
    "FallbackDecision",
    "ManifestLoader",
    "PolicyDecision",
    "ShellExecutionRequest",
    "SpecializationDecisionRecord",
    "SpecializationDescriptor",
    "SpecializationRegistry",
    "SpecializationTelemetryBridge",
    "SpecializedAgentAdapter",
    "SpecializedCoreBinding",
]
