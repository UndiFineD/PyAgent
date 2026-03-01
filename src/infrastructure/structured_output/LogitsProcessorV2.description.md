# LogitsProcessorV2

**File**: `src\infrastructure\structured_output\LogitsProcessorV2.py`  
**Type**: Python Module  
**Summary**: 9 classes, 0 functions, 23 imports  
**Lines**: 593  
**Complexity**: 47 (complex)

## Overview

LogitsProcessorV2 - Enhanced logits processor interface.

Implements vLLM's v1 LogitsProcessor interface with:
- BatchUpdate for state management
- MoveDirectionality for request movement tracking
- Argmax invariance declaration
- Efficient batch processing

Beyond vLLM innovations:
- Composable processor chains
- Lazy state updates
- Metrics collection
- Processor hot-swapping

## Classes (9)

### `MoveDirectionality`

**Inherits from**: Enum

Direction of request movement within batch.

### `SamplingParams`

Sampling parameters for a request.

**Methods** (1):
- `__post_init__(self)`

### `BatchUpdate`

Batch state change information for logits processors.

Contains metadata for requests added to, removed from, and moved
within the persistent batch. Operations should be processed in order:
removed, added, moved.

**Methods** (2):
- `empty(cls, batch_size)`
- `has_changes(self)`

### `BatchUpdateBuilder`

Builder for constructing BatchUpdate objects.

**Methods** (7):
- `__init__(self, batch_size)`
- `add_request(self, index, params, prompt_token_ids, output_token_ids)`
- `remove_request(self, index)`
- `move_request(self, from_index, to_index, directionality)`
- `set_batch_size(self, size)`
- `build(self)`
- `clear(self)`

### `LogitsProcessor`

**Inherits from**: ABC

Abstract base class for logits processors.

Processors modify logits before sampling to implement constraints
like temperature, top-k, min-p, bad words, etc.

**Methods** (6):
- `validate_params(cls, sampling_params)`
- `apply(self, logits)`
- `is_argmax_invariant(self)`
- `update_state(self, batch_update)`
- `has_state(self)`
- `reset(self)`

### `MinPLogitsProcessor`

**Inherits from**: LogitsProcessor

Min-P sampling logits processor.

Filters tokens with probability below (min_p * max_probability).
Does not affect greedy sampling (argmax invariant).

**Methods** (9):
- `__init__(self, max_num_reqs, device, is_pin_memory)`
- `is_argmax_invariant(self)`
- `get_min_p_by_index(self, index)`
- `update_state(self, batch_update)`
- `apply(self, logits)`
- `_apply_numpy(self, logits)`
- `_apply_generic(self, logits)`
- `has_state(self)`
- `reset(self)`

### `LogitBiasLogitsProcessor`

**Inherits from**: LogitsProcessor

Logit bias processor.

Adds bias values to specific token logits. Can change argmax
results, so not argmax invariant.

**Methods** (8):
- `__init__(self, max_num_reqs, device, is_pin_memory)`
- `is_argmax_invariant(self)`
- `update_state(self, batch_update)`
- `apply(self, logits)`
- `_apply_numpy(self, logits)`
- `_apply_generic(self, logits)`
- `has_state(self)`
- `reset(self)`

### `CompositeLogitsProcessor`

**Inherits from**: LogitsProcessor

Composite processor that chains multiple processors.

Beyond vLLM: Allows flexible composition of processors
with optimized execution order.

**Methods** (8):
- `__init__(self, processors)`
- `is_argmax_invariant(self)`
- `update_state(self, batch_update)`
- `apply(self, logits)`
- `has_state(self)`
- `reset(self)`
- `add_processor(self, processor)`
- `remove_processor(self, processor)`

### `LogitsProcessorRegistry`

Registry for logits processor types.

Beyond vLLM: Provides plugin-based processor registration
and automatic processor selection based on sampling params.

**Methods** (6):
- `__new__(cls)`
- `_register_defaults(self)`
- `register(self, name, processor_cls)`
- `get(self, name)`
- `create_for_params(self, params, max_num_reqs, device)`
- `get_instance(cls)`

## Dependencies

**Imports** (23):
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
- `typing.List`
- ... and 8 more

---
*Auto-generated documentation*
