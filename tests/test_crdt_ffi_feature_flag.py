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

"""Feature-flag routing behavior tests for CRDT FFI bridge."""

from __future__ import annotations

from src.core import crdt_bridge


def test_feature_flag_on_selects_ffi(monkeypatch) -> None:
    """Verify enabled feature flag selects ffi path when available."""
    monkeypatch.setenv("CRDT_FFI_ENABLED", "1")
    monkeypatch.setattr(crdt_bridge, "_ffi_available", lambda: True)
    monkeypatch.setattr(crdt_bridge, "_ffi_merge", lambda payload: {"ffi": payload["lhs_state"]})

    payload = crdt_bridge.make_request({"a": 1}, {"b": 2}, request_id="req-flag-on")
    response = crdt_bridge.merge(payload)

    assert response["path"] == "ffi"


def test_feature_flag_off_selects_fallback(monkeypatch) -> None:
    """Verify disabled feature flag selects fallback path."""
    monkeypatch.setenv("CRDT_FFI_ENABLED", "0")

    payload = crdt_bridge.make_request({"a": 1}, {"b": 2}, request_id="req-flag-off")
    response = crdt_bridge.merge(payload)

    assert response["path"] == "fallback"
