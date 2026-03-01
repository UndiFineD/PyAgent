# LogitsProcessor

**File**: `src\core\base\processing\LogitsProcessor.py`  
**Type**: Python Module  
**Summary**: 11 classes, 2 functions, 15 imports  
**Lines**: 506  
**Complexity**: 28 (complex)

## Overview

LogitsProcessor - Composable token filtering pipeline.

Implements vLLM's logits processing pattern for modifying token logits
during text generation. Includes common processors for temperature,
top-k, top-p, repetition penalty, and bad words filtering.

Phase 23: Advanced Serialization & Validation

## Classes (11)

### `LogitsProcessor`

**Inherits from**: Protocol

Protocol for logits processors.

A logits processor modifies the logits tensor before sampling.
It receives the past token IDs and current logits, returning
modified logits.

**Methods** (1):
- `__call__(self, input_ids, logits)`

### `LogitsProcessorList`

Composable list of logits processors.

Applies processors in order, passing the output of each to the next.

Example:
    >>> processors = LogitsProcessorList([
    ...     TemperatureProcessor(0.7),
    ...     TopKProcessor(50),
    ...     TopPProcessor(0.9),
    ... ])
    >>> modified_logits = processors(input_ids, logits)

**Methods** (6):
- `__init__(self, processors)`
- `append(self, processor)`
- `extend(self, processors)`
- `__call__(self, input_ids, logits)`
- `__len__(self)`
- `__iter__(self)`

### `TemperatureProcessor`

Apply temperature scaling to logits.

Temperature < 1.0 makes distribution sharper (more deterministic)
Temperature > 1.0 makes distribution flatter (more random)
Temperature = 1.0 is unchanged

**Methods** (2):
- `__init__(self, temperature)`
- `__call__(self, input_ids, logits)`

### `TopKProcessor`

Keep only top-k logits, set others to -inf.

This limits sampling to the k most likely tokens.

**Methods** (2):
- `__init__(self, top_k)`
- `__call__(self, input_ids, logits)`

### `TopPProcessor`

Nucleus sampling - keep tokens with cumulative probability <= top_p.

This dynamically adjusts the number of considered tokens based on
their cumulative probability.

**Methods** (2):
- `__init__(self, top_p)`
- `__call__(self, input_ids, logits)`

### `RepetitionPenaltyProcessor`

Penalize tokens that have already appeared.

penalty > 1.0 discourages repetition
penalty < 1.0 encourages repetition
penalty = 1.0 is unchanged

**Methods** (2):
- `__init__(self, penalty)`
- `__call__(self, input_ids, logits)`

### `NoBadWordsProcessor`

Block specific token sequences from being generated.

Given a list of "bad word" token sequences, this processor sets
their logits to -inf when they would complete a bad sequence.

**Methods** (3):
- `__init__(self, bad_words_ids)`
- `__call__(self, input_ids, logits)`
- `_init_word_bias(self, logits)`

### `MinLengthProcessor`

Prevent EOS token before minimum length is reached.

**Methods** (2):
- `__init__(self, min_length, eos_token_id)`
- `__call__(self, input_ids, logits)`

### `MaxLengthProcessor`

Force EOS token after maximum length is reached.

**Methods** (2):
- `__init__(self, max_length, eos_token_id)`
- `__call__(self, input_ids, logits)`

### `PresencePenaltyProcessor`

Additive penalty for tokens that have appeared.

Unlike RepetitionPenalty (multiplicative), this adds a flat penalty
to any token that has appeared at least once.

**Methods** (2):
- `__init__(self, penalty)`
- `__call__(self, input_ids, logits)`

### `FrequencyPenaltyProcessor`

Penalty proportional to token frequency.

Tokens that appear more often receive a larger penalty.

**Methods** (2):
- `__init__(self, penalty)`
- `__call__(self, input_ids, logits)`

## Functions (2)

### `apply_processors(input_ids, logits)`

Apply multiple processors to logits.

Convenience function for one-off processing.

Args:
    input_ids: Past token IDs
    logits: Logits tensor
    *processors: Processors to apply
    
Returns:
    Modified logits

### `create_processor_chain(temperature, top_k, top_p, repetition_penalty, presence_penalty, frequency_penalty, bad_words_ids, min_length, max_length, eos_token_id)`

Create a standard processor chain from common parameters.

Returns:
    LogitsProcessorList with configured processors

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `collections.Counter`
- `collections.abc.Callable`
- `collections.abc.Sequence`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `rust_core`
- `torch`
- `typing.Any`
- `typing.Protocol`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
