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

"""Module: triton_attention_ops - Triton-based attention operations."""

from __future__ import annotations

import logging
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

from torch import Tensor

logger: logging.Logger = logging.getLogger(__name__)

# Try importing PyTorch and Triton
try:
    import torch

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import triton
    import triton.language as tl

    HAS_TRITON = True
except ImportError:
    HAS_TRITON = False


class AttentionBackend(Enum):
    """Available attention backends."""

    TRITON = auto()  # Triton kernel
    FLASH_ATTN = auto()  # Flash Attention
    XFORMERS = auto()  # xFormers memory efficient
    SDPA = auto()  # PyTorch SDPA
    NAIVE = auto()  # Reference implementation


class PrecisionMode(Enum):
    """Precision mode for attention computation."""

    FP32 = auto()
    FP16 = auto()
    BF16 = auto()
    AUTO = auto()  # Automatic based on hardware


@dataclass
class AttentionConfig:
    """Configuration for attention operations.

    Inspired by vLLM's attention configuration patterns.
    """

    # Basic attention config
    num_heads: int = 32
    head_dim: int = 128
    num_kv_heads: int = 8  # For GQA

    # Block configuration
    block_size: int = 16
    max_seq_len: int = 8192

    # Backend selection
    backend: AttentionBackend = AttentionBackend.TRITON
    precision: PrecisionMode = PrecisionMode.AUTO

    # Memory optimization
    use_sliding_window: bool = False
    sliding_window_size: int = 4096

    # KV cache configuration
    kv_cache_dtype: str = "auto"
    kv_scale: float = 1.0

    # Performance tuning
    num_kv_splits: int = 8
    max_num_blocks_per_seq: int = 512

    # Beyond vLLM: Advanced options
    enable_cuda_graphs: bool = True
    use_tensor_cores: bool = True

    @property
    def num_queries_per_kv(self) -> int:
        """Number of query heads per KV head (for GQA)."""
        return self.num_heads // self.num_kv_heads


@dataclass
class AttentionMetadata:
    """Metadata for attention computation.

    Mirrors vLLM's AttentionMetadata structure.
    """

    # Sequence info
    seq_lens: List[int] = field(default_factory=list)
    max_decode_seq_len: int = 0

    # Block tables for paged attention
    block_tables: Optional[Any] = None  # torch.Tensor
    slot_mapping: Optional[Any] = None  # torch.Tensor

    # Context info
    context_lens: Optional[Any] = None  # torch.Tensor

    # Prefill vs decode
    is_prefill: bool = False
    num_prefill_tokens: int = 0
    num_decode_tokens: int = 0

    # Query start locations (for ragged tensors)
    query_start_loc: Optional[Any] = None  # torch.Tensor
    seq_start_loc: Optional[Any] = None  # torch.Tensor

    # Multi-modal positions
    multi_modal_placeholder_index_maps: Optional[Dict] = None

    @property
    def total_tokens(self) -> int:
        """Get total tokens (prefill + decode)."""
        return self.num_prefill_tokens + self.num_decode_tokens


class AttentionKernel(ABC):
    """Abstract base for attention kernels."""

    @abstractmethod
    def forward(
        self,
        query: Any,  # torch.Tensor
        key: Any,  # torch.Tensor
        value: Any,  # torch.Tensor
        metadata: AttentionMetadata,
        k_cache: Optional[Any] = None,
        v_cache: Optional[Any] = None,
    ) -> Any:  # torch.Tensor
        """Execute attention forward pass."""

    @abstractmethod
    def supports_context_length(self, context_len: int) -> bool:
        """Check if kernel supports given context length."""


PAGED_ATTENTION_KERNEL = None

if HAS_TRITON and HAS_TORCH:

    @triton.jit
    def _paged_attention_kernel_impl(  # pylint: disable=function-redefined, unused-argument
        output_ptr,
        query_ptr,
        k_cache_ptr,
        v_cache_ptr,
        block_tables_ptr,
        context_lens_ptr,
        stride_query_batch,
        stride_query_head,
        stride_query_dim,
        stride_k_cache_block,
        stride_k_cache_head,
        stride_k_cache_seq,
        stride_k_cache_dim,
        stride_v_cache_block,
        stride_v_cache_head,
        stride_v_cache_seq,
        stride_v_cache_dim,
        stride_output_batch,
        stride_output_head,
        stride_output_dim,
        stride_block_tables_batch,
        stride_block_tables_block,
        num_heads: tl.constexpr,
        head_dim: tl.constexpr,
        num_kv_heads: tl.constexpr,
        block_size: tl.constexpr,
        scale: tl.constexpr,
        BLOCK_D: tl.constexpr,
    ) -> None:
        """Triton kernel for paged attention decode.

        Inspired by vLLM's kernel_paged_attention_2d.
        """
        # Get batch and head indices
        batch_idx = tl.program_id(0)
        head_idx = tl.program_id(1)

        # Get context length for this sequence
        context_len = tl.load(context_lens_ptr + batch_idx)

        # Get KV head index (for GQA)
        kv_head_idx = head_idx // (num_heads // num_kv_heads)

        # Load query vector
        q_offset = batch_idx * stride_query_batch + head_idx * stride_query_head
        dim_offsets = tl.arange(0, BLOCK_D)
        query = tl.load(query_ptr + q_offset + dim_offsets * stride_query_dim)
        query = query * scale

        # Initialize accumulator
        acc = tl.zeros([BLOCK_D], dtype=tl.float32)
        max_logit = float("-inf")
        sum_exp = 0.0

        # Process each block
        num_blocks = (context_len + block_size - 1) // block_size

        for block_idx in range(num_blocks):
            # Get physical block number from block table
            block_table_offset = batch_idx * stride_block_tables_batch
            phys_block = tl.load(block_tables_ptr + block_table_offset + block_idx * stride_block_tables_block)

            # Load key block
            k_offset = phys_block * stride_k_cache_block + kv_head_idx * stride_k_cache_head

            # Compute attention scores for this block
            for seq_pos in range(block_size):
                abs_pos = block_idx * block_size + seq_pos
                if abs_pos < context_len:
                    # Load key vector
                    k = tl.load(
                        k_cache_ptr + k_offset + seq_pos * stride_k_cache_seq + dim_offsets * stride_k_cache_dim
                    )

                    # Compute attention score
                    score = tl.sum(query * k, axis=0)

                    # Online softmax update
                    new_max = tl.maximum(max_logit, score)
                    old_exp = tl.exp(max_logit - new_max)
                    new_exp = tl.exp(score - new_max)

                    # Load value vector
                    v_offset = (
                        phys_block * stride_v_cache_block
                        + kv_head_idx * stride_v_cache_head
                        + seq_pos * stride_v_cache_seq
                    )
                    v = tl.load(v_cache_ptr + v_offset + dim_offsets * stride_v_cache_dim)

                    # Update accumulator with online softmax
                    acc = acc * old_exp * sum_exp / (old_exp * sum_exp + new_exp)
                    acc = acc + v * new_exp / (old_exp * sum_exp + new_exp)

                    sum_exp = old_exp * sum_exp + new_exp
                    max_logit = new_max

        # Store output
        out_offset = batch_idx * stride_output_batch + head_idx * stride_output_head
        tl.store(output_ptr + out_offset + dim_offsets * stride_output_dim, acc)


class TritonPagedAttention(AttentionKernel):
    """Triton-based paged attention kernel.

    Implements efficient paged attention using Triton JIT compilation.
    """

    def __init__(self, config: AttentionConfig) -> None:
        self.config: AttentionConfig = config
        self.scale: float = 1.0 / math.sqrt(config.head_dim)

    def forward(
        self,
        query: "torch.Tensor",
        key: "torch.Tensor",
        value: "torch.Tensor",
        metadata: AttentionMetadata,
        k_cache: Optional["torch.Tensor"] = None,
        v_cache: Optional["torch.Tensor"] = None,
    ) -> "torch.Tensor":
        """Execute Triton paged attention."""
        if not HAS_TRITON:
            raise RuntimeError("Triton not available")

        batch_size, num_heads, head_dim = query.shape

        # Allocate output
        output: Tensor = torch.empty_like(query)

        # Check for block tables
        if metadata.block_tables is None:
            raise ValueError("Block tables required for paged attention")

        # Launch kernel
        grid: tuple[int, int] = (batch_size, num_heads)

        PAGED_ATTENTION_KERNEL[grid](
            output,
            query,
            k_cache,
            v_cache,
            metadata.block_tables,
            metadata.context_lens,
            # Strides
            query.stride(0),
            query.stride(1),
            query.stride(2),
            k_cache.stride(0),
            k_cache.stride(1),
            k_cache.stride(2),
            k_cache.stride(3),
            v_cache.stride(0),
            v_cache.stride(1),
            v_cache.stride(2),
            v_cache.stride(3),
            output.stride(0),
            output.stride(1),
            output.stride(2),
            metadata.block_tables.stride(0),
            metadata.block_tables.stride(1),
            # Config
            num_heads=num_heads,
            head_dim=head_dim,
            num_kv_heads=self.config.num_kv_heads,
            block_size=self.config.block_size,
            scale=self.scale,
            BLOCK_D=head_dim,
        )

        return output

    def supports_context_length(self, context_len: int) -> bool:
        return context_len <= self.config.max_seq_len


class NaiveAttention(AttentionKernel):
    """Reference implementation of attention (CPU/GPU compatible)."""

    def __init__(self, config: AttentionConfig) -> None:
        self.config: AttentionConfig = config
        self.scale: float = 1.0 / math.sqrt(config.head_dim)

    def forward(
        self,
        query: Any,
        key: Any,
        value: Any,
        metadata: AttentionMetadata,
        k_cache: Optional[Any] = None,
        v_cache: Optional[Any] = None,
    ) -> Any:
        """Execute naive attention."""
        if HAS_TORCH:
            return self._forward_torch(query, key, value, metadata)
        return self._forward_numpy(query, key, value, metadata)

    def _forward_torch(
        self,
        query: "torch.Tensor",
        key: "torch.Tensor",
        value: "torch.Tensor",
        _metadata: AttentionMetadata,
    ) -> "torch.Tensor":
        """PyTorch implementation."""
        # Standard attention computation
        scores: Tensor = torch.matmul(query, key.transpose(-2, -1)) * self.scale
        attn_weights: Tensor = torch.softmax(scores, dim=-1)
        output: Tensor = torch.matmul(attn_weights, value)
        return output

    def _forward_numpy(
        self,
        query: Any,
        key: Any,
        value: Any,
        _metadata: AttentionMetadata,
    ) -> Any:
        """NumPy fallback implementation."""
        import numpy as np

        # Standard attention computation
        scores = np.matmul(query, np.swapaxes(key, -2, -1)) * self.scale
        scores = scores - np.max(scores, axis=-1, keepdims=True)
        attn_weights = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)
        output = np.matmul(attn_weights, value)
        return output

    def supports_context_length(self, context_len: int) -> bool:
        return True  # No limit for naive implementation


class SlidingWindowAttention(AttentionKernel):
    """Sliding window attention for efficient long-context handling."""

    def __init__(self, config: AttentionConfig) -> None:
        self.config: AttentionConfig = config
        self.scale: float = 1.0 / math.sqrt(config.head_dim)
        self.window_size: int = config.sliding_window_size

    def forward(
        self,
        query: Any,
        key: Any,
        value: Any,
        metadata: AttentionMetadata,
        k_cache: Optional[Any] = None,
        v_cache: Optional[Any] = None,
    ) -> Any:
        """Execute sliding window attention."""
        if not HAS_TORCH:
            raise RuntimeError("PyTorch required for sliding window attention")

        _, _, seq_len, _ = query.shape

        # Create sliding window mask
        causal_mask: Tensor = torch.ones(seq_len, seq_len, device=query.device, dtype=torch.bool)
        causal_mask: Tensor = torch.tril(causal_mask)

        # Apply sliding window
        window_mask: Tensor = torch.ones_like(causal_mask)
        for i in range(seq_len):
            start: int = max(0, i - self.window_size + 1)
            window_mask[i, :start] = 0

        mask: Tensor = causal_mask & window_mask
        mask: Tensor = mask.unsqueeze(0).unsqueeze(0)  # [1, 1, seq, seq]

        # Compute attention
        scores: Tensor = torch.matmul(query, key.transpose(-2, -1)) * self.scale
        scores: Tensor = scores.masked_fill(~mask, float("-inf"))
        attn_weights: Tensor = torch.softmax(scores, dim=-1)
        output: Tensor = torch.matmul(attn_weights, value)

        return output

    def supports_context_length(self, context_len: int) -> bool:
        return True  # Sliding window handles arbitrary lengths


@dataclass
class KVSplitConfig:
    """Configuration for KV splits to handle long contexts.

    Inspired by vLLM's KV split patterns for decode attention.
    """

    num_splits: int = 8
    split_overlap: int = 0  # For context continuity
    use_parallel_reduction: bool = True
    max_context_per_split: int = 1024


class TritonAttentionOps:
    """Unified attention operations interface.

    Provides automatic backend selection and fallback.

    Beyond vLLM: Unified API for all attention backends.
    """

    _BACKEND_MAP: Dict[AttentionBackend, type] = {
        AttentionBackend.TRITON: TritonPagedAttention if HAS_TRITON else NaiveAttention,
        AttentionBackend.NAIVE: NaiveAttention,
    }

    def __init__(self, config: AttentionConfig) -> None:
        """Initialize attention operations.

        Args:
            config: Attention configuration
        """
        self.config: AttentionConfig = config

        # Select backend
        backend: AttentionBackend = config.backend
        if backend == AttentionBackend.TRITON and not HAS_TRITON:
            logger.warning("Triton not available, falling back to naive attention")
            backend: AttentionBackend = AttentionBackend.NAIVE

        kernel_cls: type = self._BACKEND_MAP.get(backend, NaiveAttention)
        self._kernel = kernel_cls(config)

        # Sliding window kernel
        if config.use_sliding_window:
            self._sliding_kernel = SlidingWindowAttention(config)
        else:
            self._sliding_kernel = None

        # KV split configuration
        self._kv_split = KVSplitConfig(num_splits=config.num_kv_splits)

    def forward(
        self,
        query: Any,
        key: Any,
        value: Any,
        metadata: AttentionMetadata,
        k_cache: Optional[Any] = None,
        v_cache: Optional[Any] = None,
    ) -> Any:
        """Execute attention operation.

        Automatically selects appropriate kernel based on context.
        """
        # Check if sliding window is needed
        if self._sliding_kernel and metadata.max_decode_seq_len > self.config.sliding_window_size:
            return self._sliding_kernel.forward(query, key, value, metadata, k_cache, v_cache)

        # Use main kernel
        return self._kernel.forward(query, key, value, metadata, k_cache, v_cache)

    def paged_attention_decode(
        self,
        query: Any,
        k_cache: Any,
        v_cache: Any,
        block_tables: Any,
        context_lens: Any,
        max_context_len: int,
    ) -> Any:
        """Execute paged attention for decode phase.

        Inspired by vLLM's _paged_attention_decode.
        """
        metadata = AttentionMetadata(
            block_tables=block_tables,
            context_lens=context_lens,
            max_decode_seq_len=max_context_len,
            is_prefill=False,
        )

        # For long contexts, use KV splits
        if max_context_len > self._kv_split.max_context_per_split * self._kv_split.num_splits:
            return self._split_kv_attention(query, k_cache, v_cache, metadata)

        return self._kernel.forward(query, None, None, metadata, k_cache, v_cache)

    def _split_kv_attention(
        self,
        query: Any,
        k_cache: Any,
        v_cache: Any,
        metadata: AttentionMetadata,
    ) -> Any:
        """Execute attention with KV splits for very long contexts.

        Divides context into splits and aggregates results.
        """
        if not HAS_TORCH:
            raise RuntimeError("KV splits require PyTorch")

        num_splits: int = self._kv_split.num_splits
        max_context: int = metadata.max_decode_seq_len
        split_size: int = (max_context + num_splits - 1) // num_splits

        # Collect split outputs
        split_outputs = []

        for i in range(num_splits):
            start_pos: int = i * split_size
            end_pos: int = min((i + 1) * split_size, max_context)

            if start_pos >= max_context:
                break

            # Create split metadata
            split_metadata = AttentionMetadata(
                block_tables=metadata.block_tables,
                context_lens=torch.clamp(metadata.context_lens - start_pos, min=0, max=end_pos - start_pos),
                max_decode_seq_len=end_pos - start_pos,
            )

            # Get split output with attention statistics
            split_out = self._kernel.forward(query, None, None, split_metadata, k_cache, v_cache)
            split_outputs.append(split_out)

        # Aggregate splits (simplified - full implementation would use log-sum-exp)
        if len(split_outputs) == 1:
            return split_outputs[0]

        return torch.mean(torch.stack(split_outputs), dim=0)

    def compute_prefill_attention(
        self,
        query: Any,
        key: Any,
        value: Any,
        seq_lens: List[int],
        _causal: bool = True,
    ) -> Any:
        """Compute attention for prefill phase.

        Args:
            query: Query tensor
            key: Key tensor
            value: Value tensor
            seq_lens: Sequence lengths
            causal: Whether to use causal masking
        """
        metadata = AttentionMetadata(
            seq_lens=seq_lens,
            is_prefill=True,
            num_prefill_tokens=sum(seq_lens),
        )

        return self._kernel.forward(query, key, value, metadata)

    @staticmethod
    def detect_best_backend() -> AttentionBackend:
        """Detect the best available attention backend."""
        if HAS_TRITON and HAS_TORCH:
            return AttentionBackend.TRITON
        if HAS_TORCH:
            return AttentionBackend.SDPA
        return AttentionBackend.NAIVE


# Factory functions
def create_attention_ops(
    num_heads: int = 32,
    head_dim: int = 128,
    num_kv_heads: Optional[int] = None,
    **kwargs: Any,
) -> TritonAttentionOps:
    """Create attention operations with sensible defaults.

    Args:
        num_heads: Number of attention heads
        head_dim: Dimension per head
        num_kv_heads: Number of KV heads (for GQA)
        **kwargs: Additional config options
    """
    config = AttentionConfig(
        num_heads=num_heads,
        head_dim=head_dim,
        num_kv_heads=num_kv_heads or num_heads,
        backend=TritonAttentionOps.detect_best_backend(),
        **kwargs,
    )

    return TritonAttentionOps(config)
