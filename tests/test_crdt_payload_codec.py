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

"""Payload codec parity tests for CRDT request handling."""

from __future__ import annotations

from src.core import crdt_bridge


def test_round_trip_semantic_equivalence_for_nested_payload() -> None:
    """Ensure nested state merge preserves semantic intent after processing."""
    payload = crdt_bridge.make_request(
        lhs_state={"a": {"x": 1, "y": 2}, "k": 10},
        rhs_state={"a": {"y": 9, "z": 3}, "k": 11},
        request_id="req-codec",
    )

    response = crdt_bridge.merge(payload)

    assert response["merged_state"] == {"a": {"x": 1, "y": 9, "z": 3}, "k": 11}
