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

"""Contract tests for CRDT bridge request and response envelopes."""

from __future__ import annotations

import pytest

from src.core import crdt_bridge


@pytest.mark.parametrize("flag", ["0", "1"])
def test_schema_envelope_contains_required_fields(monkeypatch: pytest.MonkeyPatch, flag: str) -> None:
    """Ensure bridge response envelope has required schema fields.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
        flag: Feature-flag value under test.

    """
    monkeypatch.setenv("CRDT_FFI_ENABLED", flag)
    if flag == "1":
        monkeypatch.setattr(crdt_bridge, "_ffi_available", lambda: True)
        monkeypatch.setattr(crdt_bridge, "_ffi_merge", lambda payload: {"ok": True})

    payload = crdt_bridge.make_request({"a": 1}, {"b": 2}, request_id="req-contract")
    response = crdt_bridge.merge(payload)

    assert set(response.keys()) == {
        "request_id",
        "merged_state",
        "conflict_summary",
        "engine_version",
        "path",
    }
    assert response["request_id"] == "req-contract"
    assert response["path"] in {"ffi", "fallback"}
