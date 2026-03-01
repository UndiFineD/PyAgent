# config

**File**: `src\infrastructure\structured_output\params\config.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 14 imports  
**Lines**: 124  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for config.

## Classes (2)

### `StructuredOutputConfig`

Complete structured output configuration.

Inspired by vLLM's GuidedDecodingParams.

**Methods** (4):
- `get_primary_constraint(self)`
- `get_all_constraints(self)`
- `to_dict(self)`
- `from_dict(cls, data)`

### `ValidationResult`

Result of structured output validation.

**Methods** (2):
- `has_errors(self)`
- `has_warnings(self)`

## Dependencies

**Imports** (14):
- `constraints.ChoiceConstraint`
- `constraints.GrammarConstraint`
- `constraints.JsonSchemaConstraint`
- `constraints.OutputConstraint`
- `constraints.RegexConstraint`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enums.GuidedDecodingBackend`
- `enums.StructuredOutputType`
- `enums.WhitespacePattern`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
