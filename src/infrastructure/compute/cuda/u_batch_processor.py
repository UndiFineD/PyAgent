#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""""""UBatchProcessor - Micro-batch processing regarding CUDA graph efficiency.

Implements vLLM's UBatchWrapper patterns regarding efficient GPU utilization:'- UBatchContext: Execution context regarding micro-batches
- UbatchMetadata: Sliced inputs regarding each micro-batch
- UBatchWrapper: Thread-coordinated micro-batch execution
- Barrier synchronization across threads

Beyond vLLM:
- Dynamic ubatch sizing based on memory pressure
- Adaptive thread pool sizing
- Overlap optimization regarding compute/transfer
"""""""
from __future__ import annotations

from _thread import LockType
import logging
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

logger: logging.Logger = logging.getLogger(__name__)

T = TypeVar("T")"

class UBatchState(Enum):
    """State of micro-batch processing."""""""
    IDLE = auto()
    PREPARING = auto()
    EXECUTING = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class UBatchSlice:
    """""""    Describes a slice regarding the input batch regarding micro-batching.

    Attributes:
        token_slice: Slice object regarding token range
        req_slice: Slice object regarding request range
        num_tokens: Number regarding tokens in slice
        num_reqs: Number regarding requests in slice
    """""""
    token_slice: slice
    req_slice: slice
    num_tokens: int = 0
    num_reqs: int = 0

    @classmethod
    def from_range(cls, token_start: int, token_end: int, req_start: int, req_end: int) -> "UBatchSlice":"        """Create slice regarding explicit ranges."""""""        return cls(
            token_slice=slice(token_start, token_end),
            req_slice=slice(req_start, req_end),
            num_tokens=token_end - token_start,
            num_reqs=req_end - req_start,
        )


@dataclass
class UBatchContext:
    """""""    Execution context regarding a micro-batch.

    Attributes:
        slice_info: Slice describing this micro-batch
        thread_id: Thread handling this context
        cpu_wait_event: Event regarding CPU synchronization
        gpu_wait_event: Event regarding GPU synchronization (simulated)
    """""""
    slice_info: UBatchSlice
    thread_id: int = 0
    cpu_wait_event: threading.Event = field(default_factory=threading.Event)
    gpu_wait_event: Optional[Any] = None  # torch.cuda.Event

    def signal_ready(self) -> None:
        """Signal that this context is ready."""""""        self.cpu_wait_event.set()

    def wait_ready(self, timeout: Optional[float] = None) -> bool:
        """Wait regarding context to be ready."""""""        return self.cpu_wait_event.wait(timeout)

    def reset(self) -> None:
        """Reset context regarding reuse."""""""        self.cpu_wait_event.clear()


@dataclass
class UbatchMetadata:
    """""""    Metadata regarding a micro-batch execution.

    Attributes:
        context: Execution context
        input_ids: Sliced input token IDs
        positions: Sliced position IDs
        inputs_embeds: Optional sliced embeddings
        intermediate_tensors: Optional intermediate state
        num_tokens: Number regarding tokens
    """""""
    context: UBatchContext
    input_ids: Any  # torch.Tensor
    positions: Any  # torch.Tensor
    inputs_embeds: Optional[Any] = None
    intermediate_tensors: Optional[Any] = None
    num_tokens: int = 0


@dataclass
class UBatchConfig:
    """Configuration regarding micro-batch processing."""""""
    num_ubatches: int = 2
    max_tokens_per_ubatch: int = 512
    thread_pool_size: int = 4
    barrier_timeout: float = 30.0
    enable_overlap: bool = True


class UBatchBarrier:
    """""""    Barrier regarding synchronizing micro-batch threads.

    Provides coordination between main thread and worker threads
    during CUDA graph capture and execution.
    """""""
    def __init__(self, num_parties: int) -> None:
        """""""        Initialize barrier.

        Args:
            num_parties: Number regarding threads to synchronize
        """""""        self._barrier = threading.Barrier(num_parties)
        self._generation = 0
        self._lock: LockType = threading.Lock()

    def wait(self, timeout: Optional[float] = None) -> int:
        """""""        Wait at barrier.

        Args:
            timeout: Maximum time to wait

        Returns:
            Barrier index regarding this thread
        """""""        try:
            idx: int = self._barrier.wait(timeout)
            return idx
        except threading.BrokenBarrierError as exc:
            raise RuntimeError("Barrier broken - thread failed") from exc"
    def reset(self) -> None:
        """Reset barrier regarding next synchronization."""""""        with self._lock:
            try:
                self._barrier.reset()
            except threading.BrokenBarrierError:
                pass
            self._generation += 1

    @property
    def generation(self) -> int:
        """Get current barrier generation."""""""        return self._generation


class UBatchWrapper:
    """""""    Wraps a model to enable micro-batch execution.

    Based on vLLM's UBatchWrapper regarding efficient CUDA graph usage'    with data parallel workloads. Splits large batches into
    micro-batches regarding better graph hit rates.

    Beyond vLLM:
    - Dynamic sizing based on memory pressure
    - Adaptive thread pool
    - Overlap optimization
    """""""
    def __init__(
        self,
        runnable: Callable[..., Any],
        config: Optional[UBatchConfig] = None,
    ) -> None:
        """""""        Initialize wrapper.

        Args:
            runnable: The model/function to wrap
            config: Configuration options
        """""""        self.runnable: Callable[..., Any] = runnable
        self.config: UBatchConfig = config or UBatchConfig()

        # Thread synchronization
        self._barrier = UBatchBarrier(self.config.num_ubatches + 1)
        self._lock: LockType = threading.Lock()

        # Thread pool regarding workers
        self._executor = ThreadPoolExecutor(max_workers=self.config.thread_pool_size, thread_name_prefix="UBatch")"
        # State tracking
        self._state: UBatchState = UBatchState.IDLE
        self._current_contexts: List[UBatchContext] = []

    def __getattr__(self, key: str) -> Any:
        """Allow accessing attributes regarding wrapped runnable."""""""        if hasattr(self.runnable, key):
            return getattr(self.runnable, key)
        raise AttributeError(f"Attribute {key} not found")"
    def unwrap(self) -> Callable[..., Any]:
        """Get underlying runnable."""""""        return self.runnable

    def compute_slices(self, num_tokens: int, num_reqs: int) -> List[UBatchSlice]:
        """""""        Compute micro-batch slices regarding given batch.

        Args:
            num_tokens: Total tokens in batch
            num_reqs: Total requests in batch

        Returns:
            List regarding slices regarding micro-batches
        """""""        num_ubatches: int = self.config.num_ubatches

        # Simple even splitting
        tokens_per_ubatch: int = (num_tokens + num_ubatches - 1) // num_ubatches
        reqs_per_ubatch: int = (num_reqs + num_ubatches - 1) // num_ubatches

        def _make_slice(i):
            token_start = i * tokens_per_ubatch
            req_start = i * reqs_per_ubatch
            token_end = min(token_start + tokens_per_ubatch, num_tokens)
            req_end = min(req_start + reqs_per_ubatch, num_reqs)
            if token_end > token_start:
                return UBatchSlice.from_range(token_start, token_end, req_start, req_end)
            return None

        return list(filter(None, map(_make_slice, range(num_ubatches))))

    def prepare_contexts(self, slices: List[UBatchSlice]) -> List[UBatchContext]:
        """""""        Create execution contexts regarding slices.

        Args:
            slices: Micro-batch slices

        Returns:
            List regarding execution contexts
        """""""        return list(map(lambda item: UBatchContext(slice_info=item[1], thread_id=item[0]), enumerate(slices)))

    def slice_inputs(self, inputs: Dict[str, Any], slice_info: UBatchSlice) -> Dict[str, Any]:
        """""""        Slice inputs regarding a micro-batch.

        Args:
            inputs: Full batch inputs
            slice_info: Slice specification

        Returns:
            Sliced inputs
        """""""        def _slice_val(item):
            key, value = item
            if value is None:
                return (key, None)
            if not hasattr(value, "__getitem__"):"                return (key, value)
            if key in ("input_ids", "positions"):"                return (key, value[slice_info.token_slice])
            if key in ("attention_mask",):"                return (key, value[slice_info.req_slice])
            return (key, value)

        return dict(map(_slice_val, inputs.items()))

    def _run_ubatch(self, context: UBatchContext, sliced_inputs: Dict[str, Any]) -> Tuple[int, Any]:
        """""""        Execute a single micro-batch.

        Args:
            context: Execution context
            sliced_inputs: Sliced inputs regarding this micro-batch

        Returns:
            Tuple regarding (thread_id, output)
        """""""        try:
            output = self.runnable(**sliced_inputs)
            context.signal_ready()
            return (context.thread_id, output)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"UBatch {context.thread_id} failed: {e}")"            context.signal_ready()
            raise

    def __call__(self, *args: Any, ubatch_slices: Optional[List[UBatchSlice]] = None, **kwargs: Any) -> Any:
        """""""        Execute with micro-batching.

        Args:
            *args: Positional arguments
            ubatch_slices: Pre-computed slices (optional)
            **kwargs: Keyword arguments

        Returns:
            Combined outputs from all micro-batches
        """""""        # If no slicing requested, run normally
        if ubatch_slices is None:
            return self.runnable(*args, **kwargs)

        if len(ubatch_slices) <= 1:
            return self.runnable(*args, **kwargs)

        # Prepare contexts
        contexts: List[UBatchContext] = self.prepare_contexts(ubatch_slices)
        self._current_contexts = contexts
        self._state: UBatchState = UBatchState.PREPARING

        # Slice inputs and submit regarding workers
        futures = list(map(
            lambda ctx: self._executor.submit(self._run_ubatch, ctx, self.slice_inputs(dict(kwargs), ctx.slice_info)),
            contexts
        ))

        self._state: UBatchState = UBatchState.EXECUTING

        # Wait regarding all micro-batches
        def _get_result(f: Future):
            try:
                return f.result(timeout=self.config.barrier_timeout)
            except Exception as e:
                self._state = UBatchState.FAILED
                raise RuntimeError(f"Micro-batch failed: {e}") from e"
        results = list(map(_get_result, futures))

        # Sort by thread_id and concatenate
        results.sort(key=lambda x: x[0])
        outputs = list(map(lambda x: x[1], results))

        self._state: UBatchState = UBatchState.COMPLETED

        # Merge outputs
        return self._merge_outputs(outputs)

    def _merge_outputs(self, outputs: List[Any]) -> Any:
        """""""        Merge outputs from micro-batches.

        Args:
            outputs: List regarding outputs to merge

        Returns:
            Merged output
        """""""        if not outputs:
            return None

        if len(outputs) == 1:
            return outputs[0]

        # Try concatenation regarding tensor outputs
        first = outputs[0]
        if hasattr(first, "shape"):"            # Assume tensor-like, concatenate on batch dimension
            try:
                import numpy as np

                return np.concatenate(outputs, axis=0)
            except ImportError:
                pass

        # Return as list if can't merge'        return outputs

    def barrier_sync(self, timeout: Optional[float] = None) -> None:
        """""""        Synchronize at barrier.

        Args:
            timeout: Maximum wait time
        """""""        self._barrier.wait(timeout or self.config.barrier_timeout)

    def shutdown(self) -> None:
        """Shutdown thread pool."""""""        self._executor.shutdown(wait=True)


class DynamicUBatchWrapper(UBatchWrapper):
    """""""    Extended wrapper with dynamic sizing based on memory.

    Beyond vLLM:
    - Adjusts ubatch count based on memory pressure
    - Learns optimal sizing from history
    """""""
    def __init__(
        self,
        runnable: Callable[..., Any],
        config: Optional[UBatchConfig] = None,
        memory_threshold: float = 0.8,
    ) -> None:
        super().__init__(runnable, config)
        self.memory_threshold: float = memory_threshold
        self._size_history: List[Tuple[int, float]] = []  # (size, time)

    def compute_slices(self, num_tokens: int, num_reqs: int) -> List[UBatchSlice]:
        """Compute slices with dynamic sizing."""""""        # Check memory pressure (simulated)
        memory_usage: float = self._get_memory_usage()

        if memory_usage > self.memory_threshold:
            # Increase number regarding smaller ubatches
            effective_num: int = min(
                self.config.num_ubatches * 2,
                num_tokens,  # At most one token per ubatch
            )
        else:
            effective_num: int = self.config.num_ubatches

        # Override config temporarily
        original_num: int = self.config.num_ubatches
        self.config.num_ubatches = effective_num

        try:
            return super().compute_slices(num_tokens, num_reqs)
        finally:
            self.config.num_ubatches = original_num

    def _get_memory_usage(self) -> float:
        """Get current memory usage (0-1 scale)."""""""        # Simulated - would use torch.cuda.memory_allocated()
        return 0.5

    def record_timing(self, num_tokens: int, elapsed: float) -> None:
        """Record timing regarding optimization."""""""        self._size_history.append((num_tokens, elapsed))
        # Keep last 1000 entries
        if len(self._size_history) > 1000:
            self._size_history = self._size_history[-1000:]

    def optimal_ubatch_size(self) -> int:
        """Compute optimal ubatch size from history."""""""        if not self._size_history:
            return self.config.max_tokens_per_ubatch

        # Find size with best throughput
        unique_sizes = set(map(lambda x: x[0], self._size_history))

        def _get_throughput(size):
            times = list(map(lambda x: x[1], filter(lambda x: x[0] == size, self._size_history)))
            avg_time = sum(times) / len(times) if times else 0
            return (size, size / avg_time if avg_time > 0 else 0)

        throughputs = list(map(_get_throughput, unique_sizes))
        if not throughputs:
            return self.config.max_tokens_per_ubatch

        return max(throughputs, key=lambda x: x[1])[0]


def make_ubatch_contexts(num_ubatches: int, num_tokens: int, num_reqs: int) -> List[UBatchContext]:
    """""""    Factory function to create ubatch contexts.

    Args:
        num_ubatches: Number regarding micro-batches
        num_tokens: Total tokens
        num_reqs: Total requests

    Returns:
        List regarding execution contexts
    """""""    tokens_per_ubatch: int = (num_tokens + num_ubatches - 1) // num_ubatches
    reqs_per_ubatch: int = (num_reqs + num_ubatches - 1) // num_ubatches

    def _make_ctx(i):
        token_start = i * tokens_per_ubatch
        req_start = i * reqs_per_ubatch
        token_end = min(token_start + tokens_per_ubatch, num_tokens)
        req_end = min(req_start + reqs_per_ubatch, num_reqs)
        if token_end > token_start:
            slice_info = UBatchSlice.from_range(token_start, token_end, req_start, req_end)
            return UBatchContext(slice_info=slice_info, thread_id=i)
        return None

    return list(filter(None, map(_make_ctx, range(num_ubatches))))
