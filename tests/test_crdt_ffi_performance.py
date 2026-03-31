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

"""Performance-oriented guard tests for CRDT bridge paths."""

from __future__ import annotations

import tempfile

from src.core import crdt_bridge


def test_no_temp_file_dependency_for_payload_mode(monkeypatch) -> None:
    """Ensure payload mode does not require temporary file IO."""

    def _raise_if_called(*args, **kwargs):
        raise AssertionError("TemporaryDirectory should not be used in payload mode")

    monkeypatch.setattr(tempfile, "TemporaryDirectory", _raise_if_called)

    payload = crdt_bridge.make_request({"a": 1}, {"b": 2}, request_id="req-perf")
    response = crdt_bridge.merge(payload)

    assert response["merged_state"] == {"a": 1, "b": 2}


def test_merge_duration_is_recorded(monkeypatch) -> None:
    """Ensure duration metric is emitted for payload merge path."""
    monkeypatch.setenv("CRDT_FFI_ENABLED", "0")

    payload = crdt_bridge.make_request({"a": 1}, {"b": 2}, request_id="req-perf-duration")
    crdt_bridge.merge(payload)
    event = crdt_bridge.get_last_observability_event()

    assert event is not None
    assert event["duration_ms"] >= 0
