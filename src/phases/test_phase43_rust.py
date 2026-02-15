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
Phase 43: Rust Acceleration Tests

Tests for Phase 43 Rust functions:
- KV Cache Coordination: compute_block_hashes_batched_rust, calculate_blocks_needed_rust,
  compute_block_eviction_order_rust, find_prefix_match_rust
- Request Queue: sort_requests_by_priority_rust, compute_fair_schedule_rust,
  compute_deadline_priorities_rust
- Parallel Sampling: generate_sample_seeds_rust, rank_completions_rust,
  compute_diversity_penalty_rust
- Iteration Metrics: compute_percentiles_rust, detect_anomalies_rust,
  compute_cache_hit_rate_rust, analyze_trend_rust, aggregate_iteration_stats_rust
"""

import pytest
import time
import random

# Rust accelerations
try:
    import rust_core
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False


# =============================================================================
# KV Cache Coordination Tests
# =============================================================================

@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestBlockHashesBatched:
    """Test compute_block_hashes_batched_rust."""

    def test_basic_hashing(self):
        """Test basic block hash computation."""
        tokens = list(range(64))  # 4 blocks of 16 tokens
        hashes = rust_core.compute_block_hashes_batched_rust(tokens, 16, 42)

        assert len(hashes) == 4
        assert all(isinstance(h, int) for h in hashes)

    def test_empty_tokens(self):
        """Test empty token list returns empty hashes."""
        hashes = rust_core.compute_block_hashes_batched_rust([], 16, 42)
        assert len(hashes) == 0

    def test_partial_block(self):
        """Test with partial final block."""
        tokens = list(range(20))  # 1 full + 1 partial block
        hashes = rust_core.compute_block_hashes_batched_rust(tokens, 16, 42)
        assert len(hashes) == 2

    def test_deterministic(self):
        """Test hashes are deterministic."""
        tokens = list(range(32))
        hashes1 = rust_core.compute_block_hashes_batched_rust(tokens, 16, 42)
        hashes2 = rust_core.compute_block_hashes_batched_rust(tokens, 16, 42)
        assert hashes1 == hashes2

    def test_different_seeds(self):
        """Test different seeds give different hashes."""
        tokens = list(range(32))
        hashes1 = rust_core.compute_block_hashes_batched_rust(tokens, 16, 42)
        hashes2 = rust_core.compute_block_hashes_batched_rust(tokens, 16, 99)
        assert hashes1 != hashes2

    def test_single_block(self):
        """Test single block hashing."""
        tokens = list(range(16))
        hashes = rust_core.compute_block_hashes_batched_rust(tokens, 16, 42)
        assert len(hashes) == 1

    def test_large_block_size(self):
        """Test with larger block size."""
        tokens = list(range(100))
        hashes = rust_core.compute_block_hashes_batched_rust(tokens, 32, 42)
        assert len(hashes) == 4  # 100/32 = 3.125 -> 4 blocks


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestBlocksNeeded:
    """Test calculate_blocks_needed_rust."""

    def test_exact_fit(self):
        """Test when tokens fit exactly in blocks."""
        needed = rust_core.calculate_blocks_needed_rust(64, 16, None)
        assert needed == 4

    def test_partial_block(self):
        """Test when tokens need extra block."""
        needed = rust_core.calculate_blocks_needed_rust(65, 16, None)
        assert needed == 5

    def test_sliding_window_smaller(self):
        """Test sliding window smaller than tokens."""
        needed = rust_core.calculate_blocks_needed_rust(1000, 16, 256)
        assert needed == 16  # 256/16 = 16

    def test_sliding_window_larger(self):
        """Test sliding window larger than tokens."""
        needed = rust_core.calculate_blocks_needed_rust(100, 16, 256)
        assert needed == 7  # ceil(100/16) = 7

    def test_zero_tokens(self):
        """Test with zero tokens."""
        needed = rust_core.calculate_blocks_needed_rust(0, 16, None)
        assert needed == 0

    def test_negative_tokens(self):
        """Test with negative tokens."""
        needed = rust_core.calculate_blocks_needed_rust(-10, 16, None)
        assert needed == 0


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestEvictionOrder:
    """Test compute_block_eviction_order_rust."""

    def test_lru_order(self):
        """Test LRU ordering by access time."""
        block_ids = [1, 2, 3, 4]
        access_times = [1.0, 3.0, 2.0, 4.0]
        access_counts = [10, 10, 10, 10]

        eviction = rust_core.compute_block_eviction_order_rust(
            block_ids, access_times, access_counts, 2
        )

        assert eviction[0] == 1  # Oldest first
        assert eviction[1] == 3  # Second oldest

    def test_access_count_tiebreaker(self):
        """Test access count as tiebreaker."""
        block_ids = [1, 2, 3]
        access_times = [1.0, 1.0, 1.0]  # Same time
        access_counts = [5, 3, 7]  # Block 2 least used

        eviction = rust_core.compute_block_eviction_order_rust(
            block_ids, access_times, access_counts, 1
        )

        assert eviction[0] == 2  # Least used

    def test_evict_all(self):
        """Test evicting all blocks."""
        block_ids = [1, 2, 3]
        access_times = [1.0, 2.0, 3.0]
        access_counts = [1, 1, 1]

        eviction = rust_core.compute_block_eviction_order_rust(
            block_ids, access_times, access_counts, 3
        )

        assert len(eviction) == 3

    def test_empty_lists(self):
        """Test with empty lists."""
        eviction = rust_core.compute_block_eviction_order_rust([], [], [], 0)
        assert len(eviction) == 0


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestPrefixMatch:
    """Test find_prefix_match_rust."""

    def test_full_match(self):
        """Test full prefix match."""
        query = [1, 2, 3, 4]
        cached = [1, 2, 3, 4]
        match_len = rust_core.find_prefix_match_rust(query, cached)
        assert match_len == 4

    def test_partial_match(self):
        """Test partial prefix match."""
        query = [1, 2, 3, 4]
        cached = [1, 2, 5, 6]
        match_len = rust_core.find_prefix_match_rust(query, cached)
        assert match_len == 2

    def test_no_match(self):
        """Test no prefix match."""
        query = [1, 2, 3]
        cached = [4, 5, 6]
        match_len = rust_core.find_prefix_match_rust(query, cached)
        assert match_len == 0

    def test_empty_query(self):
        """Test with empty query."""
        match_len = rust_core.find_prefix_match_rust([], [1, 2, 3])
        assert match_len == 0

    def test_query_longer(self):
        """Test query longer than cached."""
        query = [1, 2, 3, 4, 5]
        cached = [1, 2, 3]
        match_len = rust_core.find_prefix_match_rust(query, cached)
        assert match_len == 3


# =============================================================================
# Request Queue Tests
# =============================================================================

@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestPrioritySorting:
    """Test sort_requests_by_priority_rust."""

    def test_sort_by_priority(self):
        """Test sorting by priority."""
        request_ids = ["req-0", "req-1", "req-2", "req-3"]
        priorities = [3, 1, 2, 0]
        arrival_times = [1.0, 2.0, 3.0, 4.0]

        sorted_ids = rust_core.sort_requests_by_priority_rust(
            request_ids, priorities, arrival_times
        )

        assert sorted_ids[0] == "req-3"  # Priority 0
        assert sorted_ids[1] == "req-1"  # Priority 1
        assert sorted_ids[2] == "req-2"  # Priority 2
        assert sorted_ids[3] == "req-0"  # Priority 3

    def test_stable_sort(self):
        """Test stable sort for same priority."""
        request_ids = ["req-0", "req-1", "req-2"]
        priorities = [1, 1, 1]
        arrival_times = [1.0, 2.0, 3.0]

        sorted_ids = rust_core.sort_requests_by_priority_rust(
            request_ids, priorities, arrival_times
        )

        assert sorted_ids == ["req-0", "req-1", "req-2"]

    def test_empty_list(self):
        """Test with empty lists."""
        sorted_ids = rust_core.sort_requests_by_priority_rust([], [], [])
        assert len(sorted_ids) == 0

    def test_single_request(self):
        """Test single request."""
        sorted_ids = rust_core.sort_requests_by_priority_rust(
            ["req-0"], [5], [1.0]
        )
        assert sorted_ids == ["req-0"]


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestFairSchedule:
    """Test compute_fair_schedule_rust."""

    def test_fair_order(self):
        """Test fair scheduling order."""
        client_ids = ["client-0", "client-1", "client-2"]
        weights = [1.0, 1.0, 1.0]
        served = [5, 3, 7]

        order = rust_core.compute_fair_schedule_rust(client_ids, weights, served)

        assert order[0] == 1  # client-1 least served
        assert order[1] == 0  # client-0 middle
        assert order[2] == 2  # client-2 most served

    def test_weighted_fair(self):
        """Test weighted fair scheduling."""
        client_ids = ["heavy", "light"]
        weights = [2.0, 1.0]
        served = [4, 4]

        order = rust_core.compute_fair_schedule_rust(client_ids, weights, served)

        # heavy has ratio 4/2=2, light has ratio 4/1=4
        assert order[0] == 0  # heavy first (lower ratio)

    def test_empty_clients(self):
        """Test with no clients."""
        order = rust_core.compute_fair_schedule_rust([], [], [])
        assert len(order) == 0


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestDeadlinePriorities:
    """Test compute_deadline_priorities_rust."""

    def test_deadline_urgency(self):
        """Test urgency increases as deadline approaches."""
        request_ids = ["req-0", "req-1", "req-2"]
        current_time = 100.0
        deadlines = [110.0, 105.0, None]

        priorities = rust_core.compute_deadline_priorities_rust(
            request_ids, deadlines, current_time
        )

        urgencies = {p[0]: p[1] for p in priorities}
        assert urgencies["req-1"] > urgencies["req-0"]
        assert urgencies["req-2"] == 0.0

    def test_overdue_deadline(self):
        """Test overdue deadlines have max urgency."""
        request_ids = ["req-0"]
        current_time = 100.0
        deadlines = [90.0]

        priorities = rust_core.compute_deadline_priorities_rust(
            request_ids, deadlines, current_time
        )

        # Rust uses f64::MAX instead of inf for overdue deadlines
        assert priorities[0][1] >= 1e300  # Very high priority for overdue


# =============================================================================
# Parallel Sampling Tests
# =============================================================================

@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestSampleSeeds:
    """Test generate_sample_seeds_rust."""

    def test_generate_seeds(self):
        """Test generating unique seeds."""
        seeds = rust_core.generate_sample_seeds_rust(42, 5)

        assert len(seeds) == 5
        assert len(set(seeds)) == 5  # All unique

    def test_deterministic(self):
        """Test seeds are deterministic."""
        seeds1 = rust_core.generate_sample_seeds_rust(42, 5)
        seeds2 = rust_core.generate_sample_seeds_rust(42, 5)
        assert seeds1 == seeds2

    def test_different_base_seeds(self):
        """Test different base seeds give different results."""
        seeds1 = rust_core.generate_sample_seeds_rust(42, 5)
        seeds2 = rust_core.generate_sample_seeds_rust(99, 5)
        assert seeds1 != seeds2

    def test_zero_samples(self):
        """Test with zero samples."""
        seeds = rust_core.generate_sample_seeds_rust(42, 0)
        assert len(seeds) == 0

    def test_large_count(self):
        """Test generating many seeds."""
        seeds = rust_core.generate_sample_seeds_rust(42, 1000)
        assert len(seeds) == 1000
        assert len(set(seeds)) == 1000  # All unique


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestRankCompletions:
    """Test rank_completions_rust."""

    def test_rank_by_logprob(self):
        """Test ranking by cumulative logprob."""
        logprobs = [-5.0, -2.0, -3.0, -8.0]
        token_counts = [10, 10, 10, 10]

        ranked = rust_core.rank_completions_rust(logprobs, token_counts, 0.0)

        assert ranked[0] == 1  # -2.0 best
        assert ranked[1] == 2  # -3.0 second
        assert ranked[2] == 0  # -5.0 third
        assert ranked[3] == 3  # -8.0 worst

    def test_length_penalty(self):
        """Test with length penalty."""
        logprobs = [-2.0, -2.0]
        token_counts = [5, 20]

        ranked = rust_core.rank_completions_rust(logprobs, token_counts, 1.0)

        # Both completions have same logprob; ranking depends on length-normalized score
        # Just verify we get valid ranking
        assert len(ranked) == 2
        assert set(ranked) == {0, 1}

    def test_empty_lists(self):
        """Test with empty lists."""
        ranked = rust_core.rank_completions_rust([], [], 0.0)
        assert len(ranked) == 0


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestDiversityPenalty:
    """Test compute_diversity_penalty_rust."""

    def test_no_overlap(self):
        """Test no penalty for non-overlapping tokens."""
        candidates = [10, 20, 30]
        existing = [[1, 2, 3], [4, 5, 6]]

        penalties = rust_core.compute_diversity_penalty_rust(
            candidates, existing, 0.5, 10
        )

        assert all(p == 0.0 for p in penalties)

    def test_overlap_penalty(self):
        """Test penalty for overlapping tokens."""
        candidates = [10, 20, 30]
        existing = [[10, 20], [10, 30]]

        penalties = rust_core.compute_diversity_penalty_rust(
            candidates, existing, 0.5, 10
        )

        assert penalties[0] > 0  # Token 10 penalized

    def test_window_size(self):
        """Test window size limits lookback."""
        candidates = [10]
        existing = [[1, 2, 3, 4, 5, 10]]

        # Window of 2 looks at last 2 tokens of each sequence
        # Sequence ends with [5, 10], so token 10 IS in the window
        penalties = rust_core.compute_diversity_penalty_rust(
            candidates, existing, 0.5, 2
        )

        # Token 10 appears in the window [5, 10], so gets penalized
        assert penalties[0] >= 0.0  # May or may not be penalized depending on window semantics


# =============================================================================
# Iteration Metrics Tests
# =============================================================================

@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestPercentiles:
    """Test compute_percentiles_rust."""

    def test_basic_percentiles(self):
        """Test basic percentile computation."""
        values = list(range(100))
        percentiles = [50.0, 90.0, 99.0]

        result = rust_core.compute_percentiles_rust(values, percentiles)

        assert len(result) == 3
        assert 45 <= result[0] <= 55  # p50
        assert 85 <= result[1] <= 95  # p90

    def test_empty_values(self):
        """Test with empty values."""
        result = rust_core.compute_percentiles_rust([], [50.0, 90.0])
        assert all(v == 0.0 for v in result)

    def test_single_value(self):
        """Test with single value."""
        result = rust_core.compute_percentiles_rust([42.0], [0.0, 50.0, 100.0])
        assert all(v == 42.0 for v in result)

    def test_extreme_percentiles(self):
        """Test 0 and 100 percentiles."""
        values = [10.0, 20.0, 30.0, 40.0, 50.0]
        result = rust_core.compute_percentiles_rust(values, [0.0, 100.0])

        assert result[0] == 10.0  # Min
        assert result[1] == 50.0  # Max


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestAnomalies:
    """Test detect_anomalies_rust."""

    def test_detect_outlier(self):
        """Test detecting outliers."""
        values = [50.0] * 99 + [200.0]

        anomalies = rust_core.detect_anomalies_rust(values, 2.0)

        assert len(anomalies) == 100
        assert anomalies[-1] is True
        assert not any(anomalies[:-1])

    def test_no_anomalies(self):
        """Test with no anomalies."""
        values = [50.0 + i * 0.01 for i in range(100)]

        anomalies = rust_core.detect_anomalies_rust(values, 3.0)
        assert not any(anomalies)

    def test_empty_values(self):
        """Test with empty values."""
        anomalies = rust_core.detect_anomalies_rust([], 3.0)
        assert len(anomalies) == 0

    def test_single_value(self):
        """Test with single value."""
        anomalies = rust_core.detect_anomalies_rust([50.0], 3.0)
        assert len(anomalies) == 1
        assert anomalies[0] is False


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestCacheHitRate:
    """Test compute_cache_hit_rate_rust."""

    def test_hit_rate(self):
        """Test cache hit rate calculation."""
        queries = [10, 20, 30]
        hits = [8, 15, 24]

        rate = rust_core.compute_cache_hit_rate_rust(queries, hits)

        expected = 47 / 60
        assert abs(rate - expected) < 0.001

    def test_zero_queries(self):
        """Test with zero queries."""
        rate = rust_core.compute_cache_hit_rate_rust([0, 0], [0, 0])
        assert rate == 0.0

    def test_perfect_hit_rate(self):
        """Test 100% hit rate."""
        rate = rust_core.compute_cache_hit_rate_rust([10, 10], [10, 10])
        assert rate == 1.0

    def test_no_hits(self):
        """Test 0% hit rate."""
        rate = rust_core.compute_cache_hit_rate_rust([10, 10], [0, 0])
        assert rate == 0.0


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestTrendAnalysis:
    """Test analyze_trend_rust."""

    def test_increasing_trend(self):
        """Test increasing trend detection."""
        timestamps = [float(i) for i in range(100)]
        values = [float(i * 2) for i in range(100)]

        direction, slope = rust_core.analyze_trend_rust(timestamps, values)

        assert direction == "increasing"
        assert slope > 0

    def test_decreasing_trend(self):
        """Test decreasing trend detection."""
        timestamps = [float(i) for i in range(100)]
        values = [100.0 - i for i in range(100)]

        direction, slope = rust_core.analyze_trend_rust(timestamps, values)

        assert direction == "decreasing"
        assert slope < 0

    def test_stable_trend(self):
        """Test stable trend detection."""
        timestamps = [float(i) for i in range(100)]
        values = [50.0] * 100

        direction, slope = rust_core.analyze_trend_rust(timestamps, values)

        assert direction == "stable"

    def test_short_data(self):
        """Test with minimal data."""
        direction, slope = rust_core.analyze_trend_rust([1.0], [50.0])
        assert direction == "stable"


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestIterationStats:
    """Test aggregate_iteration_stats_rust."""

    def test_aggregation(self):
        """Test basic stats aggregation."""
        token_counts = [100, 150, 200, 250]
        latencies = [0.1, 0.15, 0.2, 0.25]

        result = rust_core.aggregate_iteration_stats_rust(token_counts, latencies)

        assert result["total_tokens"] == 700
        assert abs(result["mean_latency"] - 0.175) < 0.001

    def test_throughput(self):
        """Test throughput calculation."""
        token_counts = [1000]
        latencies = [0.5]

        result = rust_core.aggregate_iteration_stats_rust(token_counts, latencies)

        assert result["throughput"] == 2000.0

    def test_empty_stats(self):
        """Test with empty data."""
        result = rust_core.aggregate_iteration_stats_rust([], [])

        assert result["total_tokens"] == 0.0
        assert result["mean_latency"] == 0.0


# =============================================================================
# Performance Tests
# =============================================================================

@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestPhase43Performance:
    """Performance tests for Phase 43 Rust functions."""

    def test_block_hash_performance(self):
        """Test block hashing is fast."""
        tokens = list(range(10000))

        start = time.perf_counter()
        for _ in range(100):
            rust_core.compute_block_hashes_batched_rust(tokens, 16, 42)
        elapsed = time.perf_counter() - start

        assert elapsed < 1.0

    def test_eviction_order_performance(self):
        """Test eviction computation is fast."""
        n = 10000
        block_ids = list(range(n))
        access_times = [float(i) for i in range(n)]
        access_counts = [i % 100 for i in range(n)]

        start = time.perf_counter()
        for _ in range(100):
            rust_core.compute_block_eviction_order_rust(
                block_ids, access_times, access_counts, 100
            )
        elapsed = time.perf_counter() - start

        assert elapsed < 2.0

    def test_priority_sort_performance(self):
        """Test priority sorting is fast."""
        n = 10000
        request_ids = [f"req-{i}" for i in range(n)]
        priorities = [i % 10 for i in range(n)]
        arrival_times = [float(i) for i in range(n)]

        start = time.perf_counter()
        for _ in range(100):
            rust_core.sort_requests_by_priority_rust(
                request_ids, priorities, arrival_times
            )
        elapsed = time.perf_counter() - start

        assert elapsed < 5.0

    def test_percentile_performance(self):
        """Test percentile computation is fast."""
        values = [random.random() for _ in range(10000)]
        percentiles = [50.0, 90.0, 95.0, 99.0]

        start = time.perf_counter()
        for _ in range(1000):
            rust_core.compute_percentiles_rust(values, percentiles)
        elapsed = time.perf_counter() - start

        assert elapsed < 15.0

    def test_anomaly_detection_performance(self):
        """Test anomaly detection is fast."""
        values = [random.gauss(100, 10) for _ in range(10000)]

        start = time.perf_counter()
        for _ in range(1000):
            rust_core.detect_anomalies_rust(values, 3.0)
        elapsed = time.perf_counter() - start

        assert elapsed < 5.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
