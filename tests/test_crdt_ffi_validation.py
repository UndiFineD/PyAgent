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

"""Validation tests for CRDT FFI payload shape and schema gates."""

from __future__ import annotations

import pytest

from src.core import crdt_bridge


def test_shape_validation_rejects_non_object_states() -> None:
    """Verify invalid payload shape is mapped to validation errors."""
    payload = {
        "request_id": "req-shape",
        "lhs_state": [],
        "rhs_state": {},
        "merge_strategy": "last_write_wins",
        "schema_version": 1,
    }
    with pytest.raises(crdt_bridge.CRDTBridgeError) as exc:
        crdt_bridge.merge(payload)

    assert exc.value.category == "validation"
    assert exc.value.error_code == "crdt_validation_shape"


def test_shape_validation_rejects_missing_fields() -> None:
    """Verify missing required fields are mapped to validation errors."""
    payload = {"request_id": "req-missing", "lhs_state": {}}
    with pytest.raises(crdt_bridge.CRDTBridgeError) as exc:
        crdt_bridge.merge(payload)

    assert exc.value.category == "validation"
    assert exc.value.error_code == "crdt_validation_missing_fields"
