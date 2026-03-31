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

"""Tests for the core CRDT bridge.

The bridge is a thin Python wrapper over the Rust crdt merge binary.
"""

from __future__ import annotations

from typing import Any

import pytest

from src.core import crdt_bridge


def test_crdt_bridge_merge_deterministic():
    """Test that merging two documents produces the expected result."""
    merged = crdt_bridge.merge({"a": 1}, {"b": 2})
    assert merged["a"] == 1
    assert merged["b"] == 2


def test_bridge_ffi_envelope_path_when_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that enabled FFI path emits an envelope with path=ffi."""

    def _fake_ffi(payload: dict[str, Any]) -> dict[str, Any]:
        return {"v": payload["lhs_state"]["v"] + payload["rhs_state"]["v"]}

    monkeypatch.setenv("CRDT_FFI_ENABLED", "1")
    monkeypatch.setattr(crdt_bridge, "_ffi_available", lambda: True)
    monkeypatch.setattr(crdt_bridge, "_ffi_merge", _fake_ffi)

    payload = crdt_bridge.make_request({"v": 1}, {"v": 2}, request_id="req-ffi")
    response = crdt_bridge.merge(payload)

    assert response["path"] == "ffi"
    assert response["request_id"] == "req-ffi"
    assert response["merged_state"] == {"v": 3}


def test_bridge_ffi_envelope_path_when_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that disabled FFI path emits an envelope with path=fallback."""
    monkeypatch.setenv("CRDT_FFI_ENABLED", "0")

    payload = crdt_bridge.make_request({"x": 1}, {"y": 2}, request_id="req-fallback")
    response = crdt_bridge.merge(payload)

    assert response["path"] == "fallback"
    assert response["request_id"] == "req-fallback"
    assert response["merged_state"] == {"x": 1, "y": 2}
