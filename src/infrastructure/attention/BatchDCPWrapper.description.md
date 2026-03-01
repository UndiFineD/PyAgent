# BatchDCPWrapper

**File**: `src\infrastructure\attention\BatchDCPWrapper.py`  
**Type**: Python Module  
**Summary**: 10 classes, 3 functions, 24 imports  
**Lines**: 632  
**Complexity**: 20 (complex)

## Overview

Batch DCP Wrapper - Batch processing for disaggregated prefill-decode.

Implements batch-level wrappers for coordinating DCP (Disaggregated
Compute and Prefill) operations across multiple requests.

Key patterns from vLLM:
- BatchDCPPrefillWrapper for batch prefill coordination
- LSE (log-sum-exp) all-gather for distributed attention
- plan/run methods for two-phase execution

Beyond vLLM:
- Unified batch interface for mixed prefill/decode
- Automatic batch size optimization
- Memory-aware batching with spill prevention

## Classes (10)

### `BatchPhase`

**Inherits from**: Enum

Phase of batch processing.

### `AllReduceStrategy`

**Inherits from**: Enum

Strategy for distributed reduction.

### `BatchRequest`

A request in a batch.

Tracks per-request state within a batch.

### `BatchMetadata`

Metadata for a batch of requests.

Inspired by vLLM's batch metadata structures.

**Methods** (2):
- `is_prefill(self)`
- `is_decode(self)`

### `DCPPlanConfig`

Configuration for DCP planning.

Controls how batches are planned and executed.

### `ExecutionPlan`

Plan for executing a batch.

Produced by plan() method, consumed by run() method.

### `BatchExecutor`

**Inherits from**: ABC

Abstract base for batch execution.

**Methods** (2):
- `plan(self, requests, metadata)`
- `run(self, plan, input_tensors)`

### `BatchDCPPrefillWrapper`

**Inherits from**: BatchExecutor

Wrapper for batch DCP prefill operations.

Coordinates prefill across a batch of requests,
preparing KV cache for transfer to decode instances.

Inspired by vLLM's BatchDCPPrefillWrapper pattern.

**Methods** (4):
- `__init__(self, config, attention_fn)`
- `plan(self, requests, metadata)`
- `run(self, plan, input_tensors)`
- `get_stats(self)`

### `BatchDCPDecodeWrapper`

**Inherits from**: BatchExecutor

Wrapper for batch DCP decode operations.

Coordinates decode across a batch of requests that
receive KV cache from prefill instances.

**Methods** (6):
- `__init__(self, config, attention_fn)`
- `plan(self, requests, metadata)`
- `_plan_lse_gather(self, requests)`
- `run(self, plan, input_tensors)`
- `_do_lse_gather(self, output, gather_plan)`
- `get_stats(self)`

### `UnifiedBatchWrapper`

Unified wrapper for mixed prefill/decode batches.

Beyond vLLM: Single interface for heterogeneous batches.

**Methods** (3):
- `__init__(self, config)`
- `process_batch(self, requests, input_tensors)`
- `get_stats(self)`

## Functions (3)

### `create_prefill_wrapper(max_batch_size, max_tokens)`

Create a prefill wrapper with sensible defaults.

### `create_decode_wrapper(max_batch_size, world_size)`

Create a decode wrapper with sensible defaults.

### `create_unified_wrapper()`

Create a unified wrapper for mixed batches.

## Dependencies

**Imports** (24):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `numpy`
- `time`
- `torch`
- `torch.distributed`
- `typing.Any`
- `typing.Callable`
- ... and 9 more

---
*Auto-generated documentation*
