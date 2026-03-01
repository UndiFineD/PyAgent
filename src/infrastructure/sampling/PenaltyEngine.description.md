# PenaltyEngine

**File**: `src\infrastructure\sampling\PenaltyEngine.py`  
**Type**: Python Module  
**Summary**: 6 classes, 3 functions, 11 imports  
**Lines**: 529  
**Complexity**: 23 (complex)

## Overview

Penalty Engine for Token Penalization.

This module provides comprehensive penalty application for LLM sampling:
- Repetition penalty (multiplicative)
- Frequency penalty (additive, proportional to count)
- Presence penalty (additive, binary)
- Bad words blocking

Beyond vLLM innovations:
- Penalty scheduling (warmup, decay)
- Positional penalties (distance-based decay)
- N-gram repetition penalties
- Context-aware penalty strength
- Batch-optimized operations

## Classes (6)

### `PenaltyType`

**Inherits from**: Enum

Types of penalties.

### `PenaltySchedule`

**Inherits from**: Enum

Penalty scheduling strategies.

### `PenaltyConfig`

Configuration for penalty engine.

**Methods** (1):
- `__post_init__(self)`

### `PenaltyState`

Mutable state for penalty tracking.

**Methods** (5):
- `update_counts(self, token)`
- `update_ngram(self, ngram)`
- `get_token_count(self, token)`
- `get_ngram_count(self, ngram)`
- `reset(self)`

### `PenaltyEngine`

Comprehensive penalty engine for token penalization.

Implements vLLM's penalty application with extensions for:
- Penalty scheduling
- Positional decay
- N-gram penalties
- Context-aware strength

**Methods** (13):
- `__init__(self, config)`
- `apply_penalties(self, logits, prompt_tokens, output_tokens)`
- `_apply_repetition_penalty(self, logits, token_set, penalty)`
- `_apply_frequency_penalty(self, logits, output_tokens, penalty)`
- `_apply_presence_penalty(self, logits, token_set, penalty)`
- `_apply_ngram_penalty(self, logits, tokens, n, penalty)`
- `_apply_positional_penalty(self, logits, tokens, decay)`
- `_apply_bad_words(self, logits, past_tokens)`
- `_get_scheduled_penalty(self, base_penalty, base)`
- `add_bad_word(self, token_or_sequence)`
- ... and 3 more methods

### `BatchPenaltyEngine`

Batch-optimized penalty engine.

Efficiently applies penalties to multiple sequences
with different configurations.

**Methods** (1):
- `apply_batch_penalties(self, logits, repetition_penalties, frequency_penalties, presence_penalties, prompt_tokens, output_tokens)`

## Functions (3)

### `apply_repetition_penalty(logits, tokens, penalty)`

Apply repetition penalty to logits.

### `apply_frequency_penalty(logits, output_tokens, penalty)`

Apply frequency penalty to logits.

### `apply_presence_penalty(logits, tokens, penalty)`

Apply presence penalty to logits.

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `math`
- `numpy`
- `numpy.typing.NDArray`
- `rust_core`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
