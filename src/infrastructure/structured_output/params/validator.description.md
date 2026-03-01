# validator

**File**: `src\infrastructure\structured_output\params\validator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 87  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for validator.

## Classes (1)

### `StructuredOutputValidator`

Validate structured output against constraints.

**Methods** (5):
- `__init__(self, config)`
- `validate(self, text)`
- `validate_partial(self, text)`
- `_could_be_json(self, text)`
- `_could_match_regex(self, text, pattern)`

## Dependencies

**Imports** (6):
- `config.StructuredOutputConfig`
- `config.ValidationResult`
- `constraints.RegexConstraint`
- `json`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
