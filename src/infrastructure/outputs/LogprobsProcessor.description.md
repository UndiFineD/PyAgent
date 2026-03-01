# LogprobsProcessor

**File**: `src\infrastructure\outputs\LogprobsProcessor.py`  
**Type**: Python Module  
**Summary**: 8 classes, 2 functions, 24 imports  
**Lines**: 512  
**Complexity**: 28 (complex)

## Overview

Phase 45: Logprobs Tensors and Lists
vLLM-inspired logprobs data structures with optimized handling.

Beyond vLLM:
- Async CPU transfer with double buffering
- Compressed storage for sparse logprobs
- Streaming logprobs support
- Batch aggregation optimizations

## Classes (8)

### `TokenLogprob`

Single token with its log probability.

**Methods** (1):
- `__lt__(self, other)`

### `TopLogprobs`

Top logprobs for a single position.

**Methods** (1):
- `from_array(cls, position, logprobs, token_ids, tokens, selected_idx, k)`

### `LogprobsLists`

List-based logprobs storage (vLLM LogprobsLists equivalent).

Efficient for variable-length sequences with streaming output.

**Methods** (6):
- `__init__(self, num_sequences)`
- `append(self, seq_idx, logprobs)`
- `get_sequence(self, seq_idx)`
- `get_all(self)`
- `__len__(self)`
- `total_tokens(self)`

### `LogprobsTensors`

Tensor-based logprobs storage (vLLM LogprobsTensors equivalent).

Efficient for batched processing with GPU tensors.

Beyond vLLM:
- Double buffering for async CPU transfer
- Sparse storage for memory efficiency
- Lazy evaluation support

**Methods** (3):
- `create_empty(cls, batch_size, max_seq_len, vocab_size, top_k, sparse)`
- `set_position(self, batch_idx, position, logprobs, token_id)`
- `to_lists(self, tokenizer)`

### `AsyncCPUTransfer`

Async CPU transfer manager for GPU tensors.

Beyond vLLM: Double buffering and pipelining for overlap.

**Methods** (4):
- `__init__(self, num_buffers, max_workers)`
- `submit_transfer(self, tensor, transfer_id)`
- `get_result(self, transfer_id, timeout)`
- `shutdown(self)`

### `SamplerOutput`

Output from the sampler (vLLM SamplerOutput equivalent).

Contains sampled tokens and optional logprobs.

**Methods** (2):
- `batch_size(self)`
- `get_token_ids(self, batch_idx)`

### `ModelRunnerOutput`

Output from model runner (vLLM ModelRunnerOutput equivalent).

Contains all outputs from a single forward pass.

**Methods** (2):
- `create(cls, sampled_token_ids, req_ids, logprobs)`
- `get_output_for_request(self, req_id)`

### `StreamingLogprobsCollector`

Collector for streaming logprobs.

Beyond vLLM: Supports real-time streaming with backpressure.

**Methods** (7):
- `__init__(self, buffer_size)`
- `register_callback(self, req_id, callback)`
- `unregister(self, req_id)`
- `add(self, req_id, logprobs)`
- `_flush_locked(self, req_id)`
- `flush(self, req_id)`
- `flush_all(self)`

## Functions (2)

### `extract_top_k_logprobs_rust(logprobs, k)`

Extract top-k logprobs using Rust.

Returns (top_logprobs, top_indices) if Rust is available.

### `batch_logprobs_to_cpu_rust(logprobs, token_ids)`

Batch transfer logprobs to CPU using Rust.

Returns transferred (logprobs, token_ids) if Rust is available.

## Dependencies

**Imports** (24):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `collections.defaultdict`
- `concurrent.futures.Future`
- `concurrent.futures.ThreadPoolExecutor`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `numpy`
- `rust_core`
- `threading`
- `time`
- `typing.Any`
- ... and 9 more

---
*Auto-generated documentation*
