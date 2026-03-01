# OutputProcessor

**File**: `src\infrastructure\engine\OutputProcessor.py`  
**Type**: Python Module  
**Summary**: 15 classes, 0 functions, 18 imports  
**Lines**: 539  
**Complexity**: 24 (complex)

## Overview

OutputProcessor - Request output management and state tracking.

Inspired by vLLM's v1/engine/output_processor.py - manages per-request state,
detokenization, and output batching.

## Classes (15)

### `EventType`

**Inherits from**: Enum

Types of request events.

### `RequestEvent`

An event in request lifecycle.

### `LoRARequest`

LoRA adapter request information.

### `ParentRequest`

Parent request for multi-turn conversations.

### `SamplingParams`

Parameters for token sampling.

### `EngineCoreRequest`

Request to be processed by engine core.

### `EngineCoreOutput`

Output from engine core for a single request.

### `EngineCoreOutputs`

Batch of outputs from engine core.

### `RequestOutput`

Final output for a request (to be returned to client).

### `OutputProcessorOutput`

Output from OutputProcessor.process_outputs().

### `RequestOutputCollector`

Queue for collecting request outputs.

**Methods** (3):
- `__init__(self)`
- `put(self, output)`
- `empty(self)`

### `RequestState`

Per-request state tracking.

Manages detokenization state, output accumulation, and streaming.

**Methods** (7):
- `__init__(self, request_id, prompt, prompt_token_ids, sampling_params, arrival_time, queue, log_stats, stream_interval)`
- `from_new_request(cls, tokenizer, request, prompt, parent_req, request_index, queue, log_stats, stream_interval)`
- `add_event(self, event_type, details)`
- `update(self, new_token_ids, new_text, finish_reason)`
- `should_emit_output(self)`
- `get_output(self, delta)`
- `_get_metrics(self)`

### `LoRARequestStates`

Track LoRA request states.

**Methods** (4):
- `__init__(self, log_stats)`
- `add_request(self, request_id, lora_request)`
- `remove_request(self, request_id, lora_request)`
- `get_active_lora_ids(self)`

### `OutputProcessor`

Process EngineCoreOutputs into RequestOutputs.

Manages per-request state, detokenization, and output streaming.

**Methods** (8):
- `__init__(self, tokenizer, log_stats, stream_interval)`
- `get_num_unfinished_requests(self)`
- `has_unfinished_requests(self)`
- `propagate_error(self, e)`
- `add_request(self, request, prompt, parent_req, request_index, queue)`
- `abort_requests(self, request_ids, internal)`
- `process_outputs(self, engine_core_outputs, engine_core_timestamp, iteration_stats)`
- `get_request_state(self, request_id)`

### `IterationStats`

Statistics for a single iteration.

**Methods** (2):
- `__init__(self)`
- `to_dict(self)`

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `abc.ABC`
- `asyncio`
- `collections.defaultdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Iterator`
- `typing.List`
- ... and 3 more

---
*Auto-generated documentation*
