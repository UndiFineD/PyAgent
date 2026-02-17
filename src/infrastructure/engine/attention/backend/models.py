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


from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class AttentionBackendEnum(Enum):
    """Enumeration of available attention backends."""
    FLASH_ATTN = "flash_attn"
    FLASH_ATTN_2 = "flash_attn_2"
    FLASHINFER = "flashinfer"
    TRITON = "triton"  # Triton-based attention
    XFORMERS = "xformers"  # xFormers memory efficient
    TORCH_SDPA = "torch_sdpa"  # PyTorch SDPA
    NAIVE = "naive"  # Simple reference implementation
    PAGED = "paged"  # PagedAttention (vLLM native)
    PACKKV = "packkv"  # PackKV compressed (arXiv:2512.24449)

class AttentionType(Enum):
    """Types of attention computation."""
    PREFILL = auto()  # Full attention during prefill
    DECODE = auto()  # Incremental attention during decode
    ENCODER = auto()  # Encoder-side attention
    CROSS = auto()  # Cross-attention (decoder to encoder)


@dataclass
class AttentionCapabilities:
    """Capabilities of an attention backend."""
    # Supported attention types
    supports_prefill: bool = True
    supports_decode: bool = True
    supports_encoder: bool = True
    supports_cross: bool = False

    # Feature support
    supports_sliding_window: bool = False
    supports_alibi: bool = False
    supports_gqa: bool = True  # Grouped query attention
    supports_mqa: bool = True  # Multi-query attention
    supports_prefix_caching: bool = False
    supports_cuda_graphs: bool = True
    supports_fp8: bool = False

    # Hardware requirements
    requires_cuda: bool = True
    requires_bf16: bool = False
    min_sm_version: int = 70  # Volta+

    # Performance hints
    best_for_short_seqs: bool = False
    best_for_long_seqs: bool = False
    memory_efficient: bool = True


@dataclass
class AttentionMetadata:
    """Metadata for attention computation."""
    # Sequence lengths
    seq_lens: list[int] = field(default_factory=list)
    max_seq_len: int = 0
    context_lens: list[int] | None = None

    # Paged attention
    block_tables: Any | None = None  # [batch, max_blocks]
    slot_mapping: Any | None = None  # [total_tokens]

    # KV cache info
    kv_cache_dtype: str = "auto"
    num_kv_heads: int = 0
    head_size: int = 0

    # Attention type
    attn_type: AttentionType = AttentionType.DECODE

    # Sliding window
    sliding_window: int | None = None

    # Misc
    use_cuda_graph: bool = False
    prefix_cache_hit: bool = False

    # Compression (PackKV)
    compression_metadata: dict[int, dict[str, Any]] | None = None
