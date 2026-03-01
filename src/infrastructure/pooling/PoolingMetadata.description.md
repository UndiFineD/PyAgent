# PoolingMetadata

**File**: `src\infrastructure\pooling\PoolingMetadata.py`  
**Type**: Python Module  
**Summary**: 12 classes, 1 functions, 20 imports  
**Lines**: 511  
**Complexity**: 29 (complex)

## Overview

Phase 45: Pooling Infrastructure
vLLM-inspired pooling metadata and cursor management.

Beyond vLLM:
- Multi-strategy pooling (mean, max, first, last, attention-weighted)
- Async pooling with prefetch
- Memory-efficient chunked operations
- Cross-request pooling optimization

## Classes (12)

### `PoolingStrategy`

**Inherits from**: Enum

Pooling strategies for sequence embeddings.

### `PoolingCursor`

Cursor for tracking pooling positions (vLLM PoolingCursor equivalent).

Tracks the position within a sequence for pooling operations,
supporting both contiguous and chunked prefill scenarios.

**Methods** (6):
- `advance(self, num_tokens)`
- `reset(self)`
- `remaining(self)`
- `is_complete(self)`
- `global_start(self)`
- `global_end(self)`

### `PoolingStates`

State tracking for pooling operations (vLLM PoolingStates equivalent).

Tracks intermediate states for multi-pass pooling strategies.

**Methods** (3):
- `initialize(self, hidden_dim, strategy)`
- `update(self, hidden_states, attention_weights)`
- `finalize(self)`

### `PoolingMetadata`

Metadata for pooling operations (vLLM PoolingMetadata equivalent).

Contains all information needed to perform pooling across a batch.

**Methods** (4):
- `create(cls, seq_starts, seq_lens, hidden_dim, strategy, chunk_sizes)`
- `update_all(self, hidden_states_batch, attention_weights_batch)`
- `finalize_all(self)`
- `get_incomplete_indices(self)`

### `Pooler`

**Inherits from**: ABC

Abstract base for pooling implementations.

**Methods** (1):
- `pool(self, hidden_states, metadata)`

### `MeanPooler`

**Inherits from**: Pooler

Mean pooling implementation.

**Methods** (1):
- `pool(self, hidden_states, metadata)`

### `MaxPooler`

**Inherits from**: Pooler

Max pooling implementation.

**Methods** (1):
- `pool(self, hidden_states, metadata)`

### `LastTokenPooler`

**Inherits from**: Pooler

Last token pooling (for decoder-only models).

**Methods** (1):
- `pool(self, hidden_states, metadata)`

### `AttentionWeightedPooler`

**Inherits from**: Pooler

Attention-weighted pooling implementation.

**Methods** (2):
- `__init__(self, attention_head_idx)`
- `pool(self, hidden_states, metadata, attention_weights)`

### `PoolerFactory`

Factory for creating poolers.

**Methods** (1):
- `create(strategy)`

### `PoolerOutput`

Output from pooling operations (vLLM PoolerOutput equivalent).

Contains pooled embeddings and metadata.

**Methods** (3):
- `batch_size(self)`
- `to_numpy(self)`
- `get_embedding(self, idx)`

### `ChunkedPoolingManager`

Manager for chunked prefill pooling.

Beyond vLLM: Supports async prefetch and memory-efficient processing.

**Methods** (5):
- `__init__(self, hidden_dim, max_chunk_size, strategy)`
- `start_sequence(self, seq_id, seq_len)`
- `process_chunk(self, seq_id, hidden_states)`
- `finalize(self, seq_id)`
- `get_pending_count(self)`

## Functions (1)

### `pool_with_rust(hidden_states, seq_starts, seq_lens, strategy)`

Optimized pooling with Rust.

Returns pooled embeddings if Rust is available.

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `numpy`
- `rust_core`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Generic`
- ... and 5 more

---
*Auto-generated documentation*
