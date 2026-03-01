# orchestrator

**File**: `src\infrastructure\execution\batch\orchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 551  
**Complexity**: 20 (complex)

## Overview

Main orchestrator for GPU-resident batch management.

## Classes (1)

### `InputBatchOrchestrator`

Main orchestrator for GPU-resident batch management.

Handles:
- Request state caching
- Input buffer management
- Batch preparation from scheduler outputs
- Sampling metadata construction

Beyond vLLM: Adaptive buffer resizing based on workload.

**Methods** (20):
- `__init__(self, max_num_reqs, max_model_len, max_num_batched_tokens, device, pin_memory, vocab_size, dtype, is_pooling_model, is_spec_decode)`
- `_init_token_storage(self)`
- `_init_sampling_storage(self)`
- `num_reqs(self)`
- `req_ids(self)`
- `add_request(self, req_id, prompt_token_ids, sampling_params, mm_features, lora_request)`
- `_store_sampling_params(self, index, params)`
- `_set_default_sampling_params(self, index)`
- `remove_request(self, req_id)`
- `swap_states(self, i1, i2)`
- ... and 10 more methods

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `buffers.InputBuffers`
- `logging`
- `models.BatchUpdateBuilder`
- `models.CachedRequestState`
- `models.InputBatch`
- `models.SamplingMetadata`
- `numpy`
- `torch`
- `typing.Any`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
