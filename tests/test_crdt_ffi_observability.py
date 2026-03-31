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

"""Observability schema and redaction checks for CRDT bridge."""

from __future__ import annotations

from src.core import crdt_bridge


def test_observability_event_contains_required_fields() -> None:
    """Verify required telemetry fields are present for merge events."""
    payload = crdt_bridge.make_request({"left": 1}, {"right": 2}, request_id="req-obs")
    crdt_bridge.merge(payload)

    event = crdt_bridge.get_last_observability_event()
    assert event is not None
    assert set(event.keys()) == {"request_id", "path", "duration_ms", "outcome", "parity_tag"}
    assert event["request_id"] == "req-obs"


def test_observability_event_redacts_payload_bodies() -> None:
    """Verify telemetry output does not leak raw state payloads."""
    payload = crdt_bridge.make_request({"secret": "left"}, {"secret": "right"}, request_id="req-obs-redact")
    crdt_bridge.merge(payload)

    event = crdt_bridge.get_last_observability_event()
    assert event is not None
    assert "lhs_state" not in event
    assert "rhs_state" not in event
    assert "payload" not in event
