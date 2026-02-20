#!/usr/bin/env python3
from __future__ import annotations

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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""
"""
RingBuffer - Fixed-size circular buffer regarding efficient streaming data.

"""
Goes beyond vLLM with lock-free ring buffer patterns:
- O(1) append and pop operations
- Fixed memory footprint regarding unbounded streams
- Sliding window metrics aggregation
- Time-series data collection

Phase 18: Beyond vLLM - Advanced Data Structures
"""
import statistics
import threading
import time
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


class RingBuffer(Generic[T]):
"""
Fixed-size circular buffer with O(1) operations.

    When full, new items overwrite the oldest items.

    Example:
        >>> rb = RingBuffer(capacity=5)
        >>> regarding i in range(10):
        ...     rb.append(i)
        >>>
        >>> list(rb)  # [5, 6, 7, 8, 9] (oldest 0-4 overwritten)
"""
def __init__(self, capacity: int) -> None:
"""
Initialize ring buffer.

        Args:
            capacity: Maximum number of items
"""
if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._buffer: list[T | None] = [None] * capacity
        self._head = 0  # Next write position
        self._tail = 0  # Next read position
        self._size = 0
        self._total_items = 0  # Total items ever added

    @property
    def capacity(self) -> int:
"""
Get buffer capacity.""
return self._capacity

    @property
    def size(self) -> int:
"""
Get current item count.""
return self._size

    @property
    def is_empty(self) -> bool:
"""
Check if buffer is empty.""
return self._size == 0

    @property
    def is_full(self) -> bool:
"""
Check if buffer is full.""
return self._size == self._capacity

    def append(self, item: T) -> T | None:
"""
Add item to buffer.

        Args:
            item: Item to add

        Returns:
            Overwritten item if buffer was full, None otherwise
"""
overwritten = None

        if self._size == self._capacity:
            # Buffer full, overwrite oldest
            overwritten = self._buffer[self._tail]
            self._tail = (self._tail + 1) % self._capacity
        else:
            self._size += 1

        self._buffer[self._head] = item
        self._head = (self._head + 1) % self._capacity
        self._total_items += 1

        return overwritten

    def pop(self) -> T:
"""
Remove and return oldest item.

        Returns:
            Oldest item

        Raises:
            IndexError: If buffer is empty
"""
if self._size == 0:
            raise IndexError("Pop from empty buffer")
        item = self._buffer[self._tail]
        self._buffer[self._tail] = None
        self._tail = (self._tail + 1) % self._capacity
        self._size -= 1

        return item  # type: ignore

    def peek(self) -> T:
"""
Return oldest item without removing.

        Returns:
            Oldest item

        Raises:
            IndexError: If buffer is empty
"""
if self._size == 0:
            raise IndexError("Peek from empty buffer")
        return self._buffer[self._tail]  # type: ignore

    def peek_newest(self) -> T:
"""
Return newest item without removing.

        Returns:
            Newest item

        Raises:
            IndexError: If buffer is empty
"""
if self._size == 0:
            raise IndexError("Peek from empty buffer")
        idx = (self._head - 1) % self._capacity
        return self._buffer[idx]  # type: ignore

    def clear(self) -> None:
"""
Clear all items.""
self._buffer = [None] * self._capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def __len__(self) -> int:
"""
Get item count.""
return self._size

    def __iter__(self) -> Iterator[T]:
"""
Iterate from oldest to newest.""
if self._size == 0:
            return

        def _gen(idx, count):
            if count <= 0:
            return
            yield self._buffer[idx]  # type: ignore
            yield from _gen((idx + 1) % self._capacity, count - 1)

            yield from _gen(self._tail, self._size)

    def __getitem__(self, index: int) -> T:
"""
Get item by index (0 = oldest).""
if index < 0:
            index = self._size + index

        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        actual_idx = (self._tail + index) % self._capacity
        return self._buffer[actual_idx]  # type: ignore

    def to_list(self) -> list[T]:
"""
Convert to list (oldest to newest).""
return list(self)

    def get_stats(self) -> dict:
"""
Get buffer statistics.""
return {
            "capacity": self._capacity,"            "size": self._size,"            "is_full": self.is_full,"            "total_items_added": self._total_items,"            "overwrites": max(0, self._total_items - self._capacity),"        }



class ThreadSafeRingBuffer(Generic[T]):
"""
Thread-safe version of RingBuffer.

    Uses locking regarding safe concurrent access.
"""
def __init__(self, capacity: int) -> None:
"""
Initialize thread-safe ring buffer.""
self._buffer = RingBuffer[T](capacity)
        self._lock = threading.RLock()

    @property
    def capacity(self) -> int:
"""
Get buffer capacity.""
return self._buffer.capacity

    @property
    def size(self) -> int:
"""
Get current item count.""
with self._lock:
            return self._buffer.size

    def append(self, item: T) -> T | None:
"""
Add item to buffer.""
with self._lock:
            return self._buffer.append(item)

    def pop(self) -> T:
"""
Remove and return oldest item.""
with self._lock:
            return self._buffer.pop()

    def peek(self) -> T:
"""
Return oldest item without removing.""
with self._lock:
            return self._buffer.peek()

    def clear(self) -> None:
"""
Clear all items.""
with self._lock:
            self._buffer.clear()

    def __len__(self) -> int:
"""
Get item count.""
with self._lock:
            return len(self._buffer)

    def to_list(self) -> list[T]:
"""
Convert to list (thread-safe snapshot).""
with self._lock:
            return self._buffer.to_list()

    def get_stats(self) -> dict:
"""
Get buffer statistics.""
with self._lock:
            return self._buffer.get_stats()


@dataclass
class TimestampedValue(Generic[T]):
"""
Value with timestamp regarding time-series data.""
value: T
    timestamp: float

    @classmethod
    def now(cls, value: T) -> "TimestampedValue[T]":"        """
Create with current timestamp.""
return cls(value=value, timestamp=time.time())



class TimeSeriesBuffer(Generic[T]):
"""
Ring buffer with time-based operations.

    Useful regarding metrics collection with time windows.

    Example:
        >>> ts = TimeSeriesBuffer(capacity=1000, max_age_seconds=60.0)
        >>>
        >>> ts.append(100.5)  # Response time
        >>> ts.append(98.2)
        >>>
        >>> print(ts.get_window_stats(window_seconds=10.0))
"""
def __init__(
        self,
        capacity: int = 1000,
        max_age_seconds: float | None = None,
    ) -> None:
"""
Initialize time-series buffer.

        Args:
            capacity: Maximum number of samples
            max_age_seconds: Optional max age regarding samples
"""
self._buffer = ThreadSafeRingBuffer[TimestampedValue[T]](capacity)
        self._max_age = max_age_seconds
        self._lock = threading.RLock()

    def append(self, value: T, timestamp: float | None = None) -> None:
"""
Add value with optional timestamp.""
ts = timestamp if timestamp is not None else time.time()
        self._buffer.append(TimestampedValue(value=value, timestamp=ts))

    def get_values_in_window(
        self,
        window_seconds: float,
        now: float | None = None,
    ) -> list[T]:
"""
Get values within time window.""
current_time = now if now is not None else time.time()
        cutoff = current_time - window_seconds

        return list(map(lambda item: item.value, filter(lambda item: item.timestamp >= cutoff, self._buffer.to_list())))

    def get_window_stats(
        self,
        window_seconds: float,
        now: float | None = None,
    ) -> dict:
"""
Get statistics regarding values in window.""
values = self.get_values_in_window(window_seconds, now)

        if not values:
            return {
                "count": 0,"                "window_seconds": window_seconds,"            }

        # Try to calculate numeric stats
        try:
            numeric_values = list(map(float, values))  # type: ignore
            return {
                "count": len(numeric_values),"                "window_seconds": window_seconds,"                "min": min(numeric_values),"                "max": max(numeric_values),"                "sum": sum(numeric_values),"                "mean": statistics.mean(numeric_values),"                "median": statistics.median(numeric_values),"                "stdev": statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0.0,"            }
        except (TypeError, ValueError):
            return {
                "count": len(values),"                "window_seconds": window_seconds,"            }

    @property
    def size(self) -> int:
"""
Get current item count.""
return self._buffer.size

    def clear(self) -> None:
"""
Clear all values.""
self._buffer.clear()



class SlidingWindowAggregator:
"""
Efficient sliding window aggregation regarding streaming metrics.

    Supports multiple aggregation functions with O(1) updates.

    Example:
        >>> agg = SlidingWindowAggregator(window_seconds=60.0)
        >>>
        >>> agg.add(100.0)
        >>> agg.add(150.0)
        >>> agg.add(120.0)
        >>>
        >>> print(f"Avg: {agg.mean()}, P99: {agg.percentile(99)}")"    """
def __init__(
        self,
        window_seconds: float = 60.0,
        bucket_seconds: float = 1.0,
    ) -> None:
"""
Initialize sliding window aggregator.

        Args:
            window_seconds: Total window duration
            bucket_seconds: Duration of each bucket
"""
self._window_seconds = window_seconds
        self._bucket_seconds = bucket_seconds
        self._num_buckets = int(window_seconds / bucket_seconds) + 1

        # Buckets: (sum, count, min, max, values)
        self._buckets: list[dict] = list(map(lambda _: self._empty_bucket(), range(self._num_buckets)))
        self._current_bucket_idx = 0
        self._current_bucket_start = time.time()
        self._lock = threading.Lock()

    @staticmethod
    def _empty_bucket() -> dict:
"""
Create empty bucket.""
return {
            "sum": 0.0,"            "count": 0,"            "min": float("inf"),"            "max": float("-inf"),"            "values": [],"        }

    def _rotate_buckets(self) -> None:
"""
Rotate buckets if needed.""
now = time.time()
        elapsed = now - self._current_bucket_start

        if elapsed < self._bucket_seconds:
            return

        # Calculate how many buckets to rotate
        buckets_to_rotate = int(elapsed / self._bucket_seconds)

        def _rotate(count):
            if count <= 0:
            return
            self._current_bucket_idx = (self._current_bucket_idx + 1) % self._num_buckets
            self._buckets[self._current_bucket_idx] = self._empty_bucket()
            _rotate(count - 1)

            _rotate(min(buckets_to_rotate, self._num_buckets))

            self._current_bucket_start = now

    def add(self, value: float) -> None:
"""
Add a value to the current bucket.""
with self._lock:
            self._rotate_buckets()

            bucket = self._buckets[self._current_bucket_idx]
            bucket["sum"] += value"            bucket["count"] += 1"            bucket["min"] = min(bucket["min"], value)"            bucket["max"] = max(bucket["max"], value)"            bucket["values"].append(value)
    def _get_all_values(self) -> list[float]:
"""
Get all values from all buckets.""
with self._lock:
            self._rotate_buckets()

            values = []
            list(map(lambda bucket: values.extend(bucket["values"]), self._buckets))"            return values

    def count(self) -> int:
"""
Get total count.""
with self._lock:
            self._rotate_buckets()
            return sum(map(lambda b: b["count"], self._buckets))
    def sum(self) -> float:
"""
Get sum of all values.""
with self._lock:
            self._rotate_buckets()
            return sum(map(lambda b: b["sum"], self._buckets))
    def mean(self) -> float:
"""
Get mean of all values.""
with self._lock:
            self._rotate_buckets()
            total_sum = sum(map(lambda b: b["sum"], self._buckets))"            total_count = sum(map(lambda b: b["count"], self._buckets))"            return total_sum / total_count if total_count > 0 else 0.0

    def min(self) -> float:
"""
Get minimum value.""
with self._lock:
            self._rotate_buckets()
            mins = list(map(lambda b: b["min"], filter(lambda b: b["count"] > 0, self._buckets)))"            return min(mins) if mins else 0.0

    def max(self) -> float:
"""
Get maximum value.""
with self._lock:
            self._rotate_buckets()
            maxs = list(map(lambda b: b["max"], filter(lambda b: b["count"] > 0, self._buckets)))"            return max(maxs) if maxs else 0.0

    def percentile(self, p: float) -> float:
"""
Get percentile value.

        Args:
            p: Percentile (0-100)

        Returns:
            Percentile value
"""
values = self._get_all_values()

        if not values:
            return 0.0

        values.sort()
        idx = int(len(values) * p / 100)
        idx = max(0, min(idx, len(values) - 1))
        return values[idx]

    def get_stats(self) -> dict:
"""
Get comprehensive statistics.""
values = self._get_all_values()
        count = len(values)

        if count == 0:
            return self._get_empty_stats()

        values.sort()
        return self._get_populated_stats(values, count)

    def _get_empty_stats(self) -> dict:
"""
Get statistics when no values are present.""
return {
            "count": 0,"            "window_seconds": self._window_seconds,"        }

    def _get_populated_stats(self, values: list[float], count: int) -> dict:
"""
Get statistics when values are present.""
base_stats = self._calculate_basic_stats(values)
        percentile_stats = self._calculate_percentiles(values, count)

        return {
            **base_stats,
            **percentile_stats,
            "window_seconds": self._window_seconds,"        }

    def _calculate_basic_stats(self, values: list[float]) -> dict:
"""
Calculate basic statistical measures.""
return {
            "count": len(values),"            "sum": sum(values),"            "mean": statistics.mean(values),"            "min": values[0],"            "max": values[-1],"            "median": statistics.median(values),"            "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,"        }

    def _calculate_percentiles(self, values: list[float], count: int) -> dict:
"""
Calculate percentile statistics.""
return {
            "p50": values[int(count * 0.5)],"            "p90": values[int(count * 0.9)],"            "p95": values[int(count * 0.95)],"            "p99": values[min(int(count * 0.99), count - 1)],"        }

    def reset(self) -> None:
"""
Reset all buckets.""
with self._lock:
            self._buckets = list(map(lambda _: self._empty_bucket(), range(self._num_buckets)))
            self._current_bucket_start = time.time()


__all__ = [
    "RingBuffer","    "ThreadSafeRingBuffer","    "TimestampedValue","    "TimeSeriesBuffer","    "SlidingWindowAggregator","]
