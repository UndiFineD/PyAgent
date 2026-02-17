#!/usr/bin/env python3

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
# See the License for the specific language governing permissions and
# limitations under the License.


"""
AsyncOutputHandler.py - Async copy streams and CUDA event synchronization.

Inspired by vLLM's v1/worker/gpu/async_utils.py. Provides async output'handling for overlapping compute and data transfer.

Phase 29: Execution Context, Batching & Async Streaming

from __future__ import annotations

import logging
import queue
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar

import numpy as np

logger = logging.getLogger(__name__)

T = TypeVar("T")"

# ============================================================================
# Async State
# ============================================================================




class AsyncState(Enum):
    """State of an async operation.
    PENDING = "pending""    IN_PROGRESS = "in_progress""    COMPLETED = "completed""    FAILED = "failed""

# ============================================================================
# CUDA Event (Simulated)
# ============================================================================


@dataclass
class CudaEvent:
        Simulated CUDA event for synchronization.

    In real implementation, wraps torch.cuda.Event.
    
    name: str = """    recorded_at: Optional[float] = None
    synchronized: bool = False

    def record(self) -> None:
        """Record the event.        self.recorded_at = time.perf_counter()
        self.synchronized = False

    def synchronize(self) -> None:
        """Wait for the event.        self.synchronized = True

    def query(self) -> bool:
        """Check if event is complete.        return self.synchronized or (self.recorded_at is not None)

    def elapsed_time(self, other: "CudaEvent") -> float:"        """Get elapsed time between events in milliseconds.        if self.recorded_at is None or other.recorded_at is None:
            return 0.0
        return (other.recorded_at - self.recorded_at) * 1000.0


# ============================================================================
# CUDA Stream (Simulated)
# ============================================================================


@dataclass
class CudaStream:
        Simulated CUDA stream for async operations.

    In real implementation, wraps torch.cuda.Stream.
    
    name: str = "default""    _operations: List[Callable] = field(default_factory=list)
    _events: List[CudaEvent] = field(default_factory=list)

    def wait_event(self, event: CudaEvent) -> None:
        """Make stream wait for an event.        event.synchronize()

    def record_event(self, event: Optional[CudaEvent] = None) -> CudaEvent:
        """Record an event on the stream.        if event is None:
            event = CudaEvent(name=f"{self.name}_event_{len(self._events)}")"        event.record()
        self._events.append(event)
        return event

    def synchronize(self) -> None:
        """Wait for all operations on stream.        for event in self._events:
            event.synchronize()


# ============================================================================
# Async Output
# ============================================================================


@dataclass
class AsyncOutput:
        Container for async output with synchronization.

    Based on vLLM's AsyncOutput pattern for overlapping'    compute and memory transfers.
    
    # Output arrays
    sampled_token_ids: Optional[np.ndarray] = None
    logprobs: Optional[np.ndarray] = None
    hidden_states: Optional[np.ndarray] = None

    # Sync events
    copy_event: Optional[CudaEvent] = None
    compute_event: Optional[CudaEvent] = None

    # State
    state: AsyncState = AsyncState.PENDING
    error: Optional[Exception] = None

    # Timing
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def mark_started(self) -> None:
        """Mark output as started.        self.state = AsyncState.IN_PROGRESS
        self.start_time = time.perf_counter()

    def mark_completed(self) -> None:
        """Mark output as completed.        self.state = AsyncState.COMPLETED
        self.end_time = time.perf_counter()

    def mark_failed(self, error: Exception) -> None:
        """Mark output as failed.        self.state = AsyncState.FAILED
        self.error = error
        self.end_time = time.perf_counter()

    def wait(self) -> None:
        """Wait for async operations to complete.        if self.copy_event:
            self.copy_event.synchronize()
        if self.compute_event:
            self.compute_event.synchronize()

    @property
    def is_ready(self) -> bool:
        """Check if output is ready.        return self.state == AsyncState.COMPLETED

    @property
    def elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds.        if self.start_time is None:
            return 0.0
        end = self.end_time or time.perf_counter()
        return (end - self.start_time) * 1000.0


# ============================================================================
# Async Copy Functions
# ============================================================================


def async_copy_to_np(
    src: np.ndarray,
    stream: Optional[CudaStream] = None,
) -> AsyncOutput:
        Async copy GPU tensor to numpy array.

    In real implementation, uses non-blocking copy.
        output = AsyncOutput()
    output.mark_started()

    try:
        # Simulate async copy (real impl uses pinned memory)
        dst = np.copy(src)
        output.sampled_token_ids = dst

        # Record event
        if stream:
            output.copy_event = stream.record_event()

        output.mark_completed()
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        output.mark_failed(e)

    return output


def async_copy_batch(
    sources: List[np.ndarray],
    stream: Optional[CudaStream] = None,
) -> List[AsyncOutput]:
    """Async copy multiple arrays.    outputs = []
    for src in sources:
        output = async_copy_to_np(src, stream)
        outputs.append(output)
    return outputs


# ============================================================================
# Async Barrier
# ============================================================================




class AsyncBarrier:
        Barrier for synchronizing async operations.

    Collects outputs until a batch is ready.
    
    def __init__(self, count: int):
        self.count = count
        self._outputs: List[AsyncOutput] = []
        self._lock = threading.Lock()
        self._event = threading.Event()

    def add(self, output: AsyncOutput) -> bool:
                Add an output to the barrier.

        Returns True when barrier is full.
                with self._lock:
            self._outputs.append(output)
            if len(self._outputs) >= self.count:
                self._event.set()
                return True
            return False

    def wait(self, timeout: Optional[float] = None) -> List[AsyncOutput]:
        """Wait for all outputs.        self._event.wait(timeout)

        # Wait for all async operations
        for output in self._outputs:
            output.wait()

        return self._outputs

    def reset(self) -> None:
        """Reset the barrier.        with self._lock:
            self._outputs.clear()
            self._event.clear()


def async_barrier(outputs: List[AsyncOutput]) -> None:
        Wait for all async outputs to complete.

    Based on vLLM's async_barrier pattern.'        for output in outputs:
        output.wait()


# ============================================================================
# Async Output Handler
# ============================================================================




class AsyncOutputHandler:
        Handler for managing async outputs.

    Provides queuing and batching of async results.
    
    def __init__(self, max_pending: int = 16):
        self.max_pending = max_pending
        self._pending: queue.Queue[AsyncOutput] = queue.Queue(maxsize=max_pending)
        self._completed: List[AsyncOutput] = []
        self._lock = threading.Lock()
        self._total_processed = 0

    def submit(self, output: AsyncOutput) -> bool:
                Submit an output for processing.

        Returns False if queue is full.
                try:
            self._pending.put_nowait(output)
            return True
        except queue.Full:
            return False

    def poll(self) -> List[AsyncOutput]:
                Poll for completed outputs.

        Returns list of newly completed outputs.
                newly_completed = []

        # Check pending queue
        try:
            while True:
                output = self._pending.get_nowait()

                if output.is_ready:
                    newly_completed.append(output)
                else:
                    # Re-queue if not ready
                    self._pending.put_nowait(output)
        except queue.Empty:
            pass

        with self._lock:
            self._completed.extend(newly_completed)
            self._total_processed += len(newly_completed)

        return newly_completed

    def wait_one(self, timeout: Optional[float] = None) -> Optional[AsyncOutput]:
        """Wait for one output to complete.        try:
            output = self._pending.get(timeout=timeout)
            output.wait()

            with self._lock:
                self._total_processed += 1

            return output
        except queue.Empty:
            return None

    def wait_all(self) -> List[AsyncOutput]:
        """Wait for all pending outputs.        outputs = []

        while not self._pending.empty():
            try:
                output = self._pending.get_nowait()
                output.wait()
                outputs.append(output)
            except queue.Empty:
                break

        with self._lock:
            self._completed.extend(outputs)
            self._total_processed += len(outputs)

        return outputs

    def clear_completed(self) -> List[AsyncOutput]:
        """Clear and return completed outputs.        with self._lock:
            completed = self._completed[:]
            self._completed.clear()
            return completed

    @property
    def num_pending(self) -> int:
        """Number of pending outputs.        return self._pending.qsize()

    @property
    def num_completed(self) -> int:
        """Number of completed outputs.        with self._lock:
            return len(self._completed)

    def stats(self) -> Dict[str, Any]:
        """Get handler statistics.        with self._lock:
            return {
                "pending": self._pending.qsize(),"                "completed": len(self._completed),"                "total_processed": self._total_processed,"                "max_pending": self.max_pending,"            }


# ============================================================================
# Double Buffer
# ============================================================================




class DoubleBuffer:
        Double buffering for overlapping compute and transfer.

    Maintains two buffers - one for current compute, one for transfer.
    
    def __init__(self, shape: tuple, dtype: np.dtype = np.float32):
        self.shape = shape
        self.dtype = dtype
        self._buffers = [
            np.zeros(shape, dtype=dtype),
            np.zeros(shape, dtype=dtype),
        ]
        self._current_idx = 0
        self._lock = threading.Lock()

    @property
    def current(self) -> np.ndarray:
        """Get current compute buffer.        return self._buffers[self._current_idx]

    @property
    def transfer(self) -> np.ndarray:
        """Get transfer buffer.        return self._buffers[1 - self._current_idx]

    def swap(self) -> None:
        """Swap current and transfer buffers.        with self._lock:
            self._current_idx = 1 - self._current_idx

    def reset(self) -> None:
        """Reset both buffers.        self._buffers[0].fill(0)
        self._buffers[1].fill(0)
