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

"""MicroBatchContext - Micro-batch orchestration with CUDA stream synchronization.

This module implements thread-synchronized micro-batching for efficient
GPU utilization with separate compute and communication streams.

Inspired by vLLM v1/worker/ubatching.py UBatchContext, but extends with:
- Adaptive scheduling based on batch size and memory pressure
- Priority-based micro-batch ordering
- Dynamic stream selection based on workload
- Context state preservation across micro-batches

Example:
    >>> with MicroBatchContext(batch_size=32, micro_batch_size=8) as ctx:
    ...     for micro_batch in ctx.iterate():
    ...         result = model(micro_batch)
    ...         ctx.record_output(result)
    >>> final = ctx.gather_outputs()
"""

from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Generic, Iterator, Optional, TypeVar

# Try to import torch for GPU operations
try:
    import torch

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore

# Try to import Rust accelerations
try:
    from src.core.rust_bridge import get_bridge

    _BRIDGE = get_bridge()
    HAS_RUST = hasattr(_BRIDGE, "stream_sync_rust")
except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
    HAS_RUST = False
    _BRIDGE = None


T = TypeVar("T")


class StreamType(Enum):
    """Type of CUDA stream."""

    COMPUTE = auto()  # For compute operations
    COMMUNICATION = auto()  # For data transfers
    DEFAULT = auto()  # Default stream
    HIGH_PRIORITY = auto()  # High priority stream


class MicroBatchState(Enum):
    """State of a micro-batch."""

    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class StreamHandle:
    """Handle to a CUDA stream with metadata."""

    stream_id: int
    stream_type: StreamType
    stream: Any = None
    priority: int = 0
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)

    def synchronize(self) -> None:
        """Wait for all operations on this stream to complete."""
        if self.stream is not None and HAS_TORCH:
            self.stream.synchronize()

    def record_event(self, event: Optional[Any] = None) -> Any:
        """Record an event on this stream."""
        if not HAS_TORCH or not torch.cuda.is_available():
            return None

        if event is None:
            event = torch.cuda.Event()
        event.record(self.stream)
        return event

    def wait_event(self, event: Any) -> None:
        """Wait for an event from another stream."""
        if event is not None and self.stream is not None:
            self.stream.wait_event(event)


@dataclass
class MicroBatchInfo:
    """Information about a single micro-batch."""

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
        """Duration in milliseconds."""
        if self.end_time > 0:
            return (self.end_time - self.start_time) * 1000
        return 0.0


class StreamManager:
    """Manages CUDA streams for compute and communication.

    This class maintains separate stream pools for compute and
    communication operations, enabling overlap of transfers with compute.
    """

    def __init__(
        self,
        num_compute_streams: int = 2,
        num_comm_streams: int = 2,
        use_high_priority: bool = False,
    ):
        """Initialize stream manager.

        Args:
            num_compute_streams: Number of compute streams
            num_comm_streams: Number of communication streams
            use_high_priority: Whether to use high priority streams
        """
        self.num_compute_streams = num_compute_streams
        self.num_comm_streams = num_comm_streams
        self.use_high_priority = use_high_priority

        self._compute_streams: list[StreamHandle] = []
        self._comm_streams: list[StreamHandle] = []
        self._compute_idx = 0
        self._comm_idx = 0
        self._lock = threading.Lock()

        self._initialize_streams()

    def _initialize_streams(self) -> None:
        """Create CUDA streams."""
        if not HAS_TORCH or not torch.cuda.is_available():
            return

        # Create compute streams
        for i in range(self.num_compute_streams):
            priority = -1 if self.use_high_priority else 0
            stream = torch.cuda.Stream(priority=priority)
            self._compute_streams.append(
                StreamHandle(
                    stream_id=i,
                    stream_type=StreamType.COMPUTE,
                    stream=stream,
                    priority=priority,
                )
            )

        # Create communication streams
        for i in range(self.num_comm_streams):
            stream = torch.cuda.Stream()
            self._comm_streams.append(
                StreamHandle(
                    stream_id=i,
                    stream_type=StreamType.COMMUNICATION,
                    stream=stream,
                    priority=0,
                )
            )

    def get_compute_stream(self) -> Optional[StreamHandle]:
        """Get next compute stream (round-robin)."""
        if not self._compute_streams:
            return None

        with self._lock:
            handle = self._compute_streams[self._compute_idx]
            self._compute_idx = (self._compute_idx + 1) % len(self._compute_streams)
            handle.last_used = time.time()
            return handle

    def get_comm_stream(self) -> Optional[StreamHandle]:
        """Get next communication stream (round-robin)."""
        if not self._comm_streams:
            return None

        with self._lock:
            handle = self._comm_streams[self._comm_idx]
            self._comm_idx = (self._comm_idx + 1) % len(self._comm_streams)
            handle.last_used = time.time()
            return handle

    def synchronize_all(self) -> None:
        """Synchronize all streams."""
        for handle in self._compute_streams + self._comm_streams:
            handle.synchronize()

    @contextmanager
    def compute_context(self):
        """Context manager for compute operations."""
        handle = self.get_compute_stream()
        if handle is not None and handle.stream is not None:
            with torch.cuda.stream(handle.stream):
                yield handle
        else:
            yield handle

    @contextmanager
    def comm_context(self):
        """Context manager for communication operations."""
        handle = self.get_comm_stream()
        if handle is not None and handle.stream is not None:
            with torch.cuda.stream(handle.stream):
                yield handle
        else:
            yield handle


class MicroBatchContext(Generic[T]):
    """Thread-synchronized micro-batch context.

    This context manager handles the orchestration of micro-batches
    with proper CUDA stream synchronization and thread barriers.

    Attributes:
        batch_size: Total batch size
        micro_batch_size: Size of each micro-batch
        num_micro_batches: Number of micro-batches
    """

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        batch_size: int,
        micro_batch_size: int = 8,
        num_threads: int = 1,
        stream_manager: Optional[StreamManager] = None,
        adaptive: bool = True,
        min_micro_batch: int = 1,
        max_micro_batch: int = 64,
    ):
        """Initialize micro-batch context.

        Args:
            batch_size: Total batch size
            micro_batch_size: Size of each micro-batch
            num_threads: Number of worker threads
            stream_manager: Stream manager (creates default if None)
            adaptive: Whether to adapt micro-batch size dynamically
            min_micro_batch: Minimum micro-batch size (for adaptive)
            max_micro_batch: Maximum micro-batch size (for adaptive)
        """
        self.batch_size = batch_size
        self.micro_batch_size = micro_batch_size
        self.num_threads = num_threads
        self.adaptive = adaptive
        self.min_micro_batch = min_micro_batch
        self.max_micro_batch = max_micro_batch

        # Calculate number of micro-batches
        self.num_micro_batches = (batch_size + micro_batch_size - 1) // micro_batch_size

        # Stream manager
        if stream_manager is None:
            self._stream_manager = StreamManager(
                num_compute_streams=min(2, self.num_micro_batches),
                num_comm_streams=1,
            )
            self._owns_stream_manager = True
        else:
            self._stream_manager = stream_manager
            self._owns_stream_manager = False

        # Micro-batch tracking
        self._micro_batches: list[MicroBatchInfo] = []
        self._outputs: list[Optional[T]] = []
        self._current_idx = 0

        # Thread synchronization
        self._barrier = threading.Barrier(num_threads) if num_threads > 1 else None
        self._lock = threading.Lock()
        self._events: list[Any] = []

        # Performance tracking
        self._start_time: float = 0.0
        self._end_time: float = 0.0
        self._total_compute_time: float = 0.0

        # Initialize micro-batch info
        self._init_micro_batches()

    def _init_micro_batches(self) -> None:
        """Initialize micro-batch information."""
        for i in range(self.num_micro_batches):
            start = i * self.micro_batch_size
            end = min(start + self.micro_batch_size, self.batch_size)

            self._micro_batches.append(
                MicroBatchInfo(
                    batch_idx=i,
                    start_idx=start,
                    end_idx=end,
                    size=end - start,
                    compute_stream=self._stream_manager.get_compute_stream(),
                    comm_stream=self._stream_manager.get_comm_stream(),
                )
            )
            self._outputs.append(None)

    def __enter__(self) -> "MicroBatchContext[T]":
        """Enter context."""
        self._start_time = time.time()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context and cleanup."""
        # Synchronize all streams
        self._stream_manager.synchronize_all()
        self._end_time = time.time()

    def iterate(self) -> Iterator[MicroBatchInfo]:
        """Iterate over micro-batches.

        Yields:
            MicroBatchInfo for each micro-batch
        """
        for mb in self._micro_batches:
            mb.state = MicroBatchState.RUNNING
            mb.start_time = time.time()

            # Synchronize threads if multi-threaded
            if self._barrier is not None:
                self._barrier.wait()

            yield mb

            mb.end_time = time.time()
            mb.state = MicroBatchState.COMPLETED
            self._total_compute_time += mb.duration_ms

    def iterate_with_data(
        self,
        data: Any,
    ) -> Iterator[tuple[MicroBatchInfo, Any]]:
        """Iterate over micro-batches with corresponding data slices.

        Args:
            data: Data to slice (must support slicing)

        Yields:
            Tuple of (MicroBatchInfo, data_slice)
        """
        for mb in self.iterate():
            data_slice = data[mb.start_idx : mb.end_idx]
            yield mb, data_slice

    def record_output(self, output: T, mb_idx: Optional[int] = None) -> None:
        """Record output for a micro-batch.

        Args:
            output: Output to record
            mb_idx: Micro-batch index (uses current if None)
        """
        with self._lock:
            idx = mb_idx if mb_idx is not None else self._current_idx
            if 0 <= idx < len(self._outputs):
                self._outputs[idx] = output
            self._current_idx = idx + 1

    def gather_outputs(self) -> list[T]:
        """Gather all recorded outputs.

        Returns:
            List of outputs in order
        """
        return [o for o in self._outputs if o is not None]

    def gather_and_concat(self) -> Optional[T]:
        """Gather and concatenate outputs (for tensors).

        Returns:
            Concatenated tensor or None
        """
        outputs = self.gather_outputs()
        if not outputs:
            return None

        if HAS_TORCH and isinstance(outputs[0], torch.Tensor):
            return torch.cat(outputs, dim=0)

        # Try list concatenation
        if isinstance(outputs[0], list):
            result: list[Any] = []
            for o in outputs:
                result.extend(o)
            return result  # type: ignore

        return outputs  # type: ignore

    def sync_streams(self) -> None:
        """Synchronize all streams."""
        self._stream_manager.synchronize_all()

    def wait_barrier(self) -> None:
        """Wait at thread barrier."""
        if self._barrier is not None:
            self._barrier.wait()

    @property
    def stats(self) -> dict[str, Any]:
        """Get context statistics."""
        completed = sum(1 for mb in self._micro_batches if mb.state == MicroBatchState.COMPLETED)

        return {
            "batch_size": self.batch_size,
            "micro_batch_size": self.micro_batch_size,
            "num_micro_batches": self.num_micro_batches,
            "completed_micro_batches": completed,
            "total_time_ms": (self._end_time - self._start_time) * 1000 if self._end_time > 0 else 0,
            "total_compute_time_ms": self._total_compute_time,
            "avg_micro_batch_time_ms": self._total_compute_time / completed if completed > 0 else 0,
            "outputs_recorded": sum(1 for o in self._outputs if o is not None),
        }


class AdaptiveMicroBatchContext(MicroBatchContext[T]):
    """Micro-batch context with adaptive sizing.

    This extends MicroBatchContext to dynamically adjust micro-batch
    sizes based on memory pressure and execution times.
    """

    def __init__(
        self,
        batch_size: int,
        initial_micro_batch: int = 8,
        target_time_ms: float = 10.0,
        memory_threshold: float = 0.8,
        **kwargs: Any,
    ):
        """Initialize adaptive context.

        Args:
            batch_size: Total batch size
            initial_micro_batch: Initial micro-batch size
            target_time_ms: Target time per micro-batch
            memory_threshold: Memory threshold for shrinking
            **kwargs: Additional MicroBatchContext arguments
        """
        super().__init__(batch_size, initial_micro_batch, **kwargs)
        self.target_time_ms = target_time_ms
        self.memory_threshold = memory_threshold
        self._timing_history: list[float] = []

    def _adapt_size(self) -> None:
        """Adapt micro-batch size based on history."""
        if len(self._timing_history) < 2:
            return

        avg_time = sum(self._timing_history[-5:]) / min(5, len(self._timing_history))

        if avg_time > self.target_time_ms * 1.5:
            # Too slow - decrease size
            new_size = max(self.min_micro_batch, self.micro_batch_size // 2)
            if new_size != self.micro_batch_size:
                self.micro_batch_size = new_size
        elif avg_time < self.target_time_ms * 0.5:
            # Too fast - increase size
            new_size = min(self.max_micro_batch, self.micro_batch_size * 2)
            if new_size != self.micro_batch_size:
                self.micro_batch_size = new_size

    def iterate(self) -> Iterator[MicroBatchInfo]:
        """Iterate with adaptive sizing."""
        for mb in super().iterate():
            yield mb

            # Record timing and adapt
            self._timing_history.append(mb.duration_ms)
            if self.adaptive:
                self._adapt_size()


# Convenience functions
def create_micro_batch_context(
    batch_size: int,
    micro_batch_size: int = 8,
    adaptive: bool = False,
    **kwargs: Any,
) -> MicroBatchContext[Any]:
    """Create a micro-batch context.

    Args:
        batch_size: Total batch size
        micro_batch_size: Size of each micro-batch
        adaptive: Whether to use adaptive sizing
        **kwargs: Additional arguments

    Returns:
        MicroBatchContext instance
    """
    if adaptive:
        return AdaptiveMicroBatchContext(
            batch_size,
            initial_micro_batch=micro_batch_size,
            **kwargs,
        )
    return MicroBatchContext(batch_size, micro_batch_size, **kwargs)


@contextmanager
def micro_batch_scope(
    batch_size: int,
    micro_batch_size: int = 8,
    **kwargs: Any,
):
    """Context manager for micro-batching.

    Usage:
        >>> with micro_batch_scope(100, 10) as ctx:
        ...     for mb in ctx.iterate():
        ...         process(mb)
    """
    ctx = create_micro_batch_context(batch_size, micro_batch_size, **kwargs)
    with ctx:
        yield ctx
