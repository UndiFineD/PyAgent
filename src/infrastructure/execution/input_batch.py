"""
InputBatch.py - Structured batch management for model execution.

Inspired by vLLM's v1/worker/gpu/input_batch.py. Provides pre-allocated
buffers and structured batch state for efficient model execution.

Phase 29: Execution Context, Batching & Async Streaming
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict, Sequence

import numpy as np


# ============================================================================
# Sampling Metadata
# ============================================================================

@dataclass
class SamplingMetadata:
    """
    Per-request sampling parameters for batched sampling.
    
    Based on vLLM's SamplingMetadata pattern.
    """
    # Per-request parameters (arrays of length num_reqs)
    temperature: np.ndarray  # [num_reqs]
    top_k: np.ndarray  # [num_reqs]
    top_p: np.ndarray  # [num_reqs]
    min_p: np.ndarray  # [num_reqs]
    
    # Penalty parameters
    repetition_penalty: np.ndarray  # [num_reqs]
    presence_penalty: np.ndarray  # [num_reqs]
    frequency_penalty: np.ndarray  # [num_reqs]
    
    # Output token IDs for penalty computation (list of lists)
    output_token_ids: Optional[List[List[int]]] = None
    
    # Prompt token IDs for cross-entropy loss (optional)
    prompt_token_ids: Optional[List[List[int]]] = None
    
    # Stop conditions
    stop_token_ids: Optional[List[set]] = None
    
    # Flags
    all_greedy: bool = False
    all_random: bool = False
    
    @classmethod
    def from_defaults(cls, num_reqs: int) -> "SamplingMetadata":
        """Create with default sampling parameters."""
        return cls(
            temperature=np.ones(num_reqs, dtype=np.float32),
            top_k=np.full(num_reqs, -1, dtype=np.int32),  # -1 = disabled
            top_p=np.ones(num_reqs, dtype=np.float32),
            min_p=np.zeros(num_reqs, dtype=np.float32),
            repetition_penalty=np.ones(num_reqs, dtype=np.float32),
            presence_penalty=np.zeros(num_reqs, dtype=np.float32),
            frequency_penalty=np.zeros(num_reqs, dtype=np.float32),
            output_token_ids=[[] for _ in range(num_reqs)],
            all_greedy=False,
            all_random=True,
        )
    
    @classmethod
    def from_params(
        cls,
        temperatures: Sequence[float],
        top_ks: Sequence[int],
        top_ps: Sequence[float],
        min_ps: Optional[Sequence[float]] = None,
        repetition_penalties: Optional[Sequence[float]] = None,
        presence_penalties: Optional[Sequence[float]] = None,
        frequency_penalties: Optional[Sequence[float]] = None,
    ) -> "SamplingMetadata":
        """Create from per-request parameters."""
        num_reqs = len(temperatures)
        
        return cls(
            temperature=np.array(temperatures, dtype=np.float32),
            top_k=np.array(top_ks, dtype=np.int32),
            top_p=np.array(top_ps, dtype=np.float32),
            min_p=np.array(min_ps, dtype=np.float32) if min_ps else np.zeros(num_reqs, dtype=np.float32),
            repetition_penalty=np.array(repetition_penalties, dtype=np.float32) if repetition_penalties else np.ones(num_reqs, dtype=np.float32),
            presence_penalty=np.array(presence_penalties, dtype=np.float32) if presence_penalties else np.zeros(num_reqs, dtype=np.float32),
            frequency_penalty=np.array(frequency_penalties, dtype=np.float32) if frequency_penalties else np.zeros(num_reqs, dtype=np.float32),
            output_token_ids=[[] for _ in range(num_reqs)],
            all_greedy=all(t == 0.0 for t in temperatures),
            all_random=all(t > 0.0 for t in temperatures),
        )
    
    @property
    def num_reqs(self) -> int:
        """Get number of requests."""
        return len(self.temperature)
    
    def slice(self, start: int, end: int) -> "SamplingMetadata":
        """Get a slice of the metadata."""
        return SamplingMetadata(
            temperature=self.temperature[start:end],
            top_k=self.top_k[start:end],
            top_p=self.top_p[start:end],
            min_p=self.min_p[start:end],
            repetition_penalty=self.repetition_penalty[start:end],
            presence_penalty=self.presence_penalty[start:end],
            frequency_penalty=self.frequency_penalty[start:end],
            output_token_ids=self.output_token_ids[start:end] if self.output_token_ids else None,
            prompt_token_ids=self.prompt_token_ids[start:end] if self.prompt_token_ids else None,
            stop_token_ids=self.stop_token_ids[start:end] if self.stop_token_ids else None,
        )


# ============================================================================
# Input Buffers
# ============================================================================

@dataclass
class InputBuffers:
    """
    Pre-allocated tensors for batch inputs.
    
    Avoids runtime allocation during model execution.
    Based on vLLM's InputBuffers pattern.
    """
    max_num_reqs: int
    max_num_tokens: int
    
    # Core input arrays (numpy for CPU, can wrap GPU tensors)
    input_ids: np.ndarray  # [max_num_tokens]
    positions: np.ndarray  # [max_num_tokens]
    
    # Per-request metadata
    seq_lens: np.ndarray  # [max_num_reqs]
    query_start_loc: np.ndarray  # [max_num_reqs + 1]
    
    # Index mapping
    idx_mapping: np.ndarray  # [max_num_reqs] - request to output index
    
    # Optional embeddings input
    inputs_embeds: Optional[np.ndarray] = None  # [max_num_tokens, embed_dim]
    
    # Slot mapping for KV cache
    slot_mapping: Optional[np.ndarray] = None  # [max_num_tokens]
    
    # Block table for paged attention
    block_table: Optional[np.ndarray] = None  # [max_num_reqs, max_blocks]
    
    @classmethod
    def allocate(
        cls,
        max_num_reqs: int,
        max_num_tokens: int,
        embed_dim: Optional[int] = None,
        max_blocks_per_req: int = 256,
        dtype: np.dtype = np.int32,
    ) -> "InputBuffers":
        """Allocate buffers with specified sizes."""
        buffers = cls(
            max_num_reqs=max_num_reqs,
            max_num_tokens=max_num_tokens,
            input_ids=np.zeros(max_num_tokens, dtype=dtype),
            positions=np.zeros(max_num_tokens, dtype=np.int64),
            seq_lens=np.zeros(max_num_reqs, dtype=np.int32),
            query_start_loc=np.zeros(max_num_reqs + 1, dtype=np.int32),
            idx_mapping=np.arange(max_num_reqs, dtype=np.int32),
            slot_mapping=np.zeros(max_num_tokens, dtype=np.int32),
            block_table=np.zeros((max_num_reqs, max_blocks_per_req), dtype=np.int32),
        )
        
        if embed_dim is not None:
            buffers.inputs_embeds = np.zeros((max_num_tokens, embed_dim), dtype=np.float32)
        
        return buffers
    
    def reset(self) -> None:
        """Reset all buffers to zero."""
        self.input_ids.fill(0)
        self.positions.fill(0)
        self.seq_lens.fill(0)
        self.query_start_loc.fill(0)
        if self.slot_mapping is not None:
            self.slot_mapping.fill(0)
        if self.block_table is not None:
            self.block_table.fill(0)
        if self.inputs_embeds is not None:
            self.inputs_embeds.fill(0)


# ============================================================================
# Input Batch
# ============================================================================

@dataclass
class InputBatch:
    """
    Structured batch for model execution.
    
    Contains all inputs and metadata needed for a forward pass.
    Based on vLLM's InputBatch pattern.
    """
    # Request identifiers
    req_ids: List[str]
    
    # Input tensors (views into InputBuffers)
    input_ids: np.ndarray  # [num_tokens]
    positions: np.ndarray  # [num_tokens]
    
    # Sequence metadata
    seq_lens: np.ndarray  # [num_reqs]
    query_start_loc: np.ndarray  # [num_reqs + 1]
    
    # Index mapping: request index -> output logits index
    idx_mapping: np.ndarray  # [num_reqs]
    
    # Attention metadata (dict for per-layer metadata)
    attn_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Sampling metadata
    sampling_metadata: Optional[SamplingMetadata] = None
    
    # Optional inputs
    inputs_embeds: Optional[np.ndarray] = None
    slot_mapping: Optional[np.ndarray] = None
    block_table: Optional[np.ndarray] = None
    
    # Batch statistics
    num_tokens_after_padding: int = 0
    max_query_len: int = 0
    max_seq_len: int = 0
    
    # Previous state for async scheduling
    prev_req_id_to_index: Optional[Dict[str, int]] = None
    
    @property
    def num_reqs(self) -> int:
        """Get number of requests in batch."""
        return len(self.req_ids)
    
    @property
    def num_tokens(self) -> int:
        """Get total number of tokens."""
        return len(self.input_ids)
    
    @classmethod
    def make_dummy(
        cls,
        num_reqs: int,
        num_tokens: int,
        buffers: InputBuffers,
    ) -> "InputBatch":
        """
        Create a dummy batch for CUDA graph capture.
        
        Fills buffers with placeholder values.
        """
        # Fill dummy values
        buffers.input_ids[:num_tokens] = 0
        buffers.positions[:num_tokens] = np.arange(num_tokens)
        
        # Distribute tokens evenly across requests
        tokens_per_req = num_tokens // num_reqs if num_reqs > 0 else 0
        buffers.seq_lens[:num_reqs] = tokens_per_req
        
        # Compute query_start_loc
        buffers.query_start_loc[0] = 0
        for i in range(num_reqs):
            buffers.query_start_loc[i + 1] = buffers.query_start_loc[i] + tokens_per_req
        
        # Identity mapping
        buffers.idx_mapping[:num_reqs] = np.arange(num_reqs)
        
        return cls(
            req_ids=[f"dummy_{i}" for i in range(num_reqs)],
            input_ids=buffers.input_ids[:num_tokens],
            positions=buffers.positions[:num_tokens],
            seq_lens=buffers.seq_lens[:num_reqs],
            query_start_loc=buffers.query_start_loc[:num_reqs + 1],
            idx_mapping=buffers.idx_mapping[:num_reqs],
            num_tokens_after_padding=num_tokens,
            max_query_len=tokens_per_req,
            max_seq_len=tokens_per_req,
            sampling_metadata=SamplingMetadata.from_defaults(num_reqs),
        )
    
    @classmethod
    def from_requests(
        cls,
        req_ids: List[str],
        input_ids_list: List[List[int]],
        positions_list: List[List[int]],
        buffers: InputBuffers,
        sampling_metadata: Optional[SamplingMetadata] = None,
    ) -> "InputBatch":
        """
        Create a batch from a list of requests.
        
        Flattens inputs into contiguous buffers.
        """
        num_reqs = len(req_ids)
        
        # Compute offsets
        seq_lens = np.array([len(ids) for ids in input_ids_list], dtype=np.int32)
        query_start_loc = np.zeros(num_reqs + 1, dtype=np.int32)
        query_start_loc[1:] = np.cumsum(seq_lens)
        total_tokens = int(query_start_loc[-1])
        
        # Flatten inputs
        all_input_ids = []
        all_positions = []
        for ids, pos in zip(input_ids_list, positions_list):
            all_input_ids.extend(ids)
            all_positions.extend(pos)
        
        # Copy to buffers
        buffers.input_ids[:total_tokens] = all_input_ids
        buffers.positions[:total_tokens] = all_positions
        buffers.seq_lens[:num_reqs] = seq_lens
        buffers.query_start_loc[:num_reqs + 1] = query_start_loc
        buffers.idx_mapping[:num_reqs] = np.arange(num_reqs)
        
        return cls(
            req_ids=req_ids,
            input_ids=buffers.input_ids[:total_tokens],
            positions=buffers.positions[:total_tokens],
            seq_lens=buffers.seq_lens[:num_reqs],
            query_start_loc=buffers.query_start_loc[:num_reqs + 1],
            idx_mapping=buffers.idx_mapping[:num_reqs],
            num_tokens_after_padding=total_tokens,
            max_query_len=int(np.max(seq_lens)) if num_reqs > 0 else 0,
            max_seq_len=int(np.max(seq_lens)) if num_reqs > 0 else 0,
            sampling_metadata=sampling_metadata or SamplingMetadata.from_defaults(num_reqs),
        )
    
    def get_req_index(self, req_id: str) -> Optional[int]:
        """Get the index of a request by ID."""
        try:
            return self.req_ids.index(req_id)
        except ValueError:
            return None
    
    def get_logits_indices(self) -> np.ndarray:
        """
        Get indices for extracting logits (last token of each sequence).
        
        Returns indices into the flattened output tensor.
        """
        # Last token of each sequence
        return self.query_start_loc[1:] - 1
    
    def get_token_range(self, req_idx: int) -> tuple[int, int]:
        """Get token range [start, end) for a request."""
        start = int(self.query_start_loc[req_idx])
        end = int(self.query_start_loc[req_idx + 1])
        return start, end
    
    def slice_request(self, req_idx: int) -> Dict[str, Any]:
        """Get inputs for a single request."""
        start, end = self.get_token_range(req_idx)
        return {
            'req_id': self.req_ids[req_idx],
            'input_ids': self.input_ids[start:end],
            'positions': self.positions[start:end],
            'seq_len': int(self.seq_lens[req_idx]),
        }


# ============================================================================
# Batch Builder
# ============================================================================

class BatchBuilder:
    """
    Builder for constructing InputBatch instances.
    
    Accumulates requests and builds batches efficiently.
    """
    
    def __init__(self, buffers: InputBuffers):
        self.buffers = buffers
        self.reset()
    
    def reset(self) -> None:
        """Reset builder state."""
        self.req_ids: List[str] = []
        self.input_ids_list: List[List[int]] = []
        self.positions_list: List[List[int]] = []
        self.temperatures: List[float] = []
        self.top_ks: List[int] = []
        self.top_ps: List[float] = []
        self._total_tokens = 0
    
    def add_request(
        self,
        req_id: str,
        input_ids: List[int],
        positions: Optional[List[int]] = None,
        temperature: float = 1.0,
        top_k: int = -1,
        top_p: float = 1.0,
    ) -> bool:
        """
        Add a request to the batch.
        
        Returns False if batch is full.
        """
        num_tokens = len(input_ids)
        
        # Check capacity
        if len(self.req_ids) >= self.buffers.max_num_reqs:
            return False
        if self._total_tokens + num_tokens > self.buffers.max_num_tokens:
            return False
        
        # Add request
        self.req_ids.append(req_id)
        self.input_ids_list.append(input_ids)
        self.positions_list.append(positions or list(range(num_tokens)))
        self.temperatures.append(temperature)
        self.top_ks.append(top_k)
        self.top_ps.append(top_p)
        self._total_tokens += num_tokens
        
        return True
    
    def build(self) -> InputBatch:
        """Build the batch."""
        sampling_metadata = SamplingMetadata.from_params(
            temperatures=self.temperatures,
            top_ks=self.top_ks,
            top_ps=self.top_ps,
        )
        
        return InputBatch.from_requests(
            req_ids=self.req_ids,
            input_ids_list=self.input_ids_list,
            positions_list=self.positions_list,
            buffers=self.buffers,
            sampling_metadata=sampling_metadata,
        )
    
    @property
    def num_reqs(self) -> int:
        """Get current number of requests."""
        return len(self.req_ids)
    
    @property
    def total_tokens(self) -> int:
        """Get current total tokens."""
        return self._total_tokens
    
    def is_empty(self) -> bool:
        """Check if builder is empty."""
        return not self.req_ids
    
    def is_full(self) -> bool:
        """Check if batch is at capacity."""
        return len(self.req_ids) >= self.buffers.max_num_reqs
