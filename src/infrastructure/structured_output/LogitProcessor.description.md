# LogitProcessor

**File**: `src\infrastructure\structured_output\LogitProcessor.py`  
**Type**: Python Module  
**Summary**: 11 classes, 2 functions, 17 imports  
**Lines**: 630  
**Complexity**: 45 (complex)

## Overview

LogitProcessor: Token-level constraint application during generation.

Provides:
- Bitmask-based logit masking
- Composite processors for multiple constraints
- Logit bias injection
- Temperature/top-p/top-k integration

## Classes (11)

### `LogitBias`

Logit bias specification for token manipulation.

Supports:
- Additive bias
- Multiplicative scaling
- Hard constraints (force/ban)

**Methods** (1):
- `apply(self, logit)`

### `ProcessorStats`

Statistics for logit processors.

**Methods** (1):
- `mask_ratio(self)`

### `LogitProcessor`

**Inherits from**: ABC

Abstract base class for logit processors.

Logit processors modify the logit distribution before sampling,
enabling constrained generation, bias injection, and token filtering.

**Methods** (7):
- `__init__(self, vocab_size)`
- `__call__(self, input_ids, logits)`
- `enable(self)`
- `disable(self)`
- `is_enabled(self)`
- `reset(self)`
- `get_stats(self)`

### `ConstrainedLogitProcessor`

**Inherits from**: LogitProcessor

Logit processor for constrained generation.

Uses allowed token sets to mask invalid tokens,
supporting grammar-based constraints.

**Methods** (2):
- `__init__(self, vocab_size, allowed_tokens_fn, mask_value)`
- `__call__(self, input_ids, logits)`

### `BitmaskLogitProcessor`

**Inherits from**: LogitProcessor

High-performance logit processor using pre-computed bitmasks.

Optimized for batch processing with vectorized operations.

**Methods** (4):
- `__init__(self, vocab_size, bitmask_fn, mask_value)`
- `_ensure_buffer(self, batch_size)`
- `__call__(self, input_ids, logits)`
- `apply_inplace(self, input_ids, logits)`

### `BiasLogitProcessor`

**Inherits from**: LogitProcessor

Logit processor for applying token biases.

Supports additive bias, scaling, and hard constraints.

**Methods** (8):
- `__init__(self, vocab_size, biases)`
- `add_bias(self, bias)`
- `remove_bias(self, token_id)`
- `clear_biases(self)`
- `set_bias_value(self, token_id, bias)`
- `ban_token(self, token_id)`
- `force_token(self, token_id)`
- `__call__(self, input_ids, logits)`

### `CompositeLogitProcessor`

**Inherits from**: LogitProcessor

Combines multiple logit processors.

Processors are applied in order, allowing complex constraint combinations.

**Methods** (9):
- `__init__(self, vocab_size, processors)`
- `add_processor(self, processor)`
- `remove_processor(self, processor)`
- `clear_processors(self)`
- `get_processor(self, index)`
- `__len__(self)`
- `__call__(self, input_ids, logits)`
- `reset(self)`
- `get_all_stats(self)`

### `TemperatureProcessor`

**Inherits from**: LogitProcessor

Apply temperature scaling to logits.

**Methods** (3):
- `__init__(self, vocab_size, temperature)`
- `set_temperature(self, temperature)`
- `__call__(self, input_ids, logits)`

### `TopKProcessor`

**Inherits from**: LogitProcessor

Apply top-k filtering to logits.

**Methods** (3):
- `__init__(self, vocab_size, k)`
- `set_k(self, k)`
- `__call__(self, input_ids, logits)`

### `TopPProcessor`

**Inherits from**: LogitProcessor

Apply top-p (nucleus) filtering to logits.

**Methods** (3):
- `__init__(self, vocab_size, p)`
- `set_p(self, p)`
- `__call__(self, input_ids, logits)`

### `RepetitionPenaltyProcessor`

**Inherits from**: LogitProcessor

Apply repetition penalty to discourage repeated tokens.

**Methods** (2):
- `__init__(self, vocab_size, penalty, window_size)`
- `__call__(self, input_ids, logits)`

## Functions (2)

### `create_standard_processor_chain(vocab_size, temperature, top_k, top_p, repetition_penalty)`

Create a standard processor chain.

### `apply_constraints_to_logits(logits, allowed_tokens, mask_value)`

Simple utility to apply token constraints to logits.

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`
- `typing.Union`
- ... and 2 more

---
*Auto-generated documentation*
