# IncrementalDetokenizer

**File**: `src\infrastructure\engine\IncrementalDetokenizer.py`  
**Type**: Python Module  
**Summary**: 6 classes, 4 functions, 15 imports  
**Lines**: 479  
**Complexity**: 21 (complex)

## Overview

IncrementalDetokenizer - Fast streaming token-to-text conversion.

Inspired by vLLM's v1/engine/detokenizer.py - provides fast and slow paths
for incremental detokenization with stop string detection.

## Classes (6)

### `StopMatch`

Result of stop string matching.

### `IncrementalDetokenizer`

**Inherits from**: ABC

Base class for incremental detokenization.

Converts token IDs to text incrementally, handling special tokens
and stop strings efficiently.

**Methods** (5):
- `__init__(self)`
- `output_token_ids(self)`
- `update(self, new_token_ids, stop_terminated)`
- `get_next_output_text(self, finished, delta)`
- `from_new_request(cls, tokenizer, request)`

### `NoOpDetokenizer`

**Inherits from**: IncrementalDetokenizer

No-op detokenizer when tokenizer is not available.

**Methods** (2):
- `update(self, new_token_ids, stop_terminated)`
- `get_next_output_text(self, finished, delta)`

### `BaseIncrementalDetokenizer`

**Inherits from**: IncrementalDetokenizer, ABC

Base class with common functionality for incremental detokenizers.

**Methods** (4):
- `__init__(self, request)`
- `update(self, new_token_ids, stop_terminated)`
- `decode_next(self, next_token_id)`
- `get_next_output_text(self, finished, delta)`

### `FastIncrementalDetokenizer`

**Inherits from**: BaseIncrementalDetokenizer

Fast incremental detokenizer using tokenizers library's DecodeStream.

Requires tokenizers >= 0.21.1 for DecodeStream support.

**Methods** (3):
- `__init__(self, tokenizer, request)`
- `_protected_step(self, next_token_id)`
- `decode_next(self, next_token_id)`

### `SlowIncrementalDetokenizer`

**Inherits from**: BaseIncrementalDetokenizer

Slow incremental detokenizer using Python-based approach.

Compatible with all tokenizers but slower than FastIncrementalDetokenizer.

**Methods** (3):
- `__init__(self, tokenizer, request)`
- `output_token_ids(self)`
- `decode_next(self, next_token_id)`

## Functions (4)

### `check_stop_strings(output_text, new_char_count, stop, include_in_output)`

Check if any stop strings appear in the output text.

Args:
    output_text: The current output text
    new_char_count: Number of new characters added
    stop: List of stop strings to check
    include_in_output: Whether to include stop string in output
    
Returns:
    Tuple of (matched stop string, truncation index) or None

### `check_stop_strings_rust(output_text, new_char_count, stop, include_in_output)`

Rust-accelerated stop string checking.
Falls back to Python implementation.

### `validate_utf8(text)`

Validate that text is valid UTF-8.

### `validate_utf8_rust(text)`

Rust-accelerated UTF-8 validation.

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `logging`
- `rust_core.check_stop_strings_rust`
- `rust_core.validate_utf8_rust`
- `transformers.PreTrainedTokenizerFast`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
