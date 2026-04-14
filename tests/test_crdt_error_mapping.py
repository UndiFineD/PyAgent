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

"""Error taxonomy mapping tests for CRDT FFI bridge."""

from __future__ import annotations

from typing import Any

import pytest

from src.core import crdt_bridge


def test_maps_validation_errors_to_validation_category(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify FFI validation faults map to validation taxonomy."""

    def _raise_validation(_: dict[str, Any]) -> dict[str, Any]:
        raise crdt_bridge.CRDTBridgeError("bad", "crdt_validation_error", "validation", "req-err-1")

    monkeypatch.setenv("CRDT_FFI_ENABLED", "1")
    monkeypatch.setattr(crdt_bridge, "_ffi_available", lambda: True)
    monkeypatch.setattr(crdt_bridge, "_ffi_merge", _raise_validation)

    payload = crdt_bridge.make_request({"a": 1}, {"b": 2}, request_id="req-err-1")
    with pytest.raises(crdt_bridge.CRDTBridgeError) as exc:
        crdt_bridge.merge(payload)

    assert exc.value.category == "validation"


def test_maps_merge_runtime_errors_to_merge_category(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify runtime merge faults map to merge taxonomy."""

    def _raise_merge(_: dict[str, Any]) -> dict[str, Any]:
        raise crdt_bridge.CRDTBridgeError("merge failed", "crdt_merge_error", "merge", "req-err-2")

    monkeypatch.setenv("CRDT_FFI_ENABLED", "1")
    monkeypatch.setattr(crdt_bridge, "_ffi_available", lambda: True)
    monkeypatch.setattr(crdt_bridge, "_ffi_merge", _raise_merge)

    payload = crdt_bridge.make_request({"a": 1}, {"b": 2}, request_id="req-err-2")
    with pytest.raises(crdt_bridge.CRDTBridgeError) as exc:
        crdt_bridge.merge(payload)

    assert exc.value.category == "merge"
