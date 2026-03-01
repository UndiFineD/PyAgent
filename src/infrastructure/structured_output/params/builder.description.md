# builder

**File**: `src\infrastructure\structured_output\params\builder.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 101  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for builder.

## Classes (1)

### `ConstraintBuilder`

Fluent builder for structured output constraints.

**Methods** (12):
- `__init__(self)`
- `json_schema(self, schema, strict)`
- `json_object(self)`
- `regex(self, pattern, flags)`
- `choices(self, options, case_sensitive)`
- `grammar(self, grammar_spec, grammar_type)`
- `backend(self, backend, fallback)`
- `whitespace(self, pattern, custom)`
- `add_constraint(self, constraint)`
- `max_tokens(self, tokens)`
- ... and 2 more methods

## Dependencies

**Imports** (9):
- `config.StructuredOutputConfig`
- `constraints.OutputConstraint`
- `enums.GuidedDecodingBackend`
- `enums.StructuredOutputType`
- `enums.WhitespacePattern`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
