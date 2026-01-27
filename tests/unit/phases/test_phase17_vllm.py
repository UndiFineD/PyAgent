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

"""
Quick verification test for Phase 17: vLLM-inspired improvements.
"""
import pytest
import asyncio


class TestMathUtils:
    """Test MathUtils module."""

    def test_cdiv(self):
        from src.core.base.utils.MathUtils import cdiv
        assert cdiv(7, 3) == 3
        assert cdiv(6, 3) == 2
        assert cdiv(1, 3) == 1
        assert cdiv(0, 3) == 0

    def test_next_power_of_2(self):
        from src.core.base.utils.MathUtils import next_power_of_2
        assert next_power_of_2(7) == 8
        assert next_power_of_2(8) == 8
        assert next_power_of_2(1) == 1
        assert next_power_of_2(9) == 16

    def test_prev_power_of_2(self):
        from src.core.base.utils.MathUtils import prev_power_of_2
        assert prev_power_of_2(7) == 4
        assert prev_power_of_2(8) == 8
        assert prev_power_of_2(1) == 1

    def test_round_up(self):
        from src.core.base.utils.MathUtils import round_up
        assert round_up(7, 4) == 8
        assert round_up(8, 4) == 8
        assert round_up(1, 4) == 4

    def test_round_down(self):
        from src.core.base.utils.MathUtils import round_down
        assert round_down(7, 4) == 4
        assert round_down(8, 4) == 8


class TestAtomicCounter:
    """Test AtomicCounter module."""

    def test_counter_basic(self):
        from src.core.base.utils.AtomicCounter import Counter
        c = Counter(10)
        assert c.value == 10
        assert c.inc() == 11
        assert c.dec() == 10

    def test_atomic_counter(self):
        from src.core.base.utils.AtomicCounter import AtomicCounter
        c = AtomicCounter(0)
        c.inc(5)
        c.inc(3)
        assert c.value == 8
        c.dec(2)
        assert c.value == 6

    def test_atomic_flag(self):
        from src.core.base.utils.AtomicCounter import AtomicFlag
        f = AtomicFlag(False)
        assert not f.value
        f.set()
        assert f.value
        f.clear()
        assert not f.value

    def test_atomic_gauge(self):
        from src.core.base.utils.AtomicCounter import AtomicGauge
        g = AtomicGauge(0)
        g.inc(10)
        g.dec(3)
        snap = g.snapshot()
        assert snap['value'] == 7
        assert snap['min'] == 0
        assert snap['max'] == 10


class TestCacheInfo:
    """Test CacheInfo module."""

    def test_lru_cache_basic(self):
        from src.observability.stats.CacheInfo import LRUCache
        cache = LRUCache[str, int](max_size=100)
        cache.put("key1", 42)
        assert cache.get("key1") == 42
        assert cache.get("missing") is None

    def test_lru_cache_hit_stats(self):
        from src.observability.stats.CacheInfo import LRUCache
        cache = LRUCache[str, int](max_size=100)
        cache.put("key1", 42)
        cache.get("key1")  # hit
        cache.get("missing")  # miss
        assert cache.stats.hits == 1
        assert cache.stats.misses == 1
        assert cache.stats.hit_ratio == 0.5

    def test_lru_cache_pinned(self):
        from src.observability.stats.CacheInfo import LRUCache
        cache = LRUCache[str, int](max_size=2)
        cache.put("pinned", 100, pinned=True)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # This should evict 'a'
        assert cache.get("pinned") == 100  # Still there
        assert cache.get("a") is None  # Evicted


class TestRequestMetrics:
    """Test RequestMetrics module."""

    def test_request_lifecycle(self):
        from src.observability.stats.RequestMetrics import RequestMetrics, RequestState
        m = RequestMetrics(request_id="test-123")
        m.mark_queued()
        m.mark_scheduled()
        m.mark_processing()
        m.mark_completed()

        assert m.state == RequestState.COMPLETED
        assert m.is_complete
        assert m.is_success
        assert m.total_time_ms is not None
        assert m.total_time_ms >= 0

    def test_request_failed(self):
        from src.observability.stats.RequestMetrics import RequestMetrics, RequestState
        m = RequestMetrics(request_id="fail-123")
        m.mark_failed("Test error")

        assert m.state == RequestState.FAILED
        assert m.is_complete
        assert not m.is_success
        assert m.error == "Test error"


class TestMemorySnapshot:
    """Test MemorySnapshot module."""

    def test_capture_snapshot(self):
        from src.observability.stats.MemorySnapshot import capture_memory_snapshot
        snap = capture_memory_snapshot(include_gpu=False)
        assert snap.gc_objects > 0
        assert snap.timestamp > 0

    def test_gc_stats(self):
        from src.observability.stats.MemorySnapshot import gc_stats
        stats = gc_stats()
        assert 'counts' in stats
        assert 'thresholds' in stats
        assert stats['gc_enabled'] is True


# Check if rust_core is available
try:
    import rust_core as rc
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False


@pytest.mark.skipif(not RUST_AVAILABLE, reason="rust_core not available")
class TestRustFunctions:
    """Test Rust Phase 17 functions."""

    def test_rust_cdiv(self):
        import rust_core as rc
        assert rc.cdiv_rust(7, 3) == 3
        assert rc.cdiv_rust(6, 3) == 2
        assert rc.cdiv_rust(1, 3) == 1

    def test_rust_next_power_of_2(self):
        import rust_core as rc
        assert rc.next_power_of_2_rust(7) == 8
        assert rc.next_power_of_2_rust(8) == 8
        assert rc.next_power_of_2_rust(1) == 1

    def test_rust_round_up(self):
        import rust_core as rc
        assert rc.round_up_rust(7, 4) == 8
        assert rc.round_up_rust(8, 4) == 8

    def test_rust_xxhash(self):
        import rust_core as rc
        h1 = rc.xxhash_rust("test")
        h2 = rc.xxhash_rust("test")
        h3 = rc.xxhash_rust("different")
        assert h1 == h2  # Same input = same hash
        assert h1 != h3  # Different input = different hash
        assert len(h1) == 16  # 64-bit hex

    def test_rust_cache_hit_ratio(self):
        import rust_core as rc
        assert rc.cache_hit_ratio_rust(50, 100) == 0.5
        assert rc.cache_hit_ratio_rust(0, 100) == 0.0
        assert rc.cache_hit_ratio_rust(0, 0) == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

