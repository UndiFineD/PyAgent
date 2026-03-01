# TritonAttentionOps

**File**: `src\infrastructure\attention\TritonAttentionOps.py`  
**Type**: Python Module  
**Summary**: 10 classes, 1 functions, 20 imports  
**Lines**: 652  
**Complexity**: 22 (complex)

## Overview

Triton Attention Operations - GPU-accelerated attention kernels.

Implements high-performance attention operations inspired by vLLM's
Triton attention kernels. Provides paged attention, flash attention,
and optimized decode attention for inference.

Key patterns from vLLM:
- kernel_paged_attention_2d for 2D block attention
- _paged_attention_decode with CUDA streams
- KV splits for handling long contexts

Beyond vLLM:
- Unified attention API with automatic backend selection
- Memory-efficient sliding window attention
- Dynamic precision switching (FP16/BF16/FP32)

## Classes (10)

### `AttentionBackend`

**Inherits from**: Enum

Available attention backends.

### `PrecisionMode`

**Inherits from**: Enum

Precision mode for attention computation.

### `AttentionConfig`

Configuration for attention operations.

Inspired by vLLM's attention configuration patterns.

**Methods** (1):
- `num_queries_per_kv(self)`

### `AttentionMetadata`

Metadata for attention computation.

Mirrors vLLM's AttentionMetadata structure.

**Methods** (1):
- `total_tokens(self)`

### `AttentionKernel`

**Inherits from**: ABC

Abstract base for attention kernels.

**Methods** (2):
- `forward(self, query, key, value, metadata, k_cache, v_cache)`
- `supports_context_length(self, context_len)`

### `TritonPagedAttention`

**Inherits from**: AttentionKernel

Triton-based paged attention kernel.

Implements efficient paged attention using Triton JIT compilation.

**Methods** (3):
- `__init__(self, config)`
- `forward(self, query, key, value, metadata, k_cache, v_cache)`
- `supports_context_length(self, context_len)`

### `NaiveAttention`

**Inherits from**: AttentionKernel

Reference implementation of attention (CPU/GPU compatible).

**Methods** (5):
- `__init__(self, config)`
- `forward(self, query, key, value, metadata, k_cache, v_cache)`
- `_forward_torch(self, query, key, value, metadata)`
- `_forward_numpy(self, query, key, value, metadata)`
- `supports_context_length(self, context_len)`

### `SlidingWindowAttention`

**Inherits from**: AttentionKernel

Sliding window attention for efficient long-context handling.

**Methods** (3):
- `__init__(self, config)`
- `forward(self, query, key, value, metadata, k_cache, v_cache)`
- `supports_context_length(self, context_len)`

### `KVSplitConfig`

Configuration for KV splits to handle long contexts.

Inspired by vLLM's KV split patterns for decode attention.

### `TritonAttentionOps`

Unified attention operations interface.

Provides automatic backend selection and fallback.

Beyond vLLM: Unified API for all attention backends.

**Methods** (6):
- `__init__(self, config)`
- `forward(self, query, key, value, metadata, k_cache, v_cache)`
- `paged_attention_decode(self, query, k_cache, v_cache, block_tables, context_lens, max_context_len)`
- `_split_kv_attention(self, query, k_cache, v_cache, metadata)`
- `compute_prefill_attention(self, query, key, value, seq_lens, causal)`
- `detect_best_backend()`

## Functions (1)

### `create_attention_ops(num_heads, head_dim, num_kv_heads)`

Create attention operations with sensible defaults.

Args:
    num_heads: Number of attention heads
    head_dim: Dimension per head
    num_kv_heads: Number of KV heads (for GQA)
    **kwargs: Additional config options

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `math`
- `numpy`
- `torch`
- `triton`
- `triton.language`
- `typing.Any`
- `typing.Dict`
- ... and 5 more

---
*Auto-generated documentation*
