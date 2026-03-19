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

from src.core import crdt_bridge


def test_crdt_bridge_merge_deterministic():
    """Test that merging two documents produces the expected result."""
    merged = crdt_bridge.merge({"a": 1}, {"b": 2})
    assert merged["a"] == 1
    assert merged["b"] == 2
