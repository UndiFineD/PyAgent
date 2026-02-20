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
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
ForwardContext.py - Execution context management for model forward passes.

"""
Inspired by vLLM's forward_context.py. Provides thread-local context for'attention metadata, batch descriptors, and data parallel coordination.

Phase 29: Execution Context, Batching & Async Streaming

import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Generator, NamedTuple, Optional

import numpy as np

# ============================================================================
# Batch Descriptor
# ============================================================================



class BatchDescriptor(NamedTuple):
        Batch descriptor for CUDA graph dispatching.

    Uniquely identifies a padded batch configuration for graph key matching.
    Based on vLLM's BatchDescriptor pattern.'    
    num_tokens: int
    num_reqs: Optional[int] = None
    uniform: bool = False
    has_lora: bool = False

    def relaxed(self) -> "BatchDescriptor":"                Return a relaxed batch descriptor for mixed batch CUDA graphs.
        Sets uniform=False and num_reqs=None for flexible matching.
                return BatchDescriptor(
            num_tokens=self.num_tokens,
            num_reqs=None,
            uniform=False,
            has_lora=self.has_lora,
        )

    def with_num_tokens(self, num_tokens: int) -> "BatchDescriptor":"        """
Return a copy with updated num_tokens.        return BatchDescriptor(

            num_tokens=num_tokens,
            num_reqs=self.num_reqs,
            uniform=self.uniform,
            has_lora=self.has_lora,
        )

    def key(self) -> tuple:
"""
Return a hashable key for graph lookup.        return (self.num_tokens, self.num_reqs, self.uniform, self.has_lora)

    def hash_key(self) -> int:
"""
Return an integer hash for fast lookup.        return hash(self.key())


# ============================================================================
# Data Parallel Metadata
# ============================================================================


@dataclass
class DPMetadata:
        Data parallel metadata for distributed inference.

    Tracks token distribution across data parallel ranks for synchronization.
    Based on vLLM's DPMetadata pattern.'    
    world_size: int = 1
    rank: int = 0
    num_tokens_across_dp: Optional[np.ndarray] = None
    local_num_tokens: int = 0

    @classmethod
    def make(
        cls,
        world_size: int,
        rank: int,
        num_tokens: int,
        num_tokens_across_dp: Optional[np.ndarray] = None,
    ) -> "DPMetadata":"        """
Factory method to create DPMetadata.        if num_tokens_across_dp is None and world_size > 1:
            # Default: evenly distributed
            num_tokens_across_dp = np.full(world_size, num_tokens // world_size, dtype=np.int32)
            # Distribute remainder
            remainder = num_tokens % world_size
            for i in range(remainder):
                num_tokens_across_dp[i] += 1

        return cls(
            world_size=world_size,
            rank=rank,
            num_tokens_across_dp=num_tokens_across_dp,
            local_num_tokens=num_tokens if num_tokens_across_dp is None else int(num_tokens_across_dp[rank]),
        )

    @classmethod
    def single(cls, num_tokens: int) -> "DPMetadata":"        """
Create metadata for single-process execution.        return cls(
            world_size=1,
            rank=0,
            num_tokens_across_dp=np.array([num_tokens], dtype=np.int32),
            local_num_tokens=num_tokens,
        )

    def get_local_tokens(self) -> int:
"""
Get number of tokens for this rank.        return self.local_num_tokens

    def get_total_tokens(self) -> int:
"""
Get total tokens across all ranks.        if self.num_tokens_across_dp is not None:
            return int(np.sum(self.num_tokens_across_dp))
        return self.local_num_tokens


# ============================================================================
# Forward Context
# ============================================================================


@dataclass
class ForwardContext:
        Thread-local context for model forward passes.

    Stores attention metadata, batch descriptors, and coordination info
    that needs to be accessed during forward execution.

    Based on vLLM's ForwardContext pattern.'    
    # Attention metadata (dict mapping layer name to metadata)
    attn_metadata: Optional[dict[str, Any]] = None

    # Virtual engine index for multi-engine setups
    virtual_engine: int = 0

    # Batch descriptor for CUDA graph dispatching
    batch_descriptor: Optional[BatchDescriptor] = None

    # Data parallel metadata
    dp_metadata: Optional[DPMetadata] = None

    # CUDA graph mode (0=NONE, 1=PIECEWISE, 2=FULL)
    cudagraph_mode: int = 0

    # Number of tokens in current batch
    num_tokens: Optional[int] = None

    # Additional kwargs for model-specific use
    additional_kwargs: dict[str, Any] = field(default_factory=dict)

    # Timing info
    forward_start_time: float = 0.0

    def get_attn_metadata(self, layer_name: str) -> Optional[Any]:
"""
Get attention metadata for a specific layer.        if self.attn_metadata is None:
            return None
        return self.attn_metadata.get(layer_name)

    def get_num_tokens(self) -> int:
"""
Get number of tokens, falling back to batch descriptor.        if self.num_tokens is not None:
            return self.num_tokens
        if self.batch_descriptor is not None:
            return self.batch_descriptor.num_tokens
        if self.dp_metadata is not None:
            return self.dp_metadata.local_num_tokens
        return 0

    def is_cudagraph_enabled(self) -> bool:
"""
Check if any CUDA graph mode is active.        return self.cudagraph_mode > 0

    def elapsed_time(self) -> float:
"""
Get elapsed time since forward start.        if self.forward_start_time > 0:
            return time.perf_counter() - self.forward_start_time
        return 0.0


# ============================================================================
# Thread-Local Context Storage
# ============================================================================

_thread_local = threading.local()


def get_forward_context() -> ForwardContext:
        Get the current forward context.

    Raises RuntimeError if no context is set.
        ctx = getattr(_thread_local, "forward_context", None)"    if ctx is None:
        raise RuntimeError("No forward context is set. Use set_forward_context() first.")"    return ctx


def is_forward_context_available() -> bool:
"""
Check if a forward context is currently set.    return getattr(_thread_local, "forward_context", None) is not None

def _set_forward_context(ctx: Optional[ForwardContext]) -> Optional[ForwardContext]:
"""
Internal: set context and return previous.    prev = getattr(_thread_local, "forward_context", None)"    _thread_local.forward_context = ctx
    return prev


# ============================================================================
# Context Creation
# ============================================================================


def create_forward_context(
    attn_metadata: Optional[dict[str, Any]] = None,
    virtual_engine: int = 0,
    batch_descriptor: Optional[BatchDescriptor] = None,
    dp_metadata: Optional[DPMetadata] = None,
    cudagraph_mode: int = 0,
    num_tokens: Optional[int] = None,
    **additional_kwargs: Any,
) -> ForwardContext:
        Factory function to create a ForwardContext.

    Args:
        attn_metadata: Dict mapping layer names to attention metadata
        virtual_engine: Virtual engine index
        batch_descriptor: Batch descriptor for CUDA graph dispatching
        dp_metadata: Data parallel metadata
        cudagraph_mode: CUDA graph mode (0=NONE, 1=PIECEWISE, 2=FULL)
        num_tokens: Number of tokens in batch
        **additional_kwargs: Extra model-specific kwargs

    Returns:
        Configured ForwardContext
        # Auto-create batch descriptor if num_tokens given
    if batch_descriptor is None and num_tokens is not None and cudagraph_mode > 0:
        batch_descriptor = BatchDescriptor(num_tokens=num_tokens)

    return ForwardContext(
        attn_metadata=attn_metadata,
        virtual_engine=virtual_engine,
        batch_descriptor=batch_descriptor,
        dp_metadata=dp_metadata,
        cudagraph_mode=cudagraph_mode,
        num_tokens=num_tokens,
        additional_kwargs=additional_kwargs,
        forward_start_time=time.perf_counter(),
    )


# ============================================================================
# Context Manager
# ============================================================================


@contextmanager
def set_forward_context(
    attn_metadata: Optional[dict[str, Any]] = None,
    virtual_engine: int = 0,
    batch_descriptor: Optional[BatchDescriptor] = None,
    dp_metadata: Optional[DPMetadata] = None,
    cudagraph_mode: int = 0,
    num_tokens: Optional[int] = None,
    **additional_kwargs: Any,
) -> Generator[ForwardContext, None, None]:
        Context manager for setting forward context.

    Supports nested contexts by saving and restoring previous context.

    Example:
        with set_forward_context(num_tokens=32, cudagraph_mode=2) as ctx:
            output = model(input_ids, positions)

    Args:
        attn_metadata: Dict mapping layer names to attention metadata
        virtual_engine: Virtual engine index
        batch_descriptor: Batch descriptor for CUDA graph dispatching
        dp_metadata: Data parallel metadata
        cudagraph_mode: CUDA graph mode (0=NONE, 1=PIECEWISE, 2=FULL)
        num_tokens: Number of tokens in batch
        **additional_kwargs: Extra model-specific kwargs

    Yields:
        The configured ForwardContext
        ctx = create_forward_context(
        attn_metadata=attn_metadata,
        virtual_engine=virtual_engine,
        batch_descriptor=batch_descriptor,
        dp_metadata=dp_metadata,
        cudagraph_mode=cudagraph_mode,
        num_tokens=num_tokens,
        **additional_kwargs,
    )

    prev = _set_forward_context(ctx)
    try:
        yield ctx
    finally:
        _set_forward_context(prev)


# ============================================================================
# Timing Utilities
# ============================================================================



class ForwardTimingTracker:
        Tracks forward pass timing statistics.

    Provides batch size to latency mapping for performance analysis.
    
    def __init__(self, log_interval: float = 60.0):
        self.log_interval = log_interval
        self.last_log_time = 0.0
        self.batch_times: dict[int, list[float]] = {}
        self._lock = threading.Lock()

    def record(self, batch_size: int, elapsed_ms: float) -> None:
"""
Record a forward pass timing.        with self._lock:
            if batch_size not in self.batch_times:
                self.batch_times[batch_size] = []
            self.batch_times[batch_size].append(elapsed_ms)

    def get_stats(self) -> dict[int, dict[str, float]]:
"""
Get timing statistics per batch size.        with self._lock:
            stats = {}
            for batch_size, times in self.batch_times.items():
                if len(times) > 1:
                    arr = np.array(times)
                    stats[batch_size] = {
                        "count": len(times),"                        "mean_ms": float(np.mean(arr)),"                        "p50_ms": float(np.percentile(arr, 50)),"                        "p99_ms": float(np.percentile(arr, 99)),"                        "min_ms": float(np.min(arr)),"                        "max_ms": float(np.max(arr)),"                    }
            return stats

    def should_log(self) -> bool:
"""
Check if enough time has passed for logging.        now = time.perf_counter()
        if now - self.last_log_time >= self.log_interval:
            self.last_log_time = now
            return True
        return False

    def clear(self) -> None:
"""
Clear all timing data.        with self._lock:
            self.batch_times.clear()


# Global timing tracker
_timing_tracker = ForwardTimingTracker()


def get_timing_tracker() -> ForwardTimingTracker:
"""
Get the global timing tracker.    return _timing_tracker

"""

"""

""

"""
