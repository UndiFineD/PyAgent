# JsonConstraint

**File**: `src\infrastructure\decoding\grammar\JsonConstraint.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 213  
**Complexity**: 12 (moderate)

## Overview

JSON schema constraint logic for structured output decoding.

## Classes (1)

### `JSONSchemaGrammar`

**Inherits from**: StructuredOutputGrammar

Grammar that constrains output to match a JSON schema.

Converts JSON schema to a regex pattern for validation.
Inspired by vLLM's xgrammar and outlines backends.

**Methods** (12):
- `__post_init__(self)`
- `_schema_to_regex(self, schema)`
- `accept_tokens(self, request_id, tokens)`
- `_is_valid_prefix(self, text)`
- `_is_valid_json_prefix(self, text)`
- `validate_tokens(self, tokens)`
- `rollback(self, num_tokens)`
- `fill_bitmask(self, bitmask, idx)`
- `get_valid_tokens(self)`
- `is_terminated(self)`
- ... and 2 more methods

## Dependencies

**Imports** (13):
- `Base.StructuredOutputGrammar`
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `json`
- `numpy`
- `re`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
