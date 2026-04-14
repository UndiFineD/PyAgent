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

"""Determinism tests for CRDT merge behavior."""

from __future__ import annotations

from src.core import crdt_bridge


def test_deterministic_output_for_identical_inputs() -> None:
    """Verify repeated merge calls produce identical outputs."""
    payload = crdt_bridge.make_request(
        lhs_state={"alpha": {"x": 1}, "beta": 2},
        rhs_state={"alpha": {"y": 3}, "gamma": 4},
        request_id="req-determinism",
    )

    first = crdt_bridge.merge(payload)
    second = crdt_bridge.merge(payload)

    assert first["merged_state"] == second["merged_state"]
    assert first["conflict_summary"] == second["conflict_summary"]
