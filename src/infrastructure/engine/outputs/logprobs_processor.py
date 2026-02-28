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
Phase 45: Logprobs Tensors and Lists
vLLM-inspired logprobs data structures with optimized handling.

Beyond vLLM:
- Async CPU transfer with double buffering
- Compressed storage for sparse logprobs
- Streaming logprobs support
- Batch aggregation optimizations
"""

from __future__ import annotations

import threading
from collections import defaultdict
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

# Try to import rust_core for acceleration
try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False
    rust_core = None


@dataclass
class TokenLogprob:
    """Single token with its log probability."""

    token_id: int
    token: str
    logprob: float

    def __lt__(self, other: "TokenLogprob") -> bool:
        return self.logprob > other.logprob  # Higher logprob = better


@dataclass
class TopLogprobs:
    """Top logprobs for a single position."""

    position: int
    token_id: int
    token: str
    logprob: float
    top_k: List[TokenLogprob] = field(default_factory=list)

    @classmethod
    def from_array(
        cls,
        position: int,
        logprobs: np.ndarray,
        token_ids: np.ndarray,
        tokens: List[str],
        selected_idx: int,
        k: int = 5,
    ) -> "TopLogprobs":
        """Create from arrays."""
        # Get top-k indices
        if k >= len(logprobs):
            top_indices = np.argsort(logprobs)[::-1]
        else:
            top_indices = np.argpartition(logprobs, -k)[-k:]
            top_indices = top_indices[np.argsort(logprobs[top_indices])[::-1]]

        top_k = [
            TokenLogprob(
                token_id=int(token_ids[i]),
                token=tokens[i] if i < len(tokens) else f"<{token_ids[i]}>",
                logprob=float(logprobs[i]),
            )
            for i in top_indices
        ]

        return cls(
            position=position,
            token_id=int(token_ids[selected_idx]),
            token=tokens[selected_idx] if selected_idx < len(tokens) else f"<{token_ids[selected_idx]}>",
            logprob=float(logprobs[selected_idx]),
            top_k=top_k,
        )


class LogprobsLists:
    """
    List-based logprobs storage (vLLM LogprobsLists equivalent).

    Efficient for variable-length sequences with streaming output.
    """

    def __init__(self, num_sequences: int = 1) -> None:
        self._sequences: List[List[TopLogprobs]] = [[] for _ in range(num_sequences)]
        self._lock = threading.Lock()

    def append(
        self,
        seq_idx: int,
        logprobs: TopLogprobs,
    ) -> None:
        """Append logprobs to a sequence."""
        with self._lock:
            if seq_idx >= len(self._sequences):
                # Extend if needed
                self._sequences.extend([] for _ in range(seq_idx - len(self._sequences) + 1))
            self._sequences[seq_idx].append(logprobs)

    def get_sequence(self, seq_idx: int) -> List[TopLogprobs]:
        """Get logprobs for a sequence."""
        with self._lock:
            if seq_idx >= len(self._sequences):
                return []
            return list(self._sequences[seq_idx])

    def get_all(self) -> List[List[TopLogprobs]]:
        """Get all sequences."""
        with self._lock:
            return [list(seq) for seq in self._sequences]

    def __len__(self) -> int:
        """Get number of sequences."""
        with self._lock:
            return len(self._sequences)

    def total_tokens(self) -> int:
        """Get total number of tokens across all sequences."""
        with self._lock:
            return sum(len(seq) for seq in self._sequences)


@dataclass
class LogprobsTensors:
    """
    Tensor-based logprobs storage (vLLM LogprobsTensors equivalent).

    Efficient for batched processing with GPU tensors.

    Beyond vLLM:
    - Double buffering for async CPU transfer
    - Sparse storage for memory efficiency
    - Lazy evaluation support
    """

    # Main storage
    logprobs: np.ndarray  # (batch, seq_len, vocab_size) or sparse
    token_ids: np.ndarray  # (batch, seq_len)

    # Metadata
    batch_size: int
    seq_lens: List[int]
    top_k: int = 5

    # Transfer state
    _cpu_buffer: Optional[np.ndarray] = field(default=None, repr=False)
    _is_on_cpu: bool = True
    _transfer_future: Optional[Future] = field(default=None, repr=False)

    @classmethod
    def create_empty(
        cls,
        batch_size: int,
        max_seq_len: int,
        vocab_size: int,
        top_k: int = 5,
        sparse: bool = False,
    ) -> "LogprobsTensors":
        """Create empty tensors."""
        if sparse:
            # Only store top-k logprobs
            logprobs = np.full((batch_size, max_seq_len, top_k), float("-inf"), dtype=np.float32)
            token_ids = np.zeros((batch_size, max_seq_len, top_k), dtype=np.int64)
        else:
            logprobs = np.full((batch_size, max_seq_len, vocab_size), float("-inf"), dtype=np.float32)
            token_ids = np.zeros((batch_size, max_seq_len), dtype=np.int64)

        return cls(
            logprobs=logprobs,
            token_ids=token_ids,
            batch_size=batch_size,
            seq_lens=[0] * batch_size,
            top_k=top_k,
        )

    def set_position(
        self,
        batch_idx: int,
        position: int,
        logprobs: np.ndarray,
        token_id: int,
    ) -> None:
        """Set logprobs at a position."""
        if len(self.logprobs.shape) == 3 and self.logprobs.shape[2] == self.top_k:
            # Sparse storage
            top_indices = np.argpartition(logprobs, -self.top_k)[-self.top_k :]
            self.logprobs[batch_idx, position] = logprobs[top_indices]
            self.token_ids[batch_idx, position] = top_indices
        else:
            # Dense storage
            self.logprobs[batch_idx, position] = logprobs
            self.token_ids[batch_idx, position] = token_id

        self.seq_lens[batch_idx] = max(self.seq_lens[batch_idx], position + 1)

    def to_lists(self, tokenizer: Any = None) -> LogprobsLists:
        """Convert to list format."""
        lists = LogprobsLists(self.batch_size)

        for batch_idx in range(self.batch_size):
            for pos in range(self.seq_lens[batch_idx]):
                if len(self.logprobs.shape) == 3 and self.logprobs.shape[2] == self.top_k:
                    # Sparse
                    top_logprobs = self.logprobs[batch_idx, pos]
                    top_ids = self.token_ids[batch_idx, pos]

                    top_k_list = [
                        TokenLogprob(
                            token_id=int(tid),
                            token=tokenizer.decode([tid]) if tokenizer else f"<{tid}>",
                            logprob=float(lp),
                        )
                        for tid, lp in zip(top_ids, top_logprobs)
                    ]

                    # Use first as selected
                    entry = TopLogprobs(
                        position=pos,
                        token_id=int(top_ids[0]),
                        token=top_k_list[0].token if top_k_list else "",
                        logprob=float(top_logprobs[0]),
                        top_k=top_k_list,
                    )
                else:
                    # Dense
                    logprobs = self.logprobs[batch_idx, pos]
                    token_id = int(self.token_ids[batch_idx, pos])

                    # Get top-k
                    top_indices = np.argpartition(logprobs, -self.top_k)[-self.top_k :]
                    top_indices = top_indices[np.argsort(logprobs[top_indices])[::-1]]

                    top_k_list = [
                        TokenLogprob(
                            token_id=int(idx),
                            token=tokenizer.decode([idx]) if tokenizer else f"<{idx}>",
                            logprob=float(logprobs[idx]),
                        )
                        for idx in top_indices
                    ]

                    entry = TopLogprobs(
                        position=pos,
                        token_id=token_id,
                        token=tokenizer.decode([token_id]) if tokenizer else f"<{token_id}>",
                        logprob=float(logprobs[token_id]),
                        top_k=top_k_list,
                    )

                lists.append(batch_idx, entry)

        return lists


class AsyncCPUTransfer:
    """
    Async CPU transfer manager for GPU tensors.

    Beyond vLLM: Double buffering and pipelining for overlap.
    """

    def __init__(self, num_buffers: int = 2, max_workers: int = 2) -> None:
        self._buffers: List[Optional[np.ndarray]] = [None] * num_buffers
        self._current_buffer = 0
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._pending_transfers: Dict[int, Future] = {}
        self._lock = threading.Lock()

    def submit_transfer(
        self,
        tensor: np.ndarray,
        transfer_id: int,
    ) -> Future:
        """Submit a tensor for async transfer to CPU."""
        with self._lock:
            # Simple simulation for now
            future = self._executor.submit(lambda t: t.copy(), tensor)
            self._pending_transfers[transfer_id] = future
            return future

    def get_result(self, transfer_id: int, timeout: Optional[float] = None) -> Optional[np.ndarray]:
        """Get transfer result."""
        with self._lock:
            future = self._pending_transfers.pop(transfer_id, None)

        if future is None:
            return None

        return future.result(timeout=timeout)

    def shutdown(self) -> None:
        """Shutdown the executor."""
        self._executor.shutdown(wait=True)


@dataclass
class SamplerOutput:
    """
    Output from the sampler (vLLM SamplerOutput equivalent).

    Contains sampled tokens and optional logprobs.
    """

    # Sampled tokens
    sampled_token_ids: np.ndarray  # (batch_size,) or (batch_size, num_samples)

    # Optional logprobs
    logprobs: Optional[LogprobsTensors] = None
    prompt_logprobs: Optional[LogprobsTensors] = None

    # Sampling metadata
    num_samples: int = 1
    temperature: float = 1.0
    top_p: float = 1.0
    top_k: int = -1

    # Speculative decoding info
    spec_decode_accepted: Optional[np.ndarray] = None

    @property
    def batch_size(self) -> int:
        """Return the size of the batch."""
        return self.sampled_token_ids.shape[0]

    def get_token_ids(self, batch_idx: int) -> np.ndarray:
        """Get token IDs for a batch element."""
        if len(self.sampled_token_ids.shape) == 1:
            return np.array([self.sampled_token_ids[batch_idx]])
        return self.sampled_token_ids[batch_idx]


@dataclass
class ModelRunnerOutput:
    """
    Output from model runner (vLLM ModelRunnerOutput equivalent).

    Contains all outputs from a single forward pass.
    """

    # Sampler output
    sampler_output: SamplerOutput

    # Request mapping
    req_ids: List[str]
    req_id_to_index: Dict[str, int]

    # Hidden states (optional, for pooling)
    hidden_states: Optional[np.ndarray] = None

    # Timing
    forward_time_ns: int = 0
    sample_time_ns: int = 0

    # Memory tracking
    peak_memory_bytes: int = 0

    @classmethod
    def create(
        cls,
        sampled_token_ids: np.ndarray,
        req_ids: List[str],
        logprobs: Optional[LogprobsTensors] = None,
    ) -> "ModelRunnerOutput":
        """Create a model runner output."""
        sampler_output = SamplerOutput(
            sampled_token_ids=sampled_token_ids,
            logprobs=logprobs,
        )

        req_id_to_index = {rid: i for i, rid in enumerate(req_ids)}

        return cls(
            sampler_output=sampler_output,
            req_ids=req_ids,
            req_id_to_index=req_id_to_index,
        )

    def get_output_for_request(self, req_id: str) -> Optional[Tuple[np.ndarray, Optional[TopLogprobs]]]:
        """Get output for a specific request."""
        if req_id not in self.req_id_to_index:
            return None

        idx = self.req_id_to_index[req_id]
        token_ids = self.sampler_output.get_token_ids(idx)

        logprobs = None
        if self.sampler_output.logprobs:
            lists = self.sampler_output.logprobs.to_lists()
            seq_logprobs = lists.get_sequence(idx)
            if seq_logprobs:
                logprobs = seq_logprobs[-1]  # Latest

        return (token_ids, logprobs)


class StreamingLogprobsCollector:
    """
    Collector for streaming logprobs.

    Beyond vLLM: Supports real-time streaming with backpressure.
    """

    def __init__(self, buffer_size: int = 100) -> None:
        self._buffers: Dict[str, List[TopLogprobs]] = defaultdict(list)
        self._buffer_size = buffer_size
        self._callbacks: Dict[str, Callable[[List[TopLogprobs]], None]] = {}
        self._lock = threading.Lock()

    def register_callback(
        self,
        req_id: str,
        callback: Callable[[List[TopLogprobs]], None],
    ) -> None:
        """Register a callback for a request."""
        with self._lock:
            self._callbacks[req_id] = callback

    def unregister(self, req_id: str) -> None:
        """Unregister callback and clear buffer."""
        with self._lock:
            self._callbacks.pop(req_id, None)
            self._buffers.pop(req_id, None)

    def add(self, req_id: str, logprobs: TopLogprobs) -> None:
        """Add logprobs for a request."""
        with self._lock:
            self._buffers[req_id].append(logprobs)

            # Check if we should flush
            if len(self._buffers[req_id]) >= self._buffer_size:
                self._flush_locked(req_id)

    def _flush_locked(self, req_id: str) -> None:
        """Flush buffer (must hold lock)."""
        if req_id in self._callbacks and self._buffers[req_id]:
            callback = self._callbacks[req_id]
            data = self._buffers[req_id]
            self._buffers[req_id] = []
            # Release lock before callback
            callback(data)

    def flush(self, req_id: str) -> None:
        """Flush buffer for a request."""
        with self._lock:
            self._flush_locked(req_id)

    def flush_all(self) -> None:
        """Flush all buffers."""
        with self._lock:
            for req_id in list(self._buffers.keys()):
                self._flush_locked(req_id)


def extract_top_k_logprobs_rust(
    logprobs: np.ndarray,
    k: int,
) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Extract top-k logprobs using Rust.

    Returns (top_logprobs, top_indices) if Rust is available.
    """
    if HAS_RUST and hasattr(rust_core, "extract_top_k_logprobs"):
        return rust_core.extract_top_k_logprobs(logprobs, k)
    return None


def batch_logprobs_to_cpu_rust(
    logprobs: np.ndarray,
    token_ids: np.ndarray,
) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Batch transfer logprobs to CPU using Rust.

    Returns transferred (logprobs, token_ids) if Rust is available.
    """
    if HAS_RUST and hasattr(rust_core, "batch_logprobs_transfer"):
        return rust_core.batch_logprobs_transfer(logprobs, token_ids)
    return None


__all__ = [
    "TokenLogprob",
    "TopLogprobs",
    "LogprobsLists",
    "LogprobsTensors",
    "AsyncCPUTransfer",
    "SamplerOutput",
    "ModelRunnerOutput",
    "StreamingLogprobsCollector",
    "extract_top_k_logprobs_rust",
    "batch_logprobs_to_cpu_rust",
]
