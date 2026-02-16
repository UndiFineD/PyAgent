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

import pytest
from infrastructure.storage.kv_transfer.lru_offload_manager import LRUEntry, LRUOffloadManager, WeightedLRUManager, TieredLRUManager, PrefetchingLRUManager, AsyncLRUManager, LRUManagerFactory


def test_lruentry_basic():
    assert LRUEntry is not None


def test_lruoffloadmanager_basic():
    assert LRUOffloadManager is not None


def test_weightedlrumanager_basic():
    assert WeightedLRUManager is not None


def test_tieredlrumanager_basic():
    assert TieredLRUManager is not None


def test_prefetchinglrumanager_basic():
    assert PrefetchingLRUManager is not None


def test_asynclrumanager_basic():
    assert AsyncLRUManager is not None


def test_lrumanagerfactory_basic():
    assert LRUManagerFactory is not None
