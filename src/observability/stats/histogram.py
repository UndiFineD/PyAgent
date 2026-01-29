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
Histogram - Efficient percentile and distribution tracking.

Goes beyond vLLM with production-grade metrics:
- HDR Histogram-style logarithmic buckets
- Constant memory regardless of sample count
- O(1) add, O(buckets) percentile queries
- Mergeable for distributed aggregation

Phase 18: Beyond vLLM - Advanced Metrics
"""
# pylint: disable=protected-access

from __future__ import annotations

from _thread import LockType
import math
import threading
from dataclasses import dataclass


@dataclass
class HistogramBucket:
    """A single histogram bucket."""

    lower_bound: float
    upper_bound: float
    count: int = 0

    @property
    def midpoint(self) -> float:
        """Get bucket midpoint."""
        return (self.lower_bound + self.upper_bound) / 2


class Histogram:
    """
    Fixed-bucket histogram for efficient distribution tracking.

    Provides approximate percentiles with constant memory.

    Example:
        >>> h = Histogram(min_value=1.0, max_value=10000.0, num_buckets=100)
        >>>
        >>> for latency in response_times:
        ...     h.add(latency)
        >>>
        >>> print(f"P50: {h.percentile(50)}, P99: {h.percentile(99)}")
    """

    def __init__(
        self,
        min_value: float = 0.0,
        max_value: float = 10000.0,
        num_buckets: int = 100,
        logarithmic: bool = True,
    ) -> None:
        """
        Initialize histogram.

        Args:
            min_value: Minimum trackable value
            max_value: Maximum trackable value
            num_buckets: Number of buckets
            logarithmic: Use logarithmic bucket spacing
        """
        self._min_value: float = max(0.001, min_value)  # Avoid log(0)
        self._max_value: float = max_value
        self._num_buckets: int = num_buckets
        self._logarithmic: bool = logarithmic

        self._buckets: list[HistogramBucket] = self._create_buckets()
        self._count = 0
        self._sum = 0.0
        self._min = float("inf")
        self._max = float("-inf")
        self._underflow = 0
        self._overflow = 0
        self._lock: LockType = threading.Lock()

    def _create_buckets(self) -> list[HistogramBucket]:
        """Create bucket boundaries."""
        buckets = []

        if self._logarithmic:
            log_min: float = math.log10(self._min_value)
            log_max: float = math.log10(self._max_value)
            log_step: float = (log_max - log_min) / self._num_buckets

            for i in range(self._num_buckets):
                lower: float = 10 ** (log_min + i * log_step)
                upper: float = 10 ** (log_min + (i + 1) * log_step)
                buckets.append(HistogramBucket(lower_bound=lower, upper_bound=upper))
        else:
            step: float = (self._max_value - self._min_value) / self._num_buckets

            for i in range(self._num_buckets):
                lower: float = self._min_value + i * step
                upper: float = self._min_value + (i + 1) * step
                buckets.append(HistogramBucket(lower_bound=lower, upper_bound=upper))

        return buckets

    def _find_bucket_index(self, value: float) -> int:
        """Find bucket index for a value."""
        if value < self._min_value:
            return -1  # Underflow
        if value >= self._max_value:
            return self._num_buckets  # Overflow

        if self._logarithmic:
            log_min: float = math.log10(self._min_value)
            log_max: float = math.log10(self._max_value)
            log_val: float = math.log10(max(self._min_value, value))

            idx = int((log_val - log_min) / (log_max - log_min) * self._num_buckets)
        else:
            idx = int((value - self._min_value) / (self._max_value - self._min_value) * self._num_buckets)

        return max(0, min(idx, self._num_buckets - 1))

    def add(self, value: float, count: int = 1) -> None:
        """
        Add a value to the histogram.

        Args:
            value: Value to add
            count: Number of occurrences (default 1)
        """
        with self._lock:
            self._count += count
            self._sum += value * count
            self._min = min(self._min, value)
            self._max = max(self._max, value)

            idx: int = self._find_bucket_index(value)

            if idx < 0:
                self._underflow += count
            elif idx >= self._num_buckets:
                self._overflow += count
            else:
                self._buckets[idx].count += count

    def percentile(self, p: float) -> float:
        """
        Get percentile value.

        Args:
            p: Percentile (0-100)

        Returns:
            Approximate percentile value
        """
        with self._lock:
            if self._count == 0:
                return 0.0

            target: float = self._count * p / 100
            cumulative: int = self._underflow

            if cumulative >= target and self._underflow > 0:
                return self._min_value

            for bucket in self._buckets:
                cumulative += bucket.count
                if cumulative >= target:
                    return bucket.midpoint

            return self._max_value

    def mean(self) -> float:
        """Get mean value."""
        with self._lock:
            if self._count == 0:
                return 0.0
            return self._sum / self._count

    @property
    def count(self) -> int:
        """Get total count."""
        return self._count

    @property
    def min_observed(self) -> float:
        """Get minimum observed value."""
        return self._min if self._count > 0 else 0.0

    @property
    def max_observed(self) -> float:
        """Get maximum observed value."""
        return self._max if self._count > 0 else 0.0

    def merge(self, other: "Histogram") -> "Histogram":
        """
        Merge with another histogram.

        Returns:
            New merged histogram
        """
        # Create new histogram with same configuration
        merged = Histogram(
            min_value=min(self._min_value, other._min_value),
            max_value=max(self._max_value, other._max_value),
            num_buckets=self._num_buckets,
            logarithmic=self._logarithmic,
        )

        # Note: This is approximate due to bucket boundary differences
        merged._count = self._count + other._count
        merged._sum = self._sum + other._sum
        merged._min = min(self._min, other._min)
        merged._max = max(self._max, other._max)
        merged._underflow = self._underflow + other._underflow
        merged._overflow = self._overflow + other._overflow

        for i, (b1, b2) in enumerate(zip(self._buckets, other._buckets)):
            merged._buckets[i].count = b1.count + b2.count

        return merged

    def get_buckets(self) -> list[tuple[float, float, int]]:
        """Get bucket data as (lower, upper, count) tuples."""
        return [(b.lower_bound, b.upper_bound, b.count) for b in self._buckets]

    def get_stats(self) -> dict:
        """Get comprehensive statistics."""
        return {
            "count": self._count,
            "sum": round(self._sum, 4),
            "mean": round(self.mean(), 4),
            "min": round(self.min_observed, 4),
            "max": round(self.max_observed, 4),
            "p50": round(self.percentile(50), 4),
            "p75": round(self.percentile(75), 4),
            "p90": round(self.percentile(90), 4),
            "p95": round(self.percentile(95), 4),
            "p99": round(self.percentile(99), 4),
            "p999": round(self.percentile(99.9), 4),
            "underflow": self._underflow,
            "overflow": self._overflow,
        }

    def reset(self) -> None:
        """Reset all counts."""
        with self._lock:
            for bucket in self._buckets:
                bucket.count = 0
            self._count = 0
            self._sum = 0.0
            self._min = float("inf")
            self._max = float("-inf")
            self._underflow = 0
            self._overflow = 0


class ExponentialHistogram:
    """
    Histogram with exponentially growing bucket boundaries.

    Based on OpenTelemetry exponential histogram spec.
    Better accuracy for wide value ranges.

    Example:
        >>> h = ExponentialHistogram(scale=2)
        >>>
        >>> for v in values:
        ...     h.add(v)
        >>>
        >>> print(h.get_stats())
    """

    def __init__(
        self,
        scale: int = 2,
        max_buckets: int = 160,
    ) -> None:
        """
        Initialize exponential histogram.

        Args:
            scale: Resolution (higher = more buckets)
            max_buckets: Maximum number of buckets
        """
        self._scale: int = scale
        self._max_buckets: int = max_buckets
        self._base = 2 ** (2**-scale)

        # Positive and negative buckets
        self._positive: dict[int, int] = {}
        self._negative: dict[int, int] = {}
        self._zero_count = 0

        self._count = 0
        self._sum = 0.0
        self._min = float("inf")
        self._max = float("-inf")
        self._lock: LockType = threading.Lock()

    def _value_to_bucket(self, value: float) -> int:
        """Map value to bucket index."""
        if value <= 0:
            return 0
        return int(math.ceil(math.log(value) / math.log(self._base)))

    def _bucket_to_lower(self, index: int) -> float:
        """Get lower bound for bucket index."""
        return self._base ** (index - 1)

    def _bucket_to_upper(self, index: int) -> float:
        """Get upper bound for bucket index."""
        return self._base**index

    def add(self, value: float) -> None:
        """Add a value to the histogram."""
        with self._lock:
            self._count += 1
            self._sum += value
            self._min = min(self._min, value)
            self._max = max(self._max, value)

            if value == 0:
                self._zero_count += 1
            elif value > 0:
                idx: int = self._value_to_bucket(value)
                self._positive[idx] = self._positive.get(idx, 0) + 1
            else:
                idx: int = self._value_to_bucket(-value)
                self._negative[idx] = self._negative.get(idx, 0) + 1

    def percentile(self, p: float) -> float:
        """Get percentile value."""
        with self._lock:
            if self._count == 0:
                return 0.0

            target: float = self._count * p / 100
            cumulative = 0

            # Handle negatives
            for idx in sorted(self._negative.keys(), reverse=True):
                cumulative += self._negative[idx]
                if cumulative >= target:
                    return -self._bucket_to_upper(idx)

            # Handle zeros
            cumulative += self._zero_count
            if cumulative >= target:
                return 0.0

            # Handle positives
            for idx in sorted(self._positive.keys()):
                cumulative += self._positive[idx]
                if cumulative >= target:
                    return self._bucket_to_lower(idx)

            return self._max

    def mean(self) -> float:
        """Get mean value."""
        if self._count == 0:
            return 0.0
        return self._sum / self._count

    @property
    def count(self) -> int:
        """Get total count."""
        return self._count

    def get_stats(self) -> dict:
        """Get statistics."""
        return {
            "count": self._count,
            "sum": round(self._sum, 4),
            "mean": round(self.mean(), 4),
            "min": round(self._min, 4) if self._count > 0 else 0,
            "max": round(self._max, 4) if self._count > 0 else 0,
            "p50": round(self.percentile(50), 4),
            "p90": round(self.percentile(90), 4),
            "p99": round(self.percentile(99), 4),
            "scale": self._scale,
            "positive_buckets": len(self._positive),
            "negative_buckets": len(self._negative),
            "zero_count": self._zero_count,
        }

    def reset(self) -> None:
        """Reset histogram."""
        with self._lock:
            self._positive.clear()
            self._negative.clear()
            self._zero_count = 0
            self._count = 0
            self._sum = 0.0
            self._min = float("inf")
            self._max = float("-inf")


class LatencyHistogram(Histogram):
    """
    Pre-configured histogram for latency tracking (microseconds to seconds).

    Common for API response time monitoring.

    Example:
        >>> latency = LatencyHistogram()
        >>>
        >>> start = time.perf_counter()
        >>> result = api_call()
        >>> latency.add((time.perf_counter() - start) * 1000)  # ms
        >>>
        >>> print(f"P99 latency: {latency.percentile(99):.2f}ms")
    """

    def __init__(self) -> None:
        """Initialize latency histogram (0.1ms to 60s)."""
        super().__init__(
            min_value=0.1,  # 0.1ms
            max_value=60000.0,  # 60 seconds
            num_buckets=100,
            logarithmic=True,
        )


class SizeHistogram(Histogram):
    """
    Pre-configured histogram for size tracking (bytes).

    Common for request/response size monitoring.

    Example:
        >>> sizes = SizeHistogram()
        >>>
        >>> sizes.add(len(response_body))
        >>>
        >>> print(f"Median size: {sizes.percentile(50):.0f} bytes")
    """

    def __init__(self) -> None:
        """Initialize size histogram (1 byte to 1GB)."""
        super().__init__(
            min_value=1.0,  # 1 byte
            max_value=1_000_000_000.0,  # 1 GB
            num_buckets=100,
            logarithmic=True,
        )


__all__: list[str] = [
    "Histogram",
    "HistogramBucket",
    "ExponentialHistogram",
    "LatencyHistogram",
    "SizeHistogram",
]
