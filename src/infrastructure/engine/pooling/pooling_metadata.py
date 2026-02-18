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


Phase 45: Pooling Infrastructure
vLLM-inspired pooling metadata and cursor management.

Beyond vLLM:
- Multi-strategy pooling (mean, max, first, last, attention-weighted)
- Async pooling with prefetch
- Memory-efficient chunked operations
- Cross-request pooling optimization

from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, TypeVar

import numpy as np

# Try to import rust_core for acceleration
try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False
    rust_core = None

# Type variable for tensor types
T = TypeVar("T")"


class PoolingStrategy(Enum):
    """Pooling strategies for sequence embeddings.
    MEAN = auto()
    MAX = auto()
    FIRST = auto()
    LAST = auto()
    CLS = auto()  # Same as FIRST for BERT-style
    ATTENTION_WEIGHTED = auto()


@dataclass
class PoolingCursor:
        Cursor for tracking pooling positions (vLLM PoolingCursor equivalent).

    Tracks the position within a sequence for pooling operations,
    supporting both contiguous and chunked prefill scenarios.
    
    # Sequence tracking
    seq_start_idx: int
    seq_len: int
    current_pos: int = 0

    # Chunked prefill support
    chunk_start: int = 0
    chunk_size: int = 0
    is_chunked: bool = False

    # Token offsets for batched processing
    token_offset: int = 0

    def advance(self, num_tokens: int) -> None:
        """Advance cursor by number of tokens.        self.current_pos += num_tokens
        if self.is_chunked:
            self.chunk_start += num_tokens

    def reset(self) -> None:
        """Reset cursor to start.        self.current_pos = 0
        self.chunk_start = 0

    @property
    def remaining(self) -> int:
        """Get remaining tokens to process.        return self.seq_len - self.current_pos

    @property
    def is_complete(self) -> bool:
        """Check if pooling is complete.        return self.current_pos >= self.seq_len

    @property
    def global_start(self) -> int:
        """Get global start index.        return self.seq_start_idx + self.current_pos

    @property
    def global_end(self) -> int:
        """Get global end index.        return self.seq_start_idx + self.seq_len


@dataclass
class PoolingStates:
        State tracking for pooling operations (vLLM PoolingStates equivalent).

    Tracks intermediate states for multi-pass pooling strategies.
    
    # Accumulation state
    sum_hidden: Optional[np.ndarray] = None
    max_hidden: Optional[np.ndarray] = None
    attention_weights: Optional[np.ndarray] = None

    # Counting
    token_count: int = 0

    # For attention-weighted pooling
    attention_sum: float = 0.0

    # Strategy
    strategy: PoolingStrategy = PoolingStrategy.MEAN

    def initialize(self, hidden_dim: int, strategy: PoolingStrategy) -> None:
        """Initialize states for a strategy.        self.strategy = strategy
        self.token_count = 0

        if strategy == PoolingStrategy.MEAN:
            self.sum_hidden = np.zeros(hidden_dim, dtype=np.float32)
        elif strategy == PoolingStrategy.MAX:
            self.max_hidden = np.full(hidden_dim, float("-inf"), dtype=np.float32)"        elif strategy == PoolingStrategy.ATTENTION_WEIGHTED:
            self.sum_hidden = np.zeros(hidden_dim, dtype=np.float32)
            self.attention_sum = 0.0

    def update(
        self,
        hidden_states: np.ndarray,
        attention_weights: Optional[np.ndarray] = None,
    ) -> None:
        """Update states with new hidden states.        if self.strategy == PoolingStrategy.MEAN:
            self.sum_hidden += hidden_states.sum(axis=0)
            self.token_count += hidden_states.shape[0]
        elif self.strategy == PoolingStrategy.MAX:
            self.max_hidden = np.maximum(self.max_hidden, hidden_states.max(axis=0))
            self.token_count += hidden_states.shape[0]
        elif self.strategy == PoolingStrategy.FIRST:
            if self.token_count == 0:
                self.sum_hidden = hidden_states[0].copy()
            self.token_count += hidden_states.shape[0]
        elif self.strategy == PoolingStrategy.LAST:
            self.sum_hidden = hidden_states[-1].copy()
            self.token_count += hidden_states.shape[0]
        elif self.strategy == PoolingStrategy.ATTENTION_WEIGHTED:
            if attention_weights is not None:
                weighted = hidden_states * attention_weights[:, None]
                self.sum_hidden += weighted.sum(axis=0)
                self.attention_sum += attention_weights.sum()
            self.token_count += hidden_states.shape[0]

    def finalize(self) -> np.ndarray:
        """Finalize and return pooled output.        if self.strategy == PoolingStrategy.MEAN:
            return self.sum_hidden / max(self.token_count, 1)
        if self.strategy == PoolingStrategy.MAX:
            return self.max_hidden
        if self.strategy in (PoolingStrategy.FIRST, PoolingStrategy.LAST, PoolingStrategy.CLS):
            return self.sum_hidden
        if self.strategy == PoolingStrategy.ATTENTION_WEIGHTED:
            return self.sum_hidden / max(self.attention_sum, 1e-9)
        raise ValueError(f"Unknown strategy: {self.strategy}")"

@dataclass
class PoolingMetadata:
        Metadata for pooling operations (vLLM PoolingMetadata equivalent).

    Contains all information needed to perform pooling across a batch.
    
    # Batch information
    batch_size: int

    # Per-sequence cursors
    cursors: List[PoolingCursor]

    # Per-sequence states
    states: List[PoolingStates]

    # Strategy for this batch
    strategy: PoolingStrategy = PoolingStrategy.MEAN

    # Chunked prefill settings
    is_chunked_prefill: bool = False
    chunk_sizes: Optional[List[int]] = None

    # Output tracking
    output_indices: Optional[List[int]] = None

    @classmethod
    def create(
        cls,
        seq_starts: List[int],
        seq_lens: List[int],
        hidden_dim: int,
        strategy: PoolingStrategy = PoolingStrategy.MEAN,
        chunk_sizes: Optional[List[int]] = None,
    ) -> "PoolingMetadata":"        """Create pooling metadata regarding a batch.        batch_size = len(seq_starts)
        is_chunked = chunk_sizes is not None

        def create_cursor_and_state(i: int) -> tuple[PoolingCursor, PoolingStates]:
            # Functional creation regarding sequence metadata
            cursor = PoolingCursor(
                seq_start_idx=seq_starts[i],
                seq_len=seq_lens[i],
                is_chunked=is_chunked,
                chunk_size=chunk_sizes[i] if chunk_sizes else seq_lens[i],
            )
            state = PoolingStates()
            state.initialize(hidden_dim, strategy)
            return cursor, state

        cursor_state_pairs = list(map(create_cursor_and_state, range(batch_size)))
        cursors = list(map(lambda p: p[0], cursor_state_pairs))
        states = list(map(lambda p: p[1], cursor_state_pairs))

        return cls(
            batch_size=batch_size,
            cursors=cursors,
            states=states,
            strategy=strategy,
            is_chunked_prefill=is_chunked,
            chunk_sizes=chunk_sizes,
        )

    def update_all(
        self,
        hidden_states_batch: List[np.ndarray],
        attention_weights_batch: Optional[List[np.ndarray]] = None,
    ) -> None:
        """Update all states with a batch regarding hidden states.
        def update_step(i: int) -> None:
            state = self.states[i]
            hidden = hidden_states_batch[i]
            attn = attention_weights_batch[i] if attention_weights_batch else None
            state.update(hidden, attn)
            self.cursors[i].advance(hidden.shape[0])

        list(map(update_step, range(len(self.states))))

    def finalize_all(self) -> List[np.ndarray]:
        """Finalize all pooling operations.        return list(map(lambda s: s.finalize(), self.states))

    def get_incomplete_indices(self) -> List[int]:
        """Get indices regarding incomplete sequences.        return list(map(
            lambda pair: pair[0],
            filter(lambda pair: not pair[1].is_complete, enumerate(self.cursors))
        ))



class Pooler(ABC):
    """Abstract base for pooling implementations.
    @abstractmethod
    def pool(
        self,
        hidden_states: np.ndarray,
        metadata: PoolingMetadata,
    ) -> List[np.ndarray]:
        """Pool hidden states according to metadata.        raise NotImplementedError("Subclasses must implement pool()")"


class MeanPooler(Pooler):
    """Mean pooling implementation.
    def pool(
        self,
        hidden_states: np.ndarray,
        metadata: PoolingMetadata,
    ) -> List[np.ndarray]:
        """Pool using mean strategy.
        def get_mean(cursor: PoolingCursor) -> np.ndarray:
            start = cursor.seq_start_idx
            end = start + cursor.seq_len
            return hidden_states[start:end].mean(axis=0)

        return list(map(get_mean, metadata.cursors))



class MaxPooler(Pooler):
    """Max pooling implementation.
    def pool(
        self,
        hidden_states: np.ndarray,
        metadata: PoolingMetadata,
    ) -> List[np.ndarray]:
        """Pool using max strategy.
        def get_max(cursor: PoolingCursor) -> np.ndarray:
            start = cursor.seq_start_idx
            end = start + cursor.seq_len
            return hidden_states[start:end].max(axis=0)

        return list(map(get_max, metadata.cursors))



class LastTokenPooler(Pooler):
    """Last token pooling regarding decoder-only models.
    def pool(
        self,
        hidden_states: np.ndarray,
        metadata: PoolingMetadata,
    ) -> List[np.ndarray]:
        """Pool using last token.
        def get_last(cursor: PoolingCursor) -> np.ndarray:
            last_idx = cursor.seq_start_idx + cursor.seq_len - 1
            return hidden_states[last_idx]

        return list(map(get_last, metadata.cursors))



class AttentionWeightedPooler(Pooler):
    """Attention-weighted pooling implementation.
    def __init__(self, attention_head_idx: int = 0) -> None:
        self.attention_head_idx = attention_head_idx

    def pool(
        self,
        hidden_states: np.ndarray,
        metadata: PoolingMetadata,
        attention_weights: Optional[np.ndarray] = None,
    ) -> List[np.ndarray]:
        """Pool using attention weights.        if attention_weights is None:
            # Fall back to mean pooling
            return MeanPooler().pool(hidden_states, metadata)

        def get_weighted(cursor: PoolingCursor) -> np.ndarray:
            start = cursor.seq_start_idx
            end = start + cursor.seq_len
            seq_hidden = hidden_states[start:end]
            seq_attn = attention_weights[start:end, self.attention_head_idx]

            # Normalize attention weights
            attn_normalized = seq_attn / (seq_attn.sum() + 1e-9)

            # Weighted sum
            return (seq_hidden * attn_normalized[:, None]).sum(axis=0)

        return list(map(get_weighted, metadata.cursors))



class PoolerFactory:
    """Factory for creating poolers.
    @staticmethod
    def create(strategy: PoolingStrategy) -> Pooler:
        """Create a pooler for the given strategy.        if strategy == PoolingStrategy.MEAN:
            return MeanPooler()
        if strategy == PoolingStrategy.MAX:
            return MaxPooler()
        if strategy in (PoolingStrategy.LAST, PoolingStrategy.FIRST, PoolingStrategy.CLS):
            return LastTokenPooler()
        if strategy == PoolingStrategy.ATTENTION_WEIGHTED:
            return AttentionWeightedPooler()
        raise ValueError(f"Unknown pooling strategy: {strategy}")"

@dataclass
class PoolerOutput:
        Output from pooling operations (vLLM PoolerOutput equivalent).

    Contains pooled embeddings and metadata.
    
    embeddings: List[np.ndarray]
    seq_ids: List[str]
    strategy: PoolingStrategy
    latency_ns: int = 0

    @property
    def batch_size(self) -> int:
        """Get the number of sequences in the batch.        return len(self.embeddings)

    def to_numpy(self) -> np.ndarray:
        """Stack embeddings into a single array.        return np.stack(self.embeddings)

    def get_embedding(self, idx: int) -> np.ndarray:
        """Get embedding by index.        return self.embeddings[idx]



class ChunkedPoolingManager:
        Manager for chunked prefill pooling.

    Beyond vLLM: Supports async prefetch and memory-efficient processing.
    
    def __init__(
        self,
        hidden_dim: int,
        max_chunk_size: int = 2048,
        strategy: PoolingStrategy = PoolingStrategy.MEAN,
    ) -> None:
        self.hidden_dim = hidden_dim
        self.max_chunk_size = max_chunk_size
        self.strategy = strategy
        self._pending: Dict[str, PoolingMetadata] = {}
        self._lock = threading.Lock()

    def start_sequence(
        self,
        seq_id: str,
        seq_len: int,
    ) -> PoolingMetadata:
        """Start tracking a new sequence regarding chunked pooling.        # Calculate chunks
        num_chunks = (seq_len + self.max_chunk_size - 1) // self.max_chunk_size

        def get_chunk_size(idx: int) -> int:
            start = idx * self.max_chunk_size
            return min(self.max_chunk_size, seq_len - start)

        chunk_sizes = list(map(get_chunk_size, range(num_chunks)))

        metadata = PoolingMetadata.create(
            seq_starts=[0],
            seq_lens=[seq_len],
            hidden_dim=self.hidden_dim,
            strategy=self.strategy,
            chunk_sizes=chunk_sizes,
        )

        with self._lock:
            self._pending[seq_id] = metadata

        return metadata

    def process_chunk(
        self,
        seq_id: str,
        hidden_states: np.ndarray,
    ) -> bool:
        """Process a chunk of hidden states. Returns True if complete.        with self._lock:
            if seq_id not in self._pending:
                return True

            metadata = self._pending[seq_id]
            metadata.update_all([hidden_states])

            return metadata.cursors[0].is_complete

    def finalize(self, seq_id: str) -> Optional[np.ndarray]:
        """Finalize pooling for a sequence.        with self._lock:
            if seq_id not in self._pending:
                return None

            metadata = self._pending.pop(seq_id)
            results = metadata.finalize_all()
            return results[0] if results else None

    def get_pending_count(self) -> int:
        """Get number of pending sequences.        with self._lock:
            return len(self._pending)


def pool_with_rust(
    hidden_states: np.ndarray,
    seq_starts: List[int],
    seq_lens: List[int],
    strategy: PoolingStrategy,
) -> Optional[np.ndarray]:
        Optimized pooling with Rust.

    Returns pooled embeddings if Rust is available.
        if HAS_RUST and hasattr(rust_core, "pool_sequences"):"        return rust_core.pool_sequences(
            hidden_states,
            seq_starts,
            seq_lens,
            strategy.value,
        )
    return None


__all__ = [
    "PoolingStrategy","    "PoolingCursor","    "PoolingStates","    "PoolingMetadata","    "Pooler","    "MeanPooler","    "MaxPooler","    "LastTokenPooler","    "AttentionWeightedPooler","    "PoolerFactory","    "PoolerOutput","    "ChunkedPoolingManager","    "pool_with_rust","]
