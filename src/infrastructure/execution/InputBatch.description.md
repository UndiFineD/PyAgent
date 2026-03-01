# InputBatch

**File**: `src\infrastructure\execution\InputBatch.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 9 imports  
**Lines**: 461  
**Complexity**: 22 (complex)

## Overview

InputBatch.py - Structured batch management for model execution.

Inspired by vLLM's v1/worker/gpu/input_batch.py. Provides pre-allocated
buffers and structured batch state for efficient model execution.

Phase 29: Execution Context, Batching & Async Streaming

## Classes (4)

### `SamplingMetadata`

Per-request sampling parameters for batched sampling.

Based on vLLM's SamplingMetadata pattern.

**Methods** (4):
- `from_defaults(cls, num_reqs)`
- `from_params(cls, temperatures, top_ks, top_ps, min_ps, repetition_penalties, presence_penalties, frequency_penalties)`
- `num_reqs(self)`
- `slice(self, start, end)`

### `InputBuffers`

Pre-allocated tensors for batch inputs.

Avoids runtime allocation during model execution.
Based on vLLM's InputBuffers pattern.

**Methods** (2):
- `allocate(cls, max_num_reqs, max_num_tokens, embed_dim, max_blocks_per_req, dtype)`
- `reset(self)`

### `InputBatch`

Structured batch for model execution.

Contains all inputs and metadata needed for a forward pass.
Based on vLLM's InputBatch pattern.

**Methods** (8):
- `num_reqs(self)`
- `num_tokens(self)`
- `make_dummy(cls, num_reqs, num_tokens, buffers)`
- `from_requests(cls, req_ids, input_ids_list, positions_list, buffers, sampling_metadata)`
- `get_req_index(self, req_id)`
- `get_logits_indices(self)`
- `get_token_range(self, req_idx)`
- `slice_request(self, req_idx)`

### `BatchBuilder`

Builder for constructing InputBatch instances.

Accumulates requests and builds batches efficiently.

**Methods** (8):
- `__init__(self, buffers)`
- `reset(self)`
- `add_request(self, req_id, input_ids, positions, temperature, top_k, top_p)`
- `build(self)`
- `num_reqs(self)`
- `total_tokens(self)`
- `is_empty(self)`
- `is_full(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Sequence`

---
*Auto-generated documentation*
