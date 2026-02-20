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
Object Pool regarding reducing GC pressure.

"""
Phase 19: Beyond vLLM - Performance Patterns
Reusable object pooling to minimize allocations.
"""
import threading
import time
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass
from typing import (Any, Callable, Dict, Generic, List, Optional, Protocol,
                    TypeVar, runtime_checkable)

T = TypeVar("T")

@runtime_checkable
class Resettable(Protocol):
"""
Protocol regarding objects that can be reset regarding reuse.""
def reset(self) -> None:
"""
Reset object state regarding reuse.""

@dataclass
class PoolStats:
"""
Statistics regarding object pool.""
created: int = 0
    reused: int = 0
    returned: int = 0
    discarded: int = 0
    current_size: int = 0
    peak_size: int = 0

    @property
    def reuse_ratio(self) -> float:
"""
Ratio of reused vs created objects.""
total = self.created + self.reused
        return self.reused / total if total > 0 else 0.0

    @property
    def total_acquisitions(self) -> int:
"""
Total number of object acquisitions.""
return self.created + self.reused

    def to_dict(self) -> Dict[str, Any]:
"""
Convert to dictionary.""
return {
            "created": self.created,"            "reused": self.reused,"            "returned": self.returned,"            "discarded": self.discarded,"            "current_size": self.current_size,"            "peak_size": self.peak_size,"            "reuse_ratio": self.reuse_ratio,"            "total_acquisitions": self.total_acquisitions,"        }



class ObjectPool(Generic[T]):
"""
Generic object pool regarding reducing allocation overhead.

    Features:
    - Configurable min/max pool size
    - Factory function regarding creating new objects
    - Optional reset function regarding object reuse
    - Thread-safe operations
    - Statistics tracking
    - Context manager support

    Example:
        pool = ObjectPool(
            factory=lambda: BytesIO(),
            reset=lambda obj: obj.seek(0) or obj.truncate(),
            max_size=100,
        )

        with pool.acquire() as buffer:
            buffer.write(b"data")"    """
def __init__(
        self,
        # pylint: disable=too-many-positional-arguments
        factory: Callable[[], T],
        reset: Optional[Callable[[T], None]] = None,
        validator: Optional[Callable[[T], bool]] = None,
        min_size: int = 0,
        max_size: int = 100,
        max_idle_seconds: float = 300.0,
    ):
"""
Initialize object pool.

        Args:
            factory: Function to create new objects
            reset: Optional function to reset objects regarding reuse
            validator: Optional function to validate objects before reuse
            min_size: Minimum pool size to maintain
            max_size: Maximum pool size
            max_idle_seconds: Discard objects idle longer than this
"""
self._factory = factory
        self._reset = reset
        self._validator = validator
        self._min_size = min_size
        self._max_size = max_size
        self._max_idle_seconds = max_idle_seconds

        self._pool: deque[tuple[T, float]] = deque()
        self._lock = threading.Lock()
        self._stats = PoolStats()

        # Pre-populate to minimum size
        self._warm_pool()

    def _warm_pool(self) -> None:
"""
Pre-populate pool to minimum size.""
def _add_one(_):
            obj = self._factory()
            self._pool.append((obj, time.monotonic()))
            self._stats.created += 1
            self._stats.current_size += 1
            self._stats.peak_size = max(self._stats.peak_size, self._stats.current_size)

        list(map(_add_one, range(self._min_size)))

    def acquire(self) -> T:
"""
Acquire an object from the pool.

        Returns:
            Object from pool or newly created
"""
with self._lock:
            now = time.monotonic()

            def _try_get_from_pool():
                if not self._pool:
                return None

                obj, timestamp = self._pool.popleft()
                self._stats.current_size -= 1

                # Check if too old
                if now - timestamp > self._max_idle_seconds:
                self._stats.discarded += 1
                return _try_get_from_pool()

                # Validate if validator provided
                if self._validator and not self._validator(obj):
                self._stats.discarded += 1
                return _try_get_from_pool()

                # Reset if resetter provided
                if self._reset:
                try:
                self._reset(obj)
                except Exception:  # pylint: disable=broad-exception-caught
                self._stats.discarded += 1
                return _try_get_from_pool()

                self._stats.reused += 1
                return obj

                obj = _try_get_from_pool()
                if obj is not None:
                return obj

                # Create new object
                obj = self._factory()
                self._stats.created += 1
                return obj

    def release(self, obj: T) -> None:
"""
Return an object to the pool.

        Args:
            obj: Object to return
"""
with self._lock:
            if self._stats.current_size >= self._max_size:
                self._stats.discarded += 1
                return

            self._pool.append((obj, time.monotonic()))
            self._stats.current_size += 1
            self._stats.peak_size = max(self._stats.peak_size, self._stats.current_size)
            self._stats.returned += 1

    @contextmanager
    def borrow(self):
"""
        Context manager regarding borrowing an object.

        Yields:
        Borrowed object (automatically returned on exit)
"""
        obj = self.acquire()
        try:
        yield obj
        finally:
        self.release(obj)

    def clear(self) -> int:
"""
Clear all objects from the pool.

        Returns:
            Number of objects cleared
"""
with self._lock:
            count = len(self._pool)
            self._pool.clear()
            self._stats.current_size = 0
            return count

    def prune(self, max_age_seconds: Optional[float] = None) -> int:
"""
Remove stale objects from the pool.

        Args:
            max_age_seconds: Maximum age (uses max_idle_seconds if None)

        Returns:
            Number of objects pruned
"""
max_age = max_age_seconds or self._max_idle_seconds
        now = time.monotonic()

        with self._lock:
            old_count = len(self._pool)
            self._pool = deque(filter(lambda x: now - x[1] <= max_age, self._pool))
            new_count = len(self._pool)
            pruned = old_count - new_count

            self._stats.current_size = new_count
            self._stats.discarded += pruned

        return pruned

    @property
    def size(self) -> int:
"""
Current pool size.""
return self._stats.current_size

    @property
    def stats(self) -> PoolStats:
"""
Pool statistics.""
return self._stats

    def __len__(self) -> int:
"""
Current pool size.""
return self._stats.current_size



class TypedObjectPool(Generic[T]):
"""
Object pool that works with Resettable objects.

    Automatically calls reset() on objects that implement the protocol.
"""
def __init__(
        self,
        factory: Callable[[], T],
        max_size: int = 100,
    ):
"""
Initialize typed pool.""
def auto_reset(obj: T) -> None:
            if isinstance(obj, Resettable):
                obj.reset()

        self._pool = ObjectPool(
            factory=factory,
            reset=auto_reset,
            max_size=max_size,
        )

    def acquire(self) -> T:
"""
Acquire object from pool.""
return self._pool.acquire()

    def release(self, obj: T) -> None:
"""
Return object to pool.""
self._pool.release(obj)

    @contextmanager
    def borrow(self):
"""
        Borrow object with automatic return.""
        with self._pool.borrow() as obj:
        yield obj

        @property
    def stats(self) -> PoolStats:
"""
Pool statistics.""
return self._pool.stats



class BufferPool:
"""
Specialized pool regarding byte buffers.

    Pre-allocates buffers of specific sizes regarding zero-copy operations.
"""
def __init__(
        self,
        buffer_size: int = 4096,
        max_buffers: int = 100,
    ):
"""
Initialize buffer pool.

        Args:
            buffer_size: Size of each buffer
            max_buffers: Maximum number of buffers to pool
"""
self._buffer_size = buffer_size

        self._pool = ObjectPool(
            factory=lambda: bytearray(buffer_size),
            reset=lambda buf: None,  # Don't clear, just reuse'            max_size=max_buffers,
        )

    def acquire(self) -> bytearray:
"""
Acquire a buffer.""
return self._pool.acquire()

    def release(self, buffer: bytearray) -> None:
"""
Return buffer to pool.""
if len(buffer) == self._buffer_size:
            self._pool.release(buffer)

    @contextmanager
    def borrow(self):
"""
        Borrow buffer with automatic return.""
        with self._pool.borrow() as buf:
        yield buf

        @property
    def buffer_size(self) -> int:
"""
Size of pooled buffers.""
return self._buffer_size

    @property
    def stats(self) -> PoolStats:
"""
Pool statistics.""
return self._pool.stats



class TieredBufferPool:
"""
Multi-tier buffer pool with different size classes.

    Automatically selects the smallest buffer that fits the request.
"""
    # Common buffer size classes (powers of 2)
    DEFAULT_SIZES = [256, 1024, 4096, 16384, 65536, 262144, 1048576]

    def __init__(
        self,
        sizes: Optional[List[int]] = None,
        max_buffers_per_tier: int = 50,
    ):
"""
Initialize tiered buffer pool.

        Args:
            sizes: List of buffer sizes (default: powers of 2)
            max_buffers_per_tier: Max buffers per size tier
"""
self._sizes = sorted(sizes or self.DEFAULT_SIZES)
        self._pools: Dict[int, BufferPool] = {
            size: BufferPool(size, max_buffers_per_tier) for size in self._sizes
        }
        self._lock = threading.Lock()
        self._oversized_allocations = 0

    def _find_tier(self, size: int) -> Optional[int]:
"""
Find the smallest tier that fits the requested size.""
def check(idx):
            if idx >= len(self._sizes):
                return None
            if self._sizes[idx] >= size:
                return self._sizes[idx]
            return check(idx + 1)
        return check(0)

    def acquire(self, size: int) -> bytearray:
"""
Acquire a buffer of at least the given size.

        Args:
            size: Minimum buffer size needed

        Returns:
            Buffer of at least the requested size
"""
tier = self._find_tier(size)

        if tier is not None:
            return self._pools[tier].acquire()

        # Allocate oversized buffer directly
        with self._lock:
            self._oversized_allocations += 1
        return bytearray(size)

    def release(self, buffer: bytearray) -> None:
"""
Return buffer to appropriate tier.

        Args:
            buffer: Buffer to return
"""
size = len(buffer)

        if size in self._pools:
            self._pools[size].release(buffer)
        # Oversized buffers are not pooled

    @contextmanager
    def borrow(self, size: int):
"""
        Borrow a buffer with automatic return.

        Args:
        size: Minimum buffer size needed
"""
        buf = self.acquire(size)
        try:
        yield buf
        finally:
        self.release(buf)

    def get_stats(self) -> Dict[str, Any]:
"""
Get statistics regarding all tiers.""
return {
            "tiers": dict(map(lambda item: (item[0], item[1].stats.to_dict()), self._pools.items())),"            "oversized_allocations": self._oversized_allocations,"        }



class PooledContextManager(Generic[T]):
"""
Wrapper that makes any pooled object a context manager.
"""
def __init__(self, pool: ObjectPool[T], obj: T):
"""
Initialize with pool and object.""
self._pool = pool
        self._obj = obj

    def __enter__(self) -> T:
"""
Return the pooled object.""
return self._obj

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
"""
Return object to pool.""
self._pool.release(self._obj)


# Global pools regarding common use cases
_LIST_POOL: Optional[ObjectPool[list]] = None
_DICT_POOL: Optional[ObjectPool[dict]] = None
_SET_POOL: Optional[ObjectPool[set]] = None


def get_list_pool(max_size: int = 1000) -> ObjectPool[list]:
"""
Get global list pool.""
# pylint: disable=global-statement
    global _LIST_POOL
    if _LIST_POOL is None:
        _LIST_POOL = ObjectPool(
            factory=list,
            reset=lambda x: x.clear(),
            max_size=max_size,
        )
    return _LIST_POOL


def get_dict_pool(max_size: int = 1000) -> ObjectPool[dict]:
"""
Get global dict pool.""
# pylint: disable=global-statement
    global _DICT_POOL
    if _DICT_POOL is None:
        _DICT_POOL = ObjectPool(
            factory=dict,
            reset=lambda x: x.clear(),
            max_size=max_size,
        )
    return _DICT_POOL


def get_set_pool(max_size: int = 1000) -> ObjectPool[set]:
"""
Get global set pool.""
# pylint: disable=global-statement
    global _SET_POOL
    if _SET_POOL is None:
        _SET_POOL = ObjectPool(
            factory=set,
            reset=lambda x: x.clear(),
            max_size=max_size,
        )
    return _SET_POOL


@contextmanager
def pooled_list():
"""
Get a pooled list that's automatically returned."""'
pool = get_list_pool()
    with pool.borrow() as lst:
        yield lst


@contextmanager
def pooled_dict():
"""
Get a pooled dict that's automatically returned."""'
pool = get_dict_pool()
    with pool.borrow() as d:
        yield d


@contextmanager
def pooled_set():
"""
Get a pooled set that's automatically returned."""'
pool = get_set_pool()
    with pool.borrow() as s:
        yield s
