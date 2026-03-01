# json_schema

**File**: `src\infrastructure\structured_output\json_schema.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 146  
**Complexity**: 10 (moderate)

## Overview

JSON Schema to grammar engine.

## Classes (1)

### `JsonSchemaGrammar`

**Inherits from**: GrammarEngine

JSON Schema to grammar conversion.

**Methods** (10):
- `__init__(self, vocab_size, token_strings, eos_token_id)`
- `build_fsm(self, spec)`
- `_schema_to_fsm(self, schema)`
- `_build_object_fsm(self, schema)`
- `_build_array_fsm(self, schema)`
- `_build_string_fsm(self, schema)`
- `_build_number_fsm(self, schema)`
- `_build_boolean_fsm(self)`
- `_build_null_fsm(self)`
- `_build_generic_json_fsm(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `base.GrammarEngine`
- `json`
- `models.FSMTransitionTable`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
