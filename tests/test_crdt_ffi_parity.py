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

"""Parity checks between fallback and ffi merge paths."""

from __future__ import annotations

from src.core import crdt_bridge


def test_parity_between_ffi_and_fallback_paths(monkeypatch) -> None:
    """Verify equivalent outputs between fallback and ffi paths for same corpus item."""
    payload = crdt_bridge.make_request(
        lhs_state={"v": {"a": 1}, "p": 9},
        rhs_state={"v": {"b": 2}, "p": 10},
        request_id="req-parity",
    )

    monkeypatch.setenv("CRDT_FFI_ENABLED", "0")
    fallback_response = crdt_bridge.merge(payload)

    monkeypatch.setenv("CRDT_FFI_ENABLED", "1")
    monkeypatch.setattr(crdt_bridge, "_ffi_available", lambda: True)
    monkeypatch.setattr(
        crdt_bridge,
        "_ffi_merge",
        lambda req: crdt_bridge._deep_merge(req["lhs_state"], req["rhs_state"]),
    )
    ffi_response = crdt_bridge.merge(payload)

    assert fallback_response["merged_state"] == ffi_response["merged_state"]
