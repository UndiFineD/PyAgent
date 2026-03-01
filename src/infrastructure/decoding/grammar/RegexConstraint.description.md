# RegexConstraint

**File**: `src\infrastructure\decoding\grammar\RegexConstraint.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 10 imports  
**Lines**: 279  
**Complexity**: 19 (moderate)

## Overview

Regex and choice constraint logic for structured output decoding.

## Classes (2)

### `RegexGrammar`

**Inherits from**: StructuredOutputGrammar

Grammar that constrains output to match a regex pattern.

Uses DFA-based matching for efficient token validation.
Inspired by vLLM's outlines backend.

**Methods** (10):
- `__post_init__(self)`
- `accept_tokens(self, request_id, tokens)`
- `_is_valid_prefix(self, text)`
- `validate_tokens(self, tokens)`
- `rollback(self, num_tokens)`
- `fill_bitmask(self, bitmask, idx)`
- `get_valid_tokens(self)`
- `is_terminated(self)`
- `reset(self)`
- `num_processed_tokens(self)`

### `ChoiceGrammar`

**Inherits from**: StructuredOutputGrammar

Grammar that constrains output to one of several choices.

Efficient matching by tracking which choices remain possible.

**Methods** (9):
- `__post_init__(self)`
- `accept_tokens(self, request_id, tokens)`
- `validate_tokens(self, tokens)`
- `rollback(self, num_tokens)`
- `fill_bitmask(self, bitmask, idx)`
- `get_valid_tokens(self)`
- `is_terminated(self)`
- `reset(self)`
- `num_processed_tokens(self)`

## Dependencies

**Imports** (10):
- `Base.StructuredOutputGrammar`
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `re`
- `typing.Callable`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
