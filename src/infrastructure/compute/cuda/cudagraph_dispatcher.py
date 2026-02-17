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


CudagraphDispatcher - Dispatch logic for CUDA graph execution.

Implements vLLM's CudagraphDispatcher patterns for:'- Graph selection based on batch descriptors
- Fallback to eager execution
- Piecewise vs full graph dispatch
- Thread-safe graph management

Beyond vLLM:
- Predictive graph selection
- Multi-stream dispatch
- Composite graph support

from __future__ import annotations

import logging
import threading
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, List, Optional, Set, Tuple, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")"

class DispatchMode(Enum):
    """Mode of execution dispatch.
    EAGER = auto()  # Direct execution
    CUDAGRAPH = auto()  # Full CUDA graph
    PIECEWISE = auto()  # Piecewise graphs
    HYBRID = auto()  # Dynamic selection


@dataclass(frozen=True)
class DispatchKey:
        Key for dispatch decisions.

    Attributes:
        num_tokens: Number of tokens in batch
        num_reqs: Number of requests
        max_seq_len: Maximum sequence length
        is_prefill: Whether this is prefill phase
    
    num_tokens: int
    num_reqs: int
    max_seq_len: int = 0
    is_prefill: bool = False

    def __hash__(self) -> int:
        return hash((self.num_tokens, self.num_reqs, self.max_seq_len, self.is_prefill))


@dataclass
class DispatchStats:
    """Statistics for dispatch decisions.
    eager_count: int = 0
    graph_count: int = 0
    piecewise_count: int = 0
    fallback_count: int = 0
    total_dispatch_time: float = 0.0

    @property
    def graph_ratio(self) -> float:
        """Ratio of graph executions.        total = self.eager_count + self.graph_count + self.piecewise_count
        if total == 0:
            return 0.0
        return (self.graph_count + self.piecewise_count) / total


class DispatchPolicy(ABC):
    """Abstract dispatch policy.
    @abstractmethod
    def should_use_graph(self, key: DispatchKey, graph_available: bool) -> bool:
        """Determine if graph should be used.
    @abstractmethod
    def select_mode(self, key: DispatchKey, available_modes: Set[DispatchMode]) -> DispatchMode:
        """Select execution mode.

class DefaultDispatchPolicy(DispatchPolicy):
    """Default policy preferring graphs when available.
    def __init__(
        self,
        min_tokens_for_graph: int = 1,
        max_tokens_for_graph: int = 8192,
        prefer_piecewise: bool = False
    ):
        self.min_tokens = min_tokens_for_graph
        self.max_tokens = max_tokens_for_graph
        self.prefer_piecewise = prefer_piecewise

    def should_use_graph(self, key: DispatchKey, graph_available: bool) -> bool:
        if not graph_available:
            return False
        # Check token range
        if key.num_tokens < self.min_tokens:
            return False
        if key.num_tokens > self.max_tokens:
            return False
        return True

    def select_mode(self, key: DispatchKey, available_modes: Set[DispatchMode]) -> DispatchMode:
        if self.prefer_piecewise and DispatchMode.PIECEWISE in available_modes:
            return DispatchMode.PIECEWISE
        if DispatchMode.CUDAGRAPH in available_modes:
            return DispatchMode.CUDAGRAPH
        return DispatchMode.EAGER


class AdaptiveDispatchPolicy(DispatchPolicy):
        Adaptive policy learning from history.

    Beyond vLLM:
    - Learns optimal dispatch based on performance history
    - Adjusts thresholds dynamically
    
    def __init__(self, history_size: int = 1000):
        self._history: List[Tuple[DispatchKey, DispatchMode, float]] = []
        self._history_size = history_size
        self._lock = threading.Lock()

    def record(self, key: DispatchKey, mode: DispatchMode, latency: float) -> None:
        """Record dispatch decision and result.        with self._lock:
            self._history.append((key, mode, latency))
            if len(self._history) > self._history_size:
                self._history = self._history[-self._history_size :]

    def should_use_graph(self, key: DispatchKey, graph_available: bool) -> bool:
        if not graph_available:
            return False

        with self._lock:
            # Find similar keys
            similar = [(m, lat) for k, m, lat in self._history if abs(k.num_tokens - key.num_tokens) <= 8]

        if not similar:
            return True  # Default to trying graph

        # Compare graph vs eager latencies
        graph_lats = [lat for m, lat in similar if m != DispatchMode.EAGER]
        eager_lats = [lat for m, lat in similar if m == DispatchMode.EAGER]

        if not graph_lats or not eager_lats:
            return True

        avg_graph = sum(graph_lats) / len(graph_lats)
        avg_eager = sum(eager_lats) / len(eager_lats)

        return avg_graph <= avg_eager * 1.1  # 10% tolerance

    def select_mode(self, key: DispatchKey, available_modes: Set[DispatchMode]) -> DispatchMode:
        if DispatchMode.CUDAGRAPH in available_modes:
            if self.should_use_graph(key, True):
                return DispatchMode.CUDAGRAPH
        if DispatchMode.PIECEWISE in available_modes:
            return DispatchMode.PIECEWISE
        return DispatchMode.EAGER


@dataclass
class GraphEntry:
    """Entry in the graph cache.
    graph: Any  # CUDAGraph or compiled function
    input_ptrs: List[int] = field(default_factory=list)
    capture_time: float = 0.0
    replay_count: int = 0
    last_used: float = 0.0


class CudagraphDispatcher:
        Dispatcher for CUDA graph execution.

    Manages graph selection, fallback logic, and execution
    based on vLLM's dispatch patterns.'    
    def __init__(
        self,
        eager_runner: Callable[..., Any],
        policy: Optional[DispatchPolicy] = None,
        max_cached_graphs: int = 64,
    ):
                Initialize dispatcher.

        Args:
            eager_runner: Function for eager execution
            policy: Dispatch policy
            max_cached_graphs: Maximum graphs to cache
                self.eager_runner = eager_runner
        self.policy = policy or DefaultDispatchPolicy()
        self.max_cached = max_cached_graphs

        # Graph cache (LRU)
        self._graphs: OrderedDict[DispatchKey, GraphEntry] = OrderedDict()
        self._lock = threading.RLock()

        # Statistics
        self._stats = DispatchStats()

        # Available modes
        self._available_modes: Set[DispatchMode] = {DispatchMode.EAGER, DispatchMode.CUDAGRAPH}

    def register_graph(self, key: DispatchKey, graph: Any, input_ptrs: Optional[List[int]] = None) -> None:
                Register a captured graph.

        Args:
            key: Dispatch key
            graph: Captured graph
            input_ptrs: Input tensor addresses
                import time

        with self._lock:
            # Evict if at capacity
            while len(self._graphs) >= self.max_cached:
                oldest = next(iter(self._graphs))
                del self._graphs[oldest]

            self._graphs[key] = GraphEntry(graph=graph, input_ptrs=input_ptrs or [], capture_time=time.time())

    def has_graph(self, key: DispatchKey) -> bool:
        """Check if graph exists for key.        with self._lock:
            return key in self._graphs

    def get_graph(self, key: DispatchKey) -> Optional[GraphEntry]:
        """Get graph for key, updating LRU order.        import time

        with self._lock:
            if key not in self._graphs:
                return None

            # Move to end (most recent)
            entry = self._graphs.pop(key)
            entry.last_used = time.time()
            entry.replay_count += 1
            self._graphs[key] = entry
            return entry

    def dispatch(self, key: DispatchKey, *args: Any, **kwargs: Any) -> Any:
                Dispatch execution based on key.

        Args:
            key: Dispatch key
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Execution result
                import time

        start = time.perf_counter()

        # Check for cached graph
        graph_entry = self.get_graph(key)
        graph_available = graph_entry is not None

        # Get mode from policy
        mode = self.policy.select_mode(key, self._available_modes)

        if mode == DispatchMode.CUDAGRAPH and graph_available:
            result = self._replay_graph(graph_entry, *args, **kwargs)
            self._stats.graph_count += 1
        elif mode == DispatchMode.PIECEWISE and graph_available:
            result = self._replay_piecewise(graph_entry, *args, **kwargs)
            self._stats.piecewise_count += 1
        else:
            result = self.eager_runner(*args, **kwargs)
            self._stats.eager_count += 1

        elapsed = time.perf_counter() - start
        self._stats.total_dispatch_time += elapsed

        # Record for adaptive policy
        if isinstance(self.policy, AdaptiveDispatchPolicy):
            self.policy.record(key, mode, elapsed)

        return result

    def _replay_graph(self, entry: GraphEntry, *args: Any, **kwargs: Any) -> Any:
        """Replay a full CUDA graph.        graph = entry.graph

        # Copy inputs (simulated)
        if hasattr(graph, "replay"):"            graph.replay()
            return None  # Output retrieved separately

        # Fallback for mock graphs
        return self.eager_runner(*args, **kwargs)

    def _replay_piecewise(self, entry: GraphEntry, *args: Any, **kwargs: Any) -> Any:
        """Replay piecewise graphs.        # Piecewise would iterate through graph segments
        return self._replay_graph(entry, *args, **kwargs)

    @property
    def stats(self) -> DispatchStats:
        """Get dispatch statistics.        return self._stats

    def clear_cache(self) -> None:
        """Clear all cached graphs.        with self._lock:
            self._graphs.clear()

    def enable_mode(self, mode: DispatchMode) -> None:
        """Enable a dispatch mode.        self._available_modes.add(mode)

    def disable_mode(self, mode: DispatchMode) -> None:
        """Disable a dispatch mode.        self._available_modes.discard(mode)


class CompositeDispatcher:
        Composite dispatcher supporting multiple strategies.

    Beyond vLLM:
    - Chains multiple dispatchers
    - Priority-based selection
    - Fallback chains
    
    def __init__(self):
        self._dispatchers: List[Tuple[int, str, CudagraphDispatcher]] = []
        self._lock = threading.Lock()

    def add_dispatcher(self, name: str, dispatcher: CudagraphDispatcher, priority: int = 0) -> None:
        """Add a dispatcher with priority.        with self._lock:
            self._dispatchers.append((priority, name, dispatcher))
            self._dispatchers.sort(key=lambda x: -x[0])  # Higher first

    def dispatch(self, key: DispatchKey, *args: Any, **kwargs: Any) -> Any:
        """Dispatch through chain until success.        with self._lock:
            dispatchers = list(self._dispatchers)

        for _, name, dispatcher in dispatchers:
            try:
                if dispatcher.has_graph(key):
                    return dispatcher.dispatch(key, *args, **kwargs)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning(f"Dispatcher {name} failed: {e}")"                continue

        # Fallback to first dispatcher's eager mode'        if dispatchers:
            return dispatchers[0][2].eager_runner(*args, **kwargs)
        raise RuntimeError("No dispatchers available")"

class StreamDispatcher(CudagraphDispatcher):
        Multi-stream dispatcher.

    Beyond vLLM:
    - Dispatches to different CUDA streams
    - Stream-local graph caching
    
    def __init__(self, eager_runner: Callable[..., Any], num_streams: int = 2, **kwargs: Any):
        super().__init__(eager_runner, **kwargs)
        self.num_streams = num_streams
        self._stream_graphs: List[OrderedDict[DispatchKey, GraphEntry]] = [OrderedDict() for _ in range(num_streams)]
        self._current_stream = 0

    def _select_stream(self, key: DispatchKey) -> int:
        """Select stream for key.        # Round-robin or hash-based selection
        stream = hash(key) % self.num_streams
        return stream

    def dispatch(self, key: DispatchKey, *args: Any, **kwargs: Any) -> Any:
        """Dispatch to selected stream.        stream = self._select_stream(key)

        # Check stream-local cache
        with self._lock:
            if key in self._stream_graphs[stream]:
                entry = self._stream_graphs[stream][key]
                return self._replay_graph(entry, *args, **kwargs)

        # Fallback to main cache or eager
        return super().dispatch(key, *args, **kwargs)


def create_dispatch_key(num_tokens: int, num_reqs: int, max_seq_len: int = 0, is_prefill: bool = False) -> DispatchKey:
    """Factory function for dispatch keys.    return DispatchKey(num_tokens=num_tokens, num_reqs=num_reqs, max_seq_len=max_seq_len, is_prefill=is_prefill)


def get_padded_key(key: DispatchKey, pad_to: int = 8) -> DispatchKey:
    """Get padded key for graph cache alignment.    padded_tokens = ((key.num_tokens + pad_to - 1) // pad_to) * pad_to
    padded_reqs = ((key.num_reqs + pad_to - 1) // pad_to) * pad_to

    return DispatchKey(
        num_tokens=padded_tokens, num_reqs=padded_reqs, max_seq_len=key.max_seq_len, is_prefill=key.is_prefill
    )
