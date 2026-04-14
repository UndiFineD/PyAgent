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

"""Parity contract tests between manifest intent and adapter output."""

from __future__ import annotations

from src.agents.specialization.adapter_contracts import SpecializationDescriptor
from src.agents.specialization.specialized_agent_adapter import SpecializedAgentAdapter


def test_manifest_intent_matches_built_request_fields() -> None:
    """Manifest intent should remain parity-consistent in request output."""
    descriptor = SpecializationDescriptor(
        specialization_id="finance",
        adapter_contract_version="1.0.0",
        core_contract="summarize",
        capability_set=("summarize",),
        policy_profile="strict",
        telemetry_profile="redacted",
    )

    request = SpecializedAgentAdapter().build_request(
        descriptor,
        runtime_context={
            "capability_action": "summarize",
            "request_id": "req-fin-1",
            "correlation_id": "corr-fin-1",
        },
    )

    assert request.specialization_id == descriptor.specialization_id
    assert request.core_target == descriptor.core_contract
    assert request.policy_profile == descriptor.policy_profile
    assert request.capability_action == "summarize"
