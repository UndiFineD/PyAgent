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

"""CudaStreamPool - CUDA stream and event management with pooling.

This module provides efficient stream and event pooling for GPU operations,
enabling better overlap of compute and communication.

Inspired by vLLM's stream management, but extends with:
- Priority stream hints for latency-critical operations
- Automatic cleanup on pool destruction
- Stream affinity for related operations
- Event recycling to reduce allocation overhead

Example:
    >>> pool = CudaStreamPool(compute_streams=4, comm_streams=2)
    >>> with pool.acquire_compute() as stream:
    ...     result = model(input, stream=stream)
    >>> pool.sync_all()
"""

from __future__ import annotations

import threading
import time
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Iterator, Optional

# Try to import torch for GPU operations
try:
    import torch

    HAS_TORCH = True
    HAS_CUDA = torch.cuda.is_available()
except ImportError:
    HAS_TORCH = False
    HAS_CUDA = False
    torch = None  # type: ignore

# Try to import Rust accelerations
try:
    from src.core.rust_bridge import get_bridge

    _BRIDGE = get_bridge()
    HAS_RUST = hasattr(_BRIDGE, "event_query_rust")
except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
    HAS_RUST = False
    _BRIDGE = None


class StreamPriority(Enum):
    """Priority level for CUDA streams."""

    LOW = auto()  # Background operations
    NORMAL = auto()  # Default priority
    HIGH = auto()  # Latency-critical operations


class StreamState(Enum):
    """State of a pooled stream."""

    FREE = auto()  # Available for use
    ACQUIRED = auto()  # In use
    BUSY = auto()  # Has pending operations


@dataclass
class StreamStats:
    """Statistics for a stream."""

    acquisitions: int = 0
    total_active_time_ns: int = 0
    events_recorded: int = 0
    syncs: int = 0
    last_used: float = 0.0

    @property
    def avg_active_time_ms(self) -> float:
        """Average active time in milliseconds."""
        if self.acquisitions == 0:
            return 0.0
        return (self.total_active_time_ns / self.acquisitions) / 1_000_000


@dataclass
class PooledStream:
    """A CUDA stream managed by a pool.

    Attributes:
        stream_id: Unique identifier
        priority: Stream priority
        state: Current state
        stream: Underlying CUDA stream
    """

    stream_id: int
    priority: StreamPriority = StreamPriority.NORMAL
    state: StreamState = StreamState.FREE
    stream: Any = None
    stats: StreamStats = field(default_factory=StreamStats)
    affinity_key: Optional[str] = None

    acquired_at: float = field(default=0.0, repr=False)

    def __post_init__(self) -> None:
        """Initialize stream if not provided."""
        if self.stream is None and HAS_CUDA:
            priority = self._get_cuda_priority()
            self.stream = torch.cuda.Stream(priority=priority)

    def _get_cuda_priority(self) -> int:
        """Convert priority enum to CUDA priority."""
        if self.priority == StreamPriority.HIGH:
            return -1  # High priority in CUDA
        if self.priority == StreamPriority.LOW:
            return 1  # Low priority
        return 0  # Normal

    def synchronize(self) -> None:
        """Wait for all operations to complete."""
        if self.stream is not None:
            self.stream.synchronize()
            self.stats.syncs += 1

    def query(self) -> bool:
        """Check if all operations are complete (non-blocking).

        Returns:
            True if stream is idle, False if busy
        """
        if self.stream is None:
            return True
        return self.stream.query()

    def wait_event(self, event: Any) -> None:
        """Wait for an event on this stream."""
        if self.stream is not None and event is not None:
            self.stream.wait_event(event)

    @contextmanager
    def context(self) -> Iterator["PooledStream"]:
        """Context manager for stream operations."""
        if self.stream is not None:
            with torch.cuda.stream(self.stream):
                yield self
        else:
            yield self


@dataclass
class PooledEvent:
    """A CUDA event managed by a pool.

    Attributes:
        event_id: Unique identifier
        event: Underlying CUDA event
    """

    event_id: int
    event: Any = None
    in_use: bool = False
    recorded_on: Optional[int] = None  # Stream ID

    def __post_init__(self) -> None:
        """Initialize event if not provided."""
        if self.event is None and HAS_CUDA:
            self.event = torch.cuda.Event()

    def record(self, stream: Optional[Any] = None) -> None:
        """Record event on stream."""
        if self.event is not None:
            self.event.record(stream)

    def synchronize(self) -> None:
        """Wait for event to complete."""
        if self.event is not None:
            self.event.synchronize()

    def query(self) -> bool:
        """Check if event is complete (non-blocking)."""
        if self.event is None:
            return True
        return self.event.query()

    def elapsed_time(self, end_event: "PooledEvent") -> float:
        """Get elapsed time between events in milliseconds."""
        if self.event is None or end_event.event is None:
            return 0.0
        return self.event.elapsed_time(end_event.event)


class EventPool:
    """Pool of reusable CUDA events.

    Events are expensive to create, so pooling them improves performance.
    """

    def __init__(self, initial_size: int = 16, max_size: int = 256) -> None:
        """Initialize event pool.

        Args:
            initial_size: Initial number of events
            max_size: Maximum pool size
        """
        self.max_size = max_size
        self._events: list[PooledEvent] = []
        self._free: deque[PooledEvent] = deque()
        self._lock = threading.Lock()
        self._next_id = 0

        # Pre-allocate events
        for _ in range(initial_size):
            self._create_event()

    def _create_event(self) -> PooledEvent:
        """Create a new event."""
        event = PooledEvent(event_id=self._next_id)
        self._next_id += 1
        self._events.append(event)
        self._free.append(event)
        return event

    def acquire(self) -> Optional[PooledEvent]:
        """Acquire an event from the pool.

        Returns:
            PooledEvent or None if pool exhausted
        """
        with self._lock:
            if self._free:
                event = self._free.popleft()
                event.in_use = True
                return event

            # Create new event if under limit
            if len(self._events) < self.max_size:
                event = self._create_event()
                self._free.popleft()  # Remove from free list
                event.in_use = True
                return event

            return None

    def release(self, event: PooledEvent) -> None:
        """Release an event back to the pool."""
        with self._lock:
            event.in_use = False
            event.recorded_on = None
            self._free.append(event)

    @contextmanager
    def event_context(self) -> Iterator[Optional[PooledEvent]]:
        """Context manager for event acquisition."""
        event = self.acquire()
        try:
            yield event
        finally:
            if event is not None:
                self.release(event)

    def clear(self) -> None:
        """Reset pool state."""
        with self._lock:
            for event in self._events:
                event.in_use = False
            self._free = deque(self._events)


class CudaStreamPool:
    """Pool of CUDA streams for compute and communication.

    This pool manages separate stream pools for different operation
    types, enabling efficient overlap of compute with data transfers.

    Attributes:
        compute_streams: Number of compute streams
        comm_streams: Number of communication streams
    """

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        compute_streams: int = 4,
        comm_streams: int = 2,
        high_priority_streams: int = 1,
        event_pool_size: int = 32,
        enable_affinity: bool = True,
    ) -> None:
        """Initialize stream pool.

        Args:
            compute_streams: Number of compute streams
            comm_streams: Number of communication streams
            high_priority_streams: Number of high-priority streams
            event_pool_size: Size of event pool
            enable_affinity: Enable stream affinity tracking
        """
        self.compute_streams_count = compute_streams
        self.comm_streams_count = comm_streams
        self.high_priority_count = high_priority_streams
        self.enable_affinity = enable_affinity

        self._compute_streams: list[PooledStream] = []
        self._comm_streams: list[PooledStream] = []
        self._high_priority_streams: list[PooledStream] = []

        self._free_compute: deque[PooledStream] = deque()
        self._free_comm: deque[PooledStream] = deque()
        self._free_high: deque[PooledStream] = deque()

        self._affinity_map: dict[str, PooledStream] = {}
        self._lock = threading.Lock()
        self._next_id = 0

        # Event pool
        self._event_pool = EventPool(event_pool_size)

        # Initialize streams
        self._initialize_pools()

    def _initialize_pools(self) -> None:
        """Create stream pools."""
        # Compute streams
        for _ in range(self.compute_streams_count):
            stream = PooledStream(
                stream_id=self._next_id,
                priority=StreamPriority.NORMAL,
            )
            self._next_id += 1
            self._compute_streams.append(stream)
            self._free_compute.append(stream)

        # Communication streams
        for _ in range(self.comm_streams_count):
            stream = PooledStream(
                stream_id=self._next_id,
                priority=StreamPriority.NORMAL,
            )
            self._next_id += 1
            self._comm_streams.append(stream)
            self._free_comm.append(stream)

        # High priority streams
        for _ in range(self.high_priority_count):
            stream = PooledStream(
                stream_id=self._next_id,
                priority=StreamPriority.HIGH,
            )
            self._next_id += 1
            self._high_priority_streams.append(stream)
            self._free_high.append(stream)

    def acquire_compute(
        self,
        affinity_key: Optional[str] = None,
        blocking: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[PooledStream]:
        """Acquire a compute stream.

        Args:
            affinity_key: Key for stream affinity
            blocking: Whether to wait for available stream
            timeout: Maximum wait time

        Returns:
            PooledStream or None
        """
        return self._acquire_from_pool(
            self._free_compute,
            affinity_key,
            blocking,
            timeout,
        )

    def acquire_comm(
        self,
        affinity_key: Optional[str] = None,
        blocking: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[PooledStream]:
        """Acquire a communication stream."""
        return self._acquire_from_pool(
            self._free_comm,
            affinity_key,
            blocking,
            timeout,
        )

    def acquire_high_priority(
        self,
        blocking: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[PooledStream]:
        """Acquire a high-priority stream."""
        return self._acquire_from_pool(
            self._free_high,
            None,
            blocking,
            timeout,
        )

    def _acquire_from_pool(
        self,
        pool: deque[PooledStream],
        affinity_key: Optional[str],
        blocking: bool,
        timeout: Optional[float],
    ) -> Optional[PooledStream]:
        """Acquire stream from a specific pool."""
        start = time.time()

        while True:
            with self._lock:
                # Check affinity first
                if affinity_key and self.enable_affinity:
                    if affinity_key in self._affinity_map:
                        stream = self._affinity_map[affinity_key]
                        if stream.state == StreamState.FREE and stream in pool:
                            return self._mark_acquired(stream, pool, affinity_key)

                # Get from free pool
                if pool:
                    stream = pool.popleft()
                    return self._mark_acquired(stream, pool, affinity_key)

            if not blocking:
                return None

            if timeout and (time.time() - start) >= timeout:
                return None

            # Avoid blocking event loop; use threading.Event().wait for better async compatibility
            threading.Event().wait(0.001)

    def _mark_acquired(
        self,
        stream: PooledStream,
        pool: deque[PooledStream],
        affinity_key: Optional[str],
    ) -> PooledStream:
        """Mark stream as acquired."""
        stream.state = StreamState.ACQUIRED
        stream.acquired_at = time.perf_counter_ns()
        stream.stats.acquisitions += 1
        stream.stats.last_used = time.time()

        if affinity_key and self.enable_affinity:
            stream.affinity_key = affinity_key
            self._affinity_map[affinity_key] = stream

        # Remove from free pool if present
        try:
            pool.remove(stream)
        except ValueError:
            pass

        return stream

    def release(self, stream: PooledStream) -> None:
        """Release a stream back to its pool.

        Args:
            stream: Stream to release
        """
        with self._lock:
            # Record timing
            elapsed = time.perf_counter_ns() - stream.acquired_at
            stream.stats.total_active_time_ns += elapsed
            stream.state = StreamState.FREE

            # Return to appropriate pool
            if stream in self._compute_streams:
                self._free_compute.append(stream)
            elif stream in self._comm_streams:
                self._free_comm.append(stream)
            elif stream in self._high_priority_streams:
                self._free_high.append(stream)

    @contextmanager
    def compute_context(self, affinity_key: Optional[str] = None) -> Iterator[Optional[PooledStream]]:
        """Context manager for compute stream."""
        stream = self.acquire_compute(affinity_key)
        if stream is None:
            yield None
            return

        try:
            with stream.context():
                yield stream
        finally:
            self.release(stream)

    @contextmanager
    def comm_context(self, affinity_key: Optional[str] = None) -> Iterator[Optional[PooledStream]]:
        """Context manager for communication stream."""
        stream = self.acquire_comm(affinity_key)
        if stream is None:
            yield None
            return

        try:
            with stream.context():
                yield stream
        finally:
            self.release(stream)

    @contextmanager
    def high_priority_context(self) -> Iterator[Optional[PooledStream]]:
        """Context manager for high-priority stream."""
        stream = self.acquire_high_priority()
        if stream is None:
            yield None
            return

        try:
            with stream.context():
                yield stream
        finally:
            self.release(stream)

    def acquire_event(self) -> Optional[PooledEvent]:
        """Acquire an event from the pool."""
        return self._event_pool.acquire()

    def release_event(self, event: PooledEvent) -> None:
        """Release an event back to the pool."""
        self._event_pool.release(event)

    @contextmanager
    def event_context(self) -> Iterator[Optional[PooledEvent]]:
        """Context manager for event acquisition."""
        with self._event_pool.event_context() as event:
            yield event

    def sync_all(self) -> None:
        """Synchronize all streams."""
        all_streams = self._compute_streams + self._comm_streams + self._high_priority_streams
        for stream in all_streams:
            stream.synchronize()

    def sync_compute(self) -> None:
        """Synchronize all compute streams."""
        for stream in self._compute_streams:
            stream.synchronize()

    def sync_comm(self) -> None:
        """Synchronize all communication streams."""
        for stream in self._comm_streams:
            stream.synchronize()

    def clear_affinity(self) -> None:
        """Clear all stream affinities."""
        with self._lock:
            self._affinity_map.clear()
            for stream in self._compute_streams + self._comm_streams:
                stream.affinity_key = None

    @property
    def stats(self) -> dict[str, Any]:
        """Get pool statistics."""
        with self._lock:

            def pool_stats(streams: list[PooledStream]) -> dict[str, Any]:
                total_acq = sum(s.stats.acquisitions for s in streams)
                total_time = sum(s.stats.total_active_time_ns for s in streams)
                return {
                    "count": len(streams),
                    "total_acquisitions": total_acq,
                    "total_active_time_ms": total_time / 1_000_000,
                    "avg_active_time_ms": (total_time / total_acq / 1_000_000) if total_acq > 0 else 0,
                }

            return {
                "compute": pool_stats(self._compute_streams),
                "comm": pool_stats(self._comm_streams),
                "high_priority": pool_stats(self._high_priority_streams),
                "free_compute": len(self._free_compute),
                "free_comm": len(self._free_comm),
                "free_high": len(self._free_high),
                "affinity_keys": len(self._affinity_map),
            }


# Global pool instance
_GLOBAL_POOL: Optional[CudaStreamPool] = None
_global_lock = threading.Lock()


def get_global_stream_pool(
    compute_streams: int = 4,
    comm_streams: int = 2,
) -> CudaStreamPool:
    """Get or create global stream pool.

    Args:
        compute_streams: Number of compute streams (only used on creation)
        comm_streams: Number of comm streams (only used on creation)

    Returns:
        Global CudaStreamPool instance
    """
    global _GLOBAL_POOL  # pylint: disable=global-statement

    with _global_lock:
        if _GLOBAL_POOL is None:
            _GLOBAL_POOL = CudaStreamPool(
                compute_streams=compute_streams,
                comm_streams=comm_streams,
            )
        return _GLOBAL_POOL


def reset_global_pool() -> None:
    """Reset the global stream pool."""
    global _GLOBAL_POOL  # pylint: disable=global-statement

    with _global_lock:
        if _GLOBAL_POOL is not None:
            _GLOBAL_POOL.sync_all()
        _GLOBAL_POOL = None


# Convenience functions
@contextmanager
def compute_stream(affinity_key: Optional[str] = None) -> Iterator[Optional[PooledStream]]:
    """Get a compute stream from the global pool."""
    pool = get_global_stream_pool()
    with pool.compute_context(affinity_key) as stream:
        yield stream


@contextmanager
def comm_stream(affinity_key: Optional[str] = None) -> Iterator[Optional[PooledStream]]:
    """Get a communication stream from the global pool."""
    pool = get_global_stream_pool()
    with pool.comm_context(affinity_key) as stream:
        yield stream


@contextmanager
def high_priority_stream() -> Iterator[Optional[PooledStream]]:
    """Get a high-priority stream from the global pool."""
    pool = get_global_stream_pool()
    with pool.high_priority_context() as stream:
        yield stream
