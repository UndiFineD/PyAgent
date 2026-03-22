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
"""Tests for core.memory.MemoryStore (prj0000025)."""
from src.core.memory import MemoryStore, validate


def test_memory_store_set_and_get():
    m = MemoryStore()
    m.set("x", 42)
    assert m.get("x") == 42


def test_memory_store_default_for_missing():
    m = MemoryStore()
    assert m.get("missing") is None
    assert m.get("missing", "default") == "default"


def test_memory_store_overwrite():
    m = MemoryStore()
    m.set("k", "first")
    m.set("k", "second")
    assert m.get("k") == "second"


def test_memory_store_multiple_keys():
    m = MemoryStore()
    for i in range(10):
        m.set(f"key{i}", i)
    for i in range(10):
        assert m.get(f"key{i}") == i


def test_memory_store_stores_complex_values():
    m = MemoryStore()
    doc = {"agent": "coder", "score": 0.99, "tags": ["fast", "safe"]}
    m.set("doc", doc)
    assert m.get("doc") == doc


def test_memory_validate():
    validate()  # must not raise
