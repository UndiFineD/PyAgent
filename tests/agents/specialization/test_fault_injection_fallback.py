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

"""Fault-injection tests for deterministic fail-closed fallback policy."""

from __future__ import annotations

from src.agents.specialization.adapter_fallback_policy import AdapterFallbackPolicy


def test_timeout_fault_maps_to_fail_closed_decision() -> None:
    """Timeout faults should map to deterministic fail-closed outcome."""
    decision = AdapterFallbackPolicy().apply("timeout", runtime_context={"request_id": "req-1"})

    assert decision.fail_closed is True
    assert decision.route == "fail_closed"
    assert decision.reason == "timeout_fault"


def test_policy_fault_maps_to_fail_closed_decision() -> None:
    """Policy denials should map to deterministic policy fault outcome."""
    decision = AdapterFallbackPolicy().apply(
        "capability_not_allowlisted",
        runtime_context={"request_id": "req-1"},
    )

    assert decision.fail_closed is True
    assert decision.route == "fail_closed"
    assert decision.reason == "policy_fault"


def test_schema_fault_maps_to_fail_closed_decision() -> None:
    """Schema faults should map to deterministic schema fault outcome."""
    decision = AdapterFallbackPolicy().apply(
        "descriptor_schema_missing_field",
        runtime_context={"request_id": "req-1"},
    )

    assert decision.fail_closed is True
    assert decision.route == "fail_closed"
    assert decision.reason == "schema_fault"
