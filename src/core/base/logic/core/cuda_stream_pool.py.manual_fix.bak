#!/usr/bin/env python3
"""
Minimal CUDA stream pool stub for tests.

Provides lightweight classes and functions expected by tests without GPU deps.
"""
from __future__ import annotations





try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto

try:
    from typing import Any, Deque, List, Optional
except ImportError:
    from typing import Any, Deque, List, Optional

try:
    from collections import deque
except ImportError:
    from collections import deque



class StreamPriority(Enum):
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()


class StreamState(Enum):
    FREE = auto()
    ACQUIRED = auto()
    BUSY = auto()


@dataclass
class StreamStats:
    acquisitions: int = 0
    total_active_time_ns: int = 0
    events_recorded: int = 0
    syncs: int = 0
    last_used: float = 0.0


@dataclass
class PooledStream:
    stream_id: int
    priority: StreamPriority = StreamPriority.NORMAL
    state: StreamState = StreamState.FREE
    stream: Any = None
    stats: StreamStats = field(default_factory=StreamStats)

    def synchronize(self) -> None:
        return None

    def query(self) -> bool:
        return True

    def context(self):
        # simple context manager
        class _CM:
        def __enter__(self_non):
        return self

        def __exit__(self_non, exc_type, exc, tb):
        return False

        return _CM()


        @dataclass
class PooledEvent:
    event_id: int
    event: Any = None
    in_use: bool = False

    def record(self, stream: Optional[Any] = None) -> None:
        return None

    def query(self) -> bool:
        return True


class EventPool:
    def __init__(self, initial_size: int = 8, max_size: int = 256) -> None:
        self._events: Deque[PooledEvent] = deque()
        self._next = 0
        for _ in range(initial_size):
            self._events.append(PooledEvent(event_id=self._next))
            self._next += 1

    def acquire(self) -> Optional[PooledEvent]:
        if self._events:
            ev = self._events.popleft()
            ev.in_use = True
            return ev
        return None

    def release(self, ev: PooledEvent) -> None:
        ev.in_use = False
        self._events.append(ev)


class CudaStreamPool:
    def __init__(self, compute_streams: int = 1, comm_streams: int = 1) -> None:
        self.compute_streams = [PooledStream(i) for i in range(compute_streams)]
        self.comm_streams = [PooledStream(i + 1000) for i in range(comm_streams)]

    def acquire_compute(self) -> PooledStream:
        return self.compute_streams[0]

    def sync_all(self) -> None:
        return None


_GLOBAL_POOL: Optional[CudaStreamPool] = None


def get_global_stream_pool() -> CudaStreamPool:
    global _GLOBAL_POOL
    if _GLOBAL_POOL is None:
        _GLOBAL_POOL = CudaStreamPool()
    return _GLOBAL_POOL


def reset_global_pool() -> None:
    global _GLOBAL_POOL
    _GLOBAL_POOL = None


def compute_stream() -> PooledStream:
    return get_global_stream_pool().acquire_compute()


def comm_stream() -> PooledStream:
    return get_global_stream_pool().comm_streams[0]


def high_priority_stream() -> PooledStream:
    return PooledStream(stream_id=9999, priority=StreamPriority.HIGH)


__all__ = [
    "StreamPriority",
    "StreamState",
    "StreamStats",
    "PooledStream",
    "PooledEvent",
    "EventPool",
    "CudaStreamPool",
    "get_global_stream_pool",
    "reset_global_pool",
    "compute_stream",
    "comm_stream",
    "high_priority_stream",
]
