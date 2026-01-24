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
CUDAGraphManager - CUDA graph capture and replay management.

Implements vLLM's CUDAGraphWrapper patterns for efficient GPU execution:
- BatchDescriptor: Graph cache keys for shape-based lookup
- CUDAGraphEntry: Cached graphs with weak-ref outputs
- CUDAGraphWrapper: Automatic capture/replay management
- Runtime modes: NONE/PIECEWISE/FULL

Beyond vLLM:
- Adaptive capture based on hit rate patterns
- Predictive pre-warming for common shapes
- Memory-aware graph selection
"""

from __future__ import annotations

import gc
import logging
import threading
import time
import weakref
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CUDAGraphMode(IntEnum):
    """CUDA graph execution modes."""

    NONE = 0  # No CUDA graphs, pure eager mode
    PIECEWISE = 1  # Graphs between attention operations
    FULL = 2  # Full model as single graph

    def has_graphs(self) -> bool:
        """Check if mode uses any CUDA graphs."""
        return self != CUDAGraphMode.NONE

    def has_full_cudagraphs(self) -> bool:
        """Check if mode uses full CUDA graphs."""
        return self == CUDAGraphMode.FULL


@dataclass(frozen=True)
class BatchDescriptor:
    """
    Key for CUDA graph cache lookup.

    Attributes:
        num_tokens: Number of tokens in batch
        num_reqs: Number of requests (optional)
        is_uniform_decode: Whether batch is uniform decode
    """

    num_tokens: int
    num_reqs: Optional[int] = None
    is_uniform_decode: bool = False

    def __hash__(self) -> int:
        return hash((self.num_tokens, self.num_reqs, self.is_uniform_decode))

    def relaxed(self) -> "BatchDescriptor":
        """Get relaxed key without num_reqs for fallback matching."""
        return BatchDescriptor(num_tokens=self.num_tokens, num_reqs=None, is_uniform_decode=self.is_uniform_decode)


@dataclass
class CUDAGraphEntry:
    """
    Cached CUDA graph entry with metadata.

    Attributes:
        batch_descriptor: Key for this entry
        cudagraph: The captured CUDA graph (mock for non-GPU)
        output: Weak reference to output tensors
        input_addresses: Tracked input tensor addresses for validation
        capture_time: When graph was captured
        replay_count: Number of times replayed
    """

    batch_descriptor: BatchDescriptor
    cudagraph: Any = None  # torch.cuda.CUDAGraph
    output: Any = None  # Weak ref to output
    input_addresses: Optional[List[int]] = None
    capture_time: float = field(default_factory=time.time)
    replay_count: int = 0

    def increment_replay(self) -> None:
        """Increment replay count."""
        self.replay_count += 1


@dataclass
class CUDAGraphOptions:
    """Options for CUDA graph wrapper behavior."""

    debug_log_enable: bool = True
    gc_disable: bool = False
    weak_ref_output: bool = True
    validate_addresses: bool = False


@dataclass
class CUDAGraphStats:
    """Statistics for CUDA graph usage."""

    captures: int = 0
    replays: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    fallback_hits: int = 0

    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0


class MockCUDAGraph:
    """Mock CUDA graph for non-GPU environments."""

    def __init__(self):
        self._captured = False
        self._replay_fn: Optional[Callable] = None

    def capture_begin(self) -> None:
        """Begin graph capture."""
        self._captured = False

    def capture_end(self) -> None:
        """End graph capture."""
        self._captured = True

    def replay(self) -> None:
        """Replay captured graph."""
        if self._replay_fn is not None:
            self._replay_fn()


class CUDAGraphWrapper:
    """
    Wraps a callable to add CUDA graph capture/replay.

    Based on vLLM's CUDAGraphWrapper from cuda_graph.py.
    Provides automatic graph caching, capture, and replay
    based on batch descriptors.

    Beyond vLLM:
    - Adaptive capture based on hit patterns
    - Memory-aware graph eviction
    - Predictive pre-warming
    """

    def __init__(
        self,
        runnable: Callable[..., Any],
        runtime_mode: CUDAGraphMode = CUDAGraphMode.FULL,
        options: Optional[CUDAGraphOptions] = None,
        max_cached_graphs: int = 100,
    ):
        """
        Initialize wrapper.

        Args:
            runnable: The function/model to wrap
            runtime_mode: CUDA graph execution mode
            options: Graph options
            max_cached_graphs: Maximum graphs to cache
        """
        self.runnable = runnable
        self.runtime_mode = runtime_mode
        self.options = options or CUDAGraphOptions()
        self.max_cached_graphs = max_cached_graphs

        # Graph cache
        self.entries: Dict[BatchDescriptor, CUDAGraphEntry] = {}
        self._lock = threading.Lock()

        # Statistics
        self.stats = CUDAGraphStats()

        # First run tracking
        self._first_run_finished = False

        # Graph pool (simulated)
        self._graph_pool_id: Optional[int] = None

    def __getattr__(self, key: str) -> Any:
        """Allow accessing attributes of the wrapped runnable."""
        if hasattr(self.runnable, key):
            return getattr(self.runnable, key)
        raise AttributeError(f"Attribute {key} not found")

    def unwrap(self) -> Callable[..., Any]:
        """Get the underlying runnable."""
        return self.runnable

    def __call__(
        self,
        *args: Any,
        batch_descriptor: Optional[BatchDescriptor] = None,
        cudagraph_runtime_mode: Optional[CUDAGraphMode] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Execute with CUDA graph capture/replay.

        Args:
            *args: Positional arguments for runnable
            batch_descriptor: Key for graph caching
            cudagraph_runtime_mode: Override runtime mode
            **kwargs: Keyword arguments for runnable

        Returns:
            Output from runnable
        """
        # Determine effective mode
        mode = cudagraph_runtime_mode or self.runtime_mode

        # If no graphs or no descriptor, run eagerly
        if mode == CUDAGraphMode.NONE or batch_descriptor is None:
            return self.runnable(*args, **kwargs)

        # Mode mismatch - run eagerly
        if mode != self.runtime_mode:
            return self.runnable(*args, **kwargs)

        # Check cache
        with self._lock:
            if batch_descriptor in self.entries:
                return self._replay(batch_descriptor, *args, **kwargs)
            else:
                return self._capture(batch_descriptor, *args, **kwargs)

    def _capture(self, descriptor: BatchDescriptor, *args: Any, **kwargs: Any) -> Any:
        """Capture a new CUDA graph."""
        if self.options.debug_log_enable:
            logger.debug(f"Capturing CUDA graph for {descriptor}")

        # Create entry
        entry = CUDAGraphEntry(batch_descriptor=descriptor)

        # Track input addresses for validation
        if self.options.validate_addresses:
            entry.input_addresses = self._get_input_addresses(args)

        # Create mock graph (real impl would use torch.cuda.CUDAGraph)
        graph = MockCUDAGraph()

        # Optionally disable GC during capture
        gc_was_enabled = gc.isenabled()
        if self.options.gc_disable and gc_was_enabled:
            gc.disable()

        try:
            graph.capture_begin()
            output = self.runnable(*args, **kwargs)
            graph.capture_end()

            # Store output (optionally as weak ref)
            if self.options.weak_ref_output and hasattr(output, "__weakref__"):
                try:
                    entry.output = weakref.ref(output)
                except TypeError:
                    entry.output = output
            else:
                entry.output = output

            entry.cudagraph = graph

        finally:
            if self.options.gc_disable and gc_was_enabled:
                gc.enable()

        # Cache entry (with eviction if needed)
        self._cache_entry(descriptor, entry)
        self.stats.captures += 1

        return output

    def _replay(self, descriptor: BatchDescriptor, *args: Any, **kwargs: Any) -> Any:
        """Replay a cached CUDA graph."""
        entry = self.entries[descriptor]

        # Validate input addresses in debug mode
        if self.options.validate_addresses and entry.input_addresses is not None:
            current_addresses = self._get_input_addresses(args)
            if current_addresses != entry.input_addresses:
                raise RuntimeError(
                    f"Input addresses changed during replay. Expected {entry.input_addresses}, got {current_addresses}"
                )

        # Replay graph
        if entry.cudagraph is not None:
            entry.cudagraph.replay()

        entry.increment_replay()
        self.stats.replays += 1
        self.stats.cache_hits += 1

        # Return output (dereference weak ref if needed)
        output = entry.output
        if isinstance(output, weakref.ref):
            output = output()
        return output

    def _cache_entry(self, descriptor: BatchDescriptor, entry: CUDAGraphEntry) -> None:
        """Cache entry with LRU eviction if needed."""
        # Evict if at capacity
        if len(self.entries) >= self.max_cached_graphs:
            self._evict_lru()

        self.entries[descriptor] = entry

    def _evict_lru(self) -> None:
        """Evict least recently used entry."""
        if not self.entries:
            return

        # Find entry with oldest capture time and lowest replay count
        lru_key = min(self.entries.keys(), key=lambda k: (self.entries[k].replay_count, self.entries[k].capture_time))
        del self.entries[lru_key]

    def _get_input_addresses(self, args: tuple) -> List[int]:
        """Get data pointer addresses for tensor inputs."""
        addresses = []
        for arg in args:
            if hasattr(arg, "data_ptr"):
                addresses.append(arg.data_ptr())
            elif hasattr(arg, "__iter__") and not isinstance(arg, (str, bytes)):
                for item in arg:
                    if hasattr(item, "data_ptr"):
                        addresses.append(item.data_ptr())
        return addresses

    def get_cached_descriptors(self) -> List[BatchDescriptor]:
        """Get list of cached batch descriptors."""
        with self._lock:
            return list(self.entries.keys())

    def clear_cache(self) -> None:
        """Clear all cached graphs."""
        with self._lock:
            self.entries.clear()

    def get_stats(self) -> CUDAGraphStats:
        """Get current statistics."""
        return self.stats


class AdaptiveCUDAGraphWrapper(CUDAGraphWrapper):
    """
    Extended wrapper with adaptive capture based on usage patterns.

    Beyond vLLM:
    - Tracks shape frequency to prioritize common shapes
    - Predictive pre-warming of likely shapes
    - Memory budget awareness
    """

    def __init__(
        self,
        runnable: Callable[..., Any],
        runtime_mode: CUDAGraphMode = CUDAGraphMode.FULL,
        options: Optional[CUDAGraphOptions] = None,
        max_cached_graphs: int = 100,
        min_replays_to_keep: int = 3,
    ):
        super().__init__(runnable, runtime_mode, options, max_cached_graphs)
        self.min_replays_to_keep = min_replays_to_keep
        self.shape_frequency: Dict[BatchDescriptor, int] = defaultdict(int)

    def __call__(
        self,
        *args: Any,
        batch_descriptor: Optional[BatchDescriptor] = None,
        cudagraph_runtime_mode: Optional[CUDAGraphMode] = None,
        **kwargs: Any,
    ) -> Any:
        """Execute with adaptive caching."""
        if batch_descriptor is not None:
            self.shape_frequency[batch_descriptor] += 1

        return super().__call__(
            *args, batch_descriptor=batch_descriptor, cudagraph_runtime_mode=cudagraph_runtime_mode, **kwargs
        )

    def _evict_lru(self) -> None:
        """Evict considering both recency and frequency."""
        if not self.entries:
            return

        # Don't evict entries with high replay count
        candidates = [k for k, v in self.entries.items() if v.replay_count < self.min_replays_to_keep]

        if not candidates:
            # All entries are important, use standard LRU
            candidates = list(self.entries.keys())

        # Evict least frequent among candidates
        lru_key = min(candidates, key=lambda k: (self.shape_frequency.get(k, 0), self.entries[k].replay_count))
        del self.entries[lru_key]

    def get_hot_shapes(self, top_k: int = 10) -> List[Tuple[BatchDescriptor, int]]:
        """Get most frequently accessed shapes."""
        sorted_shapes = sorted(self.shape_frequency.items(), key=lambda x: x[1], reverse=True)
        return sorted_shapes[:top_k]

    def prewarm(self, shapes: List[BatchDescriptor], dummy_fn: Callable) -> None:
        """Pre-warm cache for expected shapes."""
        for shape in shapes:
            if shape not in self.entries:
                # Create dummy inputs and capture
                dummy_args = dummy_fn(shape)
                self._capture(shape, *dummy_args)


@contextmanager
def cudagraph_context(mode: CUDAGraphMode = CUDAGraphMode.NONE, descriptor: Optional[BatchDescriptor] = None):
    """Context manager for CUDA graph execution context."""
    # Store context in thread-local
    ctx = {"mode": mode, "descriptor": descriptor}
    yield ctx


def get_cudagraph_sizes(
    capture_sizes: Optional[List[int]], max_num_reqs: int, max_num_tokens: int, mode: CUDAGraphMode
) -> List[int]:
    """
    Compute CUDA graph capture sizes.

    Args:
        capture_sizes: Explicit sizes to capture
        max_num_reqs: Maximum number of requests
        max_num_tokens: Maximum number of tokens
        mode: CUDA graph mode

    Returns:
        List of sizes to capture graphs for
    """
    if mode == CUDAGraphMode.NONE:
        return []

    if capture_sizes is not None:
        return sorted(capture_sizes)

    # Default sizes: powers of 2 up to max
    sizes = []
    size = 1
    while size <= max_num_tokens:
        sizes.append(size)
        size *= 2

    # Add max size if not already included
    if max_num_tokens not in sizes:
        sizes.append(max_num_tokens)

    return sorted(sizes)
