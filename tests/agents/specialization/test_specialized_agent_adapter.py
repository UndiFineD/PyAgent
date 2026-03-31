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

"""Determinism contract tests for specialized agent adapter mapping."""

from __future__ import annotations

from src.agents.specialization.adapter_contracts import SpecializationDescriptor
from src.agents.specialization.specialized_agent_adapter import SpecializedAgentAdapter


def _descriptor() -> SpecializationDescriptor:
    """Build deterministic descriptor fixture.

    Returns:
        Specialization descriptor fixture.

    """
    return SpecializationDescriptor(
        specialization_id="support",
        adapter_contract_version="1.0.0",
        core_contract="summarize",
        capability_set=("classify", "summarize"),
        policy_profile="default",
        telemetry_profile="redacted",
    )


def test_build_request_is_deterministic_for_identical_inputs() -> None:
    """Adapter should produce equivalent requests for identical inputs."""
    adapter = SpecializedAgentAdapter()
    context = {
        "capability_action": "summarize",
        "correlation_id": "corr-1",
        "request_id": "req-1",
    }

    left = adapter.build_request(_descriptor(), context)
    right = adapter.build_request(_descriptor(), context)

    assert left == right


def test_build_request_replay_id_is_stable_without_explicit_request_id() -> None:
    """Fallback request id should be deterministic across replays."""
    adapter = SpecializedAgentAdapter()
    context = {"capability_action": "summarize", "correlation_id": "corr-1"}

    left = adapter.build_request(_descriptor(), context)
    right = adapter.build_request(_descriptor(), context)

    assert left.request_id == right.request_id
    assert left.request_id.startswith("req-")
