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
from infrastructure.services.metrics.caching_metrics import CacheType, EvictionReason, CacheEvent, EvictionEvent, CacheStats, SlidingWindowStats, SlidingWindowMetrics, CachingMetrics, PrefixCacheStats, MultiLevelCacheMetrics, observe_with_rust


def test_cachetype_basic():
    assert CacheType is not None


def test_evictionreason_basic():
    assert EvictionReason is not None


def test_cacheevent_basic():
    assert CacheEvent is not None


def test_evictionevent_basic():
    assert EvictionEvent is not None


def test_cachestats_basic():
    assert CacheStats is not None


def test_slidingwindowstats_basic():
    assert SlidingWindowStats is not None


def test_slidingwindowmetrics_basic():
    assert SlidingWindowMetrics is not None


def test_cachingmetrics_basic():
    assert CachingMetrics is not None


def test_prefixcachestats_basic():
    assert PrefixCacheStats is not None


def test_multilevelcachemetrics_basic():
    assert MultiLevelCacheMetrics is not None


def test_observe_with_rust_basic():
    assert callable(observe_with_rust)
