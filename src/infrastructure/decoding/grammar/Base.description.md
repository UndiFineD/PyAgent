# Base

**File**: `src\infrastructure\decoding\grammar\Base.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 15 imports  
**Lines**: 207  
**Complexity**: 12 (moderate)

## Overview

Base classes and parameters for structured output grammar.

## Classes (3)

### `StructuredOutputOptions`

**Inherits from**: Enum

Types of structured output constraints.

Inspired by vLLM's StructuredOutputOptions.

### `StructuredOutputsParams`

Parameters for structured output generation.

Inspired by vLLM's StructuredOutputsParams.
Only one constraint type should be set at a time.

Attributes:
    json: JSON schema (dict or string).
    regex: Regular expression pattern.
    choice: List of valid choices.
    grammar: EBNF grammar string.
    json_object: Just ensure valid JSON object output.
    structural_tag: Tagged section specifications.
    disable_fallback: Don't fall back to other backends.
    disable_any_whitespace: Strict whitespace matching.
    disable_additional_properties: Block extra JSON properties.
    whitespace_pattern: Custom whitespace regex.

**Methods** (4):
- `__post_init__(self)`
- `get_option_type(self)`
- `all_constraints_none(self)`
- `get_spec(self)`

### `StructuredOutputGrammar`

**Inherits from**: ABC

Abstract base class for grammar-constrained decoding.

Inspired by vLLM's StructuredOutputGrammar interface.
Implementations track state and validate tokens against the grammar.

**Methods** (8):
- `accept_tokens(self, request_id, tokens)`
- `validate_tokens(self, tokens)`
- `rollback(self, num_tokens)`
- `fill_bitmask(self, bitmask, idx)`
- `get_valid_tokens(self)`
- `is_terminated(self)`
- `reset(self)`
- `num_processed_tokens(self)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `json`
- `numpy`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Union`

---
*Auto-generated documentation*
