# UBatchProcessor

**File**: `src\infrastructure\cuda\UBatchProcessor.py`  
**Type**: Python Module  
**Summary**: 8 classes, 1 functions, 17 imports  
**Lines**: 578  
**Complexity**: 25 (complex)

## Overview

UBatchProcessor - Micro-batch processing for CUDA graph efficiency.

Implements vLLM's UBatchWrapper patterns for efficient GPU utilization:
- UBatchContext: Execution context for micro-batches
- UbatchMetadata: Sliced inputs for each micro-batch  
- UBatchWrapper: Thread-coordinated micro-batch execution
- Barrier synchronization across threads

Beyond vLLM:
- Dynamic ubatch sizing based on memory pressure
- Adaptive thread pool sizing
- Overlap optimization for compute/transfer

## Classes (8)

### `UBatchState`

**Inherits from**: Enum

State of micro-batch processing.

### `UBatchSlice`

Describes a slice of the input batch for micro-batching.

Attributes:
    token_slice: Slice object for token range
    req_slice: Slice object for request range
    num_tokens: Number of tokens in slice
    num_reqs: Number of requests in slice

**Methods** (1):
- `from_range(cls, token_start, token_end, req_start, req_end)`

### `UBatchContext`

Execution context for a micro-batch.

Attributes:
    slice_info: Slice describing this micro-batch
    thread_id: Thread handling this context
    cpu_wait_event: Event for CPU synchronization
    gpu_wait_event: Event for GPU synchronization (simulated)

**Methods** (3):
- `signal_ready(self)`
- `wait_ready(self, timeout)`
- `reset(self)`

### `UbatchMetadata`

Metadata for a micro-batch execution.

Attributes:
    context: Execution context
    input_ids: Sliced input token IDs
    positions: Sliced position IDs
    inputs_embeds: Optional sliced embeddings
    intermediate_tensors: Optional intermediate state
    num_tokens: Number of tokens

### `UBatchConfig`

Configuration for micro-batch processing.

### `UBatchBarrier`

Barrier for synchronizing micro-batch threads.

Provides coordination between main thread and worker threads
during CUDA graph capture and execution.

**Methods** (4):
- `__init__(self, num_parties)`
- `wait(self, timeout)`
- `reset(self)`
- `generation(self)`

### `UBatchWrapper`

Wraps a model to enable micro-batch execution.

Based on vLLM's UBatchWrapper for efficient CUDA graph usage
with data parallel workloads. Splits large batches into
micro-batches for better graph hit rates.

Beyond vLLM:
- Dynamic sizing based on memory pressure
- Adaptive thread pool
- Overlap optimization

**Methods** (11):
- `__init__(self, runnable, config)`
- `__getattr__(self, key)`
- `unwrap(self)`
- `compute_slices(self, num_tokens, num_reqs)`
- `prepare_contexts(self, slices)`
- `slice_inputs(self, inputs, slice_info)`
- `_run_ubatch(self, context, sliced_inputs)`
- `__call__(self)`
- `_merge_outputs(self, outputs)`
- `barrier_sync(self, timeout)`
- ... and 1 more methods

### `DynamicUBatchWrapper`

**Inherits from**: UBatchWrapper

Extended wrapper with dynamic sizing based on memory.

Beyond vLLM:
- Adjusts ubatch count based on memory pressure
- Learns optimal sizing from history

**Methods** (5):
- `__init__(self, runnable, config, memory_threshold)`
- `compute_slices(self, num_tokens, num_reqs)`
- `_get_memory_usage(self)`
- `record_timing(self, num_tokens, elapsed)`
- `optimal_ubatch_size(self)`

## Functions (1)

### `make_ubatch_contexts(num_ubatches, num_tokens, num_reqs)`

Factory function to create ubatch contexts.

Args:
    num_ubatches: Number of micro-batches
    num_tokens: Total tokens
    num_reqs: Total requests
    
Returns:
    List of execution contexts

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `concurrent.futures.ThreadPoolExecutor`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `numpy`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 2 more

---
*Auto-generated documentation*
