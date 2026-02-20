#!/usr/bin/env python3
from __future__ import annotations

"""
Micro-batching context utilities.

This module provides a lightweight MicroBatchContext and stream manager
stubs for environments without CUDA. It intentionally avoids GPU-specific
complexity for unit tests.
"""
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Iterator, Optional, TypeVar


T = TypeVar("T")


class StreamType(Enum):
    COMPUTE = auto()
    COMMUNICATION = auto()
    DEFAULT = auto()


class MicroBatchState(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class StreamHandle:
    stream_id: int
    stream_type: StreamType
    stream: Any = None
    priority: int = 0
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)

    def synchronize(self) -> None:
        if hasattr(self.stream, "synchronize"):
            try:
                self.stream.synchronize()
            except Exception:
                pass


@dataclass
class MicroBatchInfo:
    batch_idx: int
    start_idx: int
    end_idx: int
    size: int
    state: MicroBatchState = MicroBatchState.PENDING
    compute_stream: Optional[StreamHandle] = None
    comm_stream: Optional[StreamHandle] = None
    start_time: float = 0.0
    end_time: float = 0.0

    @property
    def duration_ms(self) -> float:
        if self.end_time > 0:
            return (self.end_time - self.start_time) * 1000
        return 0.0


class StreamManager:
"""
Simple round-robin stream manager used for tests.""
def __init__(self, num_compute_streams: int = 1, num_comm_streams: int = 1):
        self._compute_streams = [StreamHandle(i, StreamType.COMPUTE) for i in range(num_compute_streams)]
        self._comm_streams = [StreamHandle(i, StreamType.COMMUNICATION) for i in range(num_comm_streams)]
        self._compute_idx = 0
        self._comm_idx = 0
        self._lock = threading.Lock()

    def get_compute_stream(self) -> Optional[StreamHandle]:
        if not self._compute_streams:
            return None
        with self._lock:
            h = self._compute_streams[self._compute_idx]
            self._compute_idx = (self._compute_idx + 1) % len(self._compute_streams)
            h.last_used = time.time()
            return h

    def get_comm_stream(self) -> Optional[StreamHandle]:
        if not self._comm_streams:
            return None
        with self._lock:
            h = self._comm_streams[self._comm_idx]
            self._comm_idx = (self._comm_idx + 1) % len(self._comm_streams)
            h.last_used = time.time()
            return h

    def synchronize_all(self) -> None:
        for h in self._compute_streams + self._comm_streams:
            h.synchronize()

    @contextmanager
    def compute_context(self) -> Iterator[Optional[StreamHandle]]:
        h = self.get_compute_stream()
        try:
            yield h
        finally:
            return

    @contextmanager
    def comm_context(self) -> Iterator[Optional[StreamHandle]]:
        h = self.get_comm_stream()
        try:
            yield h
        finally:
            return


class MicroBatchContext:
"""
Minimal micro-batch context for tests.""
def __init__(self, batch_size: int = 1, micro_batch_size: int = 1):
        self.batch_size = batch_size
        self.micro_batch_size = micro_batch_size
        self.stream_manager = StreamManager()
        self._infos: list[MicroBatchInfo] = []

    def iterate(self):
"""
        Yield micro-batch placeholders.""
        num = max(1, self.batch_size // max(1, self.micro_batch_size))
        for i in range(num):
        info = MicroBatchInfo(batch_idx=i, start_idx=i * self.micro_batch_size, end_idx=(i + 1) * self.micro_batch_size, size=self.micro_batch_size)
        yield info

    def record_output(self, info: MicroBatchInfo, _output: Any) -> None:
        info.state = MicroBatchState.COMPLETED

    def gather_outputs(self) -> list:
        return []


class AdaptiveMicroBatchContext(MicroBatchContext):
"""
Thin adaptive micro-batch context used in tests.

    It behaves like MicroBatchContext but exposes a simple `adapt()` method
    to change `micro_batch_size` at runtime.
"""
def adapt(self, new_micro_batch_size: int) -> None:
        self.micro_batch_size = max(1, int(new_micro_batch_size))


def create_micro_batch_context(batch_size: int = 1, micro_batch_size: int = 1) -> MicroBatchContext:
"""
Factory returning a MicroBatchContext instance (or adaptive variant).

    Tests import this factory and expect a callable.
"""
return MicroBatchContext(batch_size=batch_size, micro_batch_size=micro_batch_size)


@contextmanager
def micro_batch_scope(batch_size: int = 1, micro_batch_size: int = 1) -> Iterator[MicroBatchContext]:
"""
Context manager returning a micro-batch context for a block.

    Example:
        with micro_batch_scope(32, 8) as ctx:
            for info in ctx.iterate():
                ...
    ""
ctx = create_micro_batch_context(batch_size=batch_size, micro_batch_size=micro_batch_size)
    try:
        yield ctx
    finally:
        return
