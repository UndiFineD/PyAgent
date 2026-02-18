#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import pytest
except ImportError:
    import pytest

try:
    from infrastructure.engine.loading.kv_offload.managers import LRUOffloadingManager, ARCOffloadingManager, TieredOffloadManager, compute_lru_eviction_rust, compute_arc_target_rust
except ImportError:
    from infrastructure.engine.loading.kv_offload.managers import LRUOffloadingManager, ARCOffloadingManager, TieredOffloadManager, compute_lru_eviction_rust, compute_arc_target_rust



def test_lruoffloadingmanager_basic():
    assert LRUOffloadingManager is not None


def test_arcoffloadingmanager_basic():
    assert ARCOffloadingManager is not None


def test_tieredoffloadmanager_basic():
    assert TieredOffloadManager is not None


def test_compute_lru_eviction_rust_basic():
    assert callable(compute_lru_eviction_rust)


def test_compute_arc_target_rust_basic():
    assert callable(compute_arc_target_rust)
