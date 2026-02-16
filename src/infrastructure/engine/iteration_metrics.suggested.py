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

# SPDX-License-Identifier: Apache-2.0
"""
Iteration Metrics - Comprehensive per-iteration statistics and metrics.

Implements vLLM's metrics patterns with PyAgent enhancements:
- Cache hit/miss statistics
- Request lifecycle metrics
- Performance counters
- Eviction event tracking

Beyond vLLM:
- Sliding window aggregation
- Percentile tracking
- Anomaly detection
- Trend analysis
"""

import statistics
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Deque, Dict, List, Optional, Tuple


class MetricType(Enum):
    """Type of metric."""

    COUNTER = auto()  # Monotonically increasing
    GAUGE = auto()  # Point-in-time value
    HISTOGRAM = auto()  # Distribution
    SUMMARY = auto()  # Percentiles


@dataclass
class BaseCacheStats:
    """Base class for cache statistics."""

    reset: bool = False
    requests: int = 0
    queries: int = 0
    hits: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate hit rate."""
        if self.queries == 0:
            return 0.0
        return self.hits / self.queries


@dataclass
class PrefixCacheStats(BaseCacheStats):
    """Statistics for prefix cache."""

    preempted_requests: int = 0
    preempted_queries: int = 0
    preempted_hits: int = 0

    def record(
        self,
        num_tokens: int,
        num_hits: int,
        preempted: bool = False,
    ) -> None:
        """Record a cache query."""
        if preempted:
            self.preempted_requests += 1
            self.preempted_queries += num_tokens
            self.preempted_hits += num_hits
        else:
            self.requests += 1
            self.queries += num_tokens
            self.hits += num_hits


@dataclass
class MultiModalCacheStats(BaseCacheStats):
    """Statistics for multi-modal cache."""

    def record(self, num_items: int, num_hits: int) -> None:
        """Record a multi-modal cache query."""
        self.requests += 1
        self.queries += num_items
        self.hits += num_hits


@dataclass
class KVCacheEvictionEvent:
    """Single KV cache block eviction sample."""

    block_id: int
    lifetime_seconds: float
    idle_seconds: float
    access_count: int
    timestamp: float = field(default_factory=time.time)


class CachingMetrics:
    """
    Metrics for caching with sliding window aggregation.

    Tracks hit rates over recent N requests.
    """

    def __init__(self, max_recent_requests: int = 1000) -> None:
        self.max_recent_requests = max_recent_requests

        # Aggregated values
        self.aggregated_requests = 0
        self.aggregated_query_total = 0
        self.aggregated_query_hit = 0

        # Sliding window: (requests, queries, hits)
        self.query_queue: Deque[Tuple[int, int, int]] = deque()

    def observe(self, stats: BaseCacheStats) -> None:
        """Observe cache stats for a batch of requests."""
        if stats.reset:
            self.reset()

        if stats.requests == 0:
            return

        # Add to window
        self.query_queue.append((stats.requests, stats.queries, stats.hits))
        self.aggregated_requests += stats.requests
        self.aggregated_query_total += stats.queries
        self.aggregated_query_hit += stats.hits

        # Maintain window size
        while len(self.query_queue) > 1 and self.aggregated_requests > self.max_recent_requests:
            old_reqs, old_queries, old_hits = self.query_queue.popleft()
            self.aggregated_requests -= old_reqs
            self.aggregated_query_total -= old_queries
            self.aggregated_query_hit -= old_hits

    def reset(self) -> None:
        """Reset all metrics."""
        self.aggregated_requests = 0
        self.aggregated_query_total = 0
        self.aggregated_query_hit = 0
        self.query_queue.clear()

    @property
    def hit_rate(self) -> float:
        """Calculate recent hit rate."""
        if self.aggregated_query_total == 0:
            return 0.0
        return self.aggregated_query_hit / self.aggregated_query_total

    @property
    def empty(self) -> bool:
        """Check if no data has been collected."""
        return self.aggregated_requests == 0


@dataclass
class RequestStateStats:
    """Stats tracked across request lifecycle."""

    num_generation_tokens: int = 0

    # Timestamps
    arrival_time: float = 0.0
    queued_ts: float = 0.0
    scheduled_ts: float = 0.0
    first_token_ts: float = 0.0
    last_token_ts: float = 0.0

    # Derived metrics
    first_token_latency: float = 0.0

    # Corruption tracking
    is_corrupted: bool = False

    def record_first_token(self, timestamp: float) -> None:
        """Record first token time."""
        self.first_token_ts = timestamp
        if self.scheduled_ts > 0:
            self.first_token_latency = timestamp - self.scheduled_ts

    def record_token(self, timestamp: float) -> None:
        """Record token generation."""
        self.last_token_ts = timestamp
        self.num_generation_tokens += 1


@dataclass
class FinishedRequestStats:
    """Stats for a completed request."""

    request_id: str
    finish_reason: str

    # Timing
    e2e_latency: float = 0.0
    queued_time: float = 0.0
    prefill_time: float = 0.0
    inference_time: float = 0.0
    decode_time: float = 0.0

    # Token counts
    num_prompt_tokens: int = 0
    num_generation_tokens: int = 0
    num_cached_tokens: int = 0
    max_tokens_param: Optional[int] = None

    # Quality
    is_corrupted: bool = False

    @property
    def mean_time_per_output_token(self) -> float:
        """Calculate mean time per output token."""
        if self.num_generation_tokens == 0:
            return 0.0
        return self.decode_time / self.num_generation_tokens


@dataclass
class SchedulerStats:
    """Stats from the scheduler."""

    num_running_reqs: int = 0
    num_waiting_reqs: int = 0

    # For DP load balancing
    step_counter: int = 0
    current_wave: int = 0

    # Cache usage
    kv_cache_usage: float = 0.0

    # Cache stats
    prefix_cache_stats: PrefixCacheStats = field(default_factory=PrefixCacheStats)
    connector_prefix_cache_stats: Optional[PrefixCacheStats] = None

    # Eviction events
    kv_cache_eviction_events: List[KVCacheEvictionEvent] = field(default_factory=list)

    # LoRA stats
    waiting_lora_adapters: Dict[str, int] = field(default_factory=dict)
    running_lora_adapters: Dict[str, int] = field(default_factory=dict)


@dataclass
class IterationStats:
    """Comprehensive stats for a single iteration."""

    iteration_timestamp: float = field(default_factory=time.time)

    # Token counts
    num_generation_tokens: int = 0
    num_prompt_tokens: int = 0

    # Request counts
    num_preempted_reqs: int = 0
    num_corrupted_reqs: int = 0

    # Finished requests
    finished_requests: List[FinishedRequestStats] = field(default_factory=list)

    # Per-iteration metrics
    max_num_generation_tokens_iter: List[int] = field(default_factory=list)
    n_params_iter: List[int] = field(default_factory=list)
    time_to_first_tokens_iter: List[float] = field(default_factory=list)
    inter_token_latencies_iter: List[float] = field(default_factory=list)

    def record_finished(
        self,
        request_id: str,
        finish_reason: str,
        e2e_latency: float,
        num_prompt_tokens: int,
        num_generation_tokens: int,
        num_cached_tokens: int = 0,
        is_corrupted: bool = False,
    ) -> None:
        """Record a finished request."""
        self.finished_requests.append(
            FinishedRequestStats(
                request_id=request_id,
                finish_reason=finish_reason,
                e2e_latency=e2e_latency,
                num_prompt_tokens=num_prompt_tokens,
                num_generation_tokens=num_generation_tokens,
                num_cached_tokens=num_cached_tokens,
                is_corrupted=is_corrupted,
            )
        )

        if is_corrupted:
            self.num_corrupted_reqs += 1


# ============================================================================
# Beyond vLLM: Advanced Metrics
# ============================================================================
class PercentileTracker:
    """
    Track percentiles over a sliding window.

    Efficiently computes p50, p90, p95, p99 without storing all values.
    """

    def __init__(self, window_size: int = 1000) -> None:
        self.window_size = window_size
        self._values: Deque[float] = deque(maxlen=window_size)
        self._sorted_cache: Optional[List[float]] = None
        self._cache_valid = False

    def record(self, value: float) -> None:
        """Record a value."""
        self._values.append(value)
        self._cache_valid = False

    def _ensure_sorted(self) -> None:
        """Ensure sorted cache is up to date."""
        if not self._cache_valid:
            self._sorted_cache = sorted(self._values)
            self._cache_valid = True

    def percentile(self, p: float) -> float:
        """Get percentile value (0-100)."""
        if not self._values:
            return 0.0

        self._ensure_sorted()
        assert self._sorted_cache is not None

        k = (len(self._sorted_cache) - 1) * (p / 100.0)
        f = int(k)
        c = f + 1 if f < len(self._sorted_cache) - 1 else f

        return self._sorted_cache[f] + (k - f) * (self._sorted_cache[c] - self._sorted_cache[f])

    @property
    def p50(self) -> float:
        """Get 50th percentile."""
        return self.percentile(50)

    @property
    def p90(self) -> float:
        """Get 90th percentile."""
        return self.percentile(90)

    @property
    def p95(self) -> float:
        """Get 95th percentile."""
        return self.percentile(95)

    @property
    def p99(self) -> float:
        """Get 99th percentile."""
        return self.percentile(99)

    @property
    def mean(self) -> float:
        """Get mean value."""
        if not self._values:
            return 0.0
        return statistics.mean(self._values)

    @property
    def std(self) -> float:
        """Get standard deviation."""
        if len(self._values) < 2:
            return 0.0
        return statistics.stdev(self._values)


class TrendAnalyzer:
    """
    Analyze trends in metrics over time.

    Detects increasing, decreasing, or stable trends.
    """

    def __init__(self, window_size: int = 100) -> None:
        self.window_size = window_size
        self._values: Deque[Tuple[float, float]] = deque(maxlen=window_size)

    def record(self, value: float, timestamp: Optional[float] = None) -> None:
        """Record a value with timestamp."""
        ts = timestamp or time.time()
        self._values.append((ts, value))

    def get_trend(self) -> Tuple[str, float]:
        """
        Calculate trend direction and slope.

        Returns:
            (direction, slope) where direction is 'increasing', 'decreasing', or 'stable'
        """
        if len(self._values) < 2:
            return "stable", 0.0

        # Simple linear regression
        n = len(self._values)
        sum_x = sum(v[0] for v in self._values)
        sum_y = sum(v[1] for v in self._values)
        sum_xy = sum(v[0] * v[1] for v in self._values)
        sum_xx = sum(v[0] ** 2 for v in self._values)

        denom = n * sum_xx - sum_x**2
        if abs(denom) < 1e-10:
            return "stable", 0.0

        slope = (n * sum_xy - sum_x * sum_y) / denom

        # Determine direction based on slope magnitude
        threshold = 0.01  # Sensitivity threshold
        if slope > threshold:
            return "increasing", slope
        if slope < -threshold:
            return "decreasing", slope
        return "stable", slope


class AnomalyDetector:
    """
    Detect anomalies in metric values using z-score.
    """

    def __init__(
        self,
        window_size: int = 100,
        z_threshold: float = 3.0,
    ) -> None:
        self.window_size = window_size
        self.z_threshold = z_threshold
        self._values: Deque[float] = deque(maxlen=window_size)
        self._mean = 0.0
        self._m2 = 0.0  # For online variance calculation
        self._count = 0

    def record(self, value: float) -> bool:
        """
        Record a value and check for anomaly.

        Returns True if value is anomalous.
        """
        self._values.append(value)

        # Update running stats (Welford's algorithm)
        self._count += 1
        delta = value - self._mean
        self._mean += delta / self._count
        delta2 = value - self._mean
        self._m2 += delta * delta2

        # Check for anomaly
        if self._count < 10:
            return False

        variance = self._m2 / self._count
        std = variance**0.5

        if std < 1e-10:
            return False

        z_score = abs(value - self._mean) / std
        return z_score > self.z_threshold

    @property
    def mean(self) -> float:
        """Get mean value."""
        return self._mean

    @property
    def std(self) -> float:
        """Get standard deviation."""
        if self._count < 2:
            return 0.0
        return (self._m2 / self._count) ** 0.5


class MetricsCollector:
    """
    Comprehensive metrics collection.

    Aggregates all metrics types with thread safety.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()

        # Counters
        self.counters: Dict[str, int] = {}

        # Gauges
        self.gauges: Dict[str, float] = {}

        # Histograms (using PercentileTracker)
        self.histograms: Dict[str, PercentileTracker] = {}

        # Trend analyzers
        self.trends: Dict[str, TrendAnalyzer] = {}

        # Anomaly detectors
        self.anomaly_detectors: Dict[str, AnomalyDetector] = {}

        # Cache metrics
        self.cache_metrics = CachingMetrics()

    def increment(self, name: str, value: int = 1) -> None:
        """Increment a counter."""
        with self._lock:
            self.counters[name] = self.counters.get(name, 0) + value

    def set_gauge(self, name: str, value: float) -> None:
        """Set a gauge value."""
        with self._lock:
            self.gauges[name] = value

    def record_histogram(self, name: str, value: float) -> None:
        """Record a histogram value."""
        with self._lock:
            if name not in self.histograms:
                self.histograms[name] = PercentileTracker()
            self.histograms[name].record(value)

    def record_trend(self, name: str, value: float) -> None:
        """Record value for trend analysis."""
        with self._lock:
            if name not in self.trends:
                self.trends[name] = TrendAnalyzer()
            self.trends[name].record(value)

    def check_anomaly(self, name: str, value: float) -> bool:
        """Check if value is anomalous."""
        with self._lock:
            if name not in self.anomaly_detectors:
                self.anomaly_detectors[name] = AnomalyDetector()
            return self.anomaly_detectors[name].record(value)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics."""
        with self._lock:
            return {
                "counters": dict(self.counters),
                "gauges": dict(self.gauges),
                "histograms": {
                    name: {
                        "mean": tracker.mean,
                        "p50": tracker.p50,
                        "p90": tracker.p90,
                        "p99": tracker.p99,
                    }
                    for name, tracker in self.histograms.items()
                },
                "trends": {name: analyzer.get_trend() for name, analyzer in self.trends.items()},
                "cache": {
                    "hit_rate": self.cache_metrics.hit_rate,
                },
            }


# ============================================================================
# Exports
# ============================================================================
__all__ = [
    # Enums
    "MetricType",
    # Base stats
    "BaseCacheStats",
    "PrefixCacheStats",
    "MultiModalCacheStats",
    "KVCacheEvictionEvent",
    # Caching
    "CachingMetrics",
    # Request stats
    "RequestStateStats",
    "FinishedRequestStats",
    "SchedulerStats",
    "IterationStats",
    # Advanced metrics
    "PercentileTracker",
    "TrendAnalyzer",
    "AnomalyDetector",
    "MetricsCollector",
]
