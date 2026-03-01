# constraints

**File**: `src\infrastructure\structured_output\params\constraints.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 12 imports  
**Lines**: 250  
**Complexity**: 14 (moderate)

## Overview

Python module containing implementation for constraints.

## Classes (6)

### `OutputConstraint`

Base output constraint.

**Methods** (2):
- `validate(self, text)`
- `to_dict(self)`

### `JsonSchemaConstraint`

**Inherits from**: OutputConstraint

JSON Schema constraint.

**Methods** (4):
- `validate(self, text)`
- `_validate_schema(self, data)`
- `_validate_property(self, value, prop_schema)`
- `to_dict(self)`

### `RegexConstraint`

**Inherits from**: OutputConstraint

Regex pattern constraint.

**Methods** (3):
- `__post_init__(self)`
- `validate(self, text)`
- `to_dict(self)`

### `ChoiceConstraint`

**Inherits from**: OutputConstraint

Fixed choice constraint.

**Methods** (2):
- `validate(self, text)`
- `to_dict(self)`

### `GrammarConstraint`

**Inherits from**: OutputConstraint

Grammar constraint (EBNF/Lark).

**Methods** (1):
- `to_dict(self)`

### `TypeConstraint`

**Inherits from**: OutputConstraint

Type annotation constraint.

**Methods** (2):
- `validate(self, text)`
- `to_dict(self)`

## Dependencies

**Imports** (12):
- `dataclasses.dataclass`
- `dataclasses.field`
- `enums.ConstraintType`
- `enums.SchemaFormat`
- `json`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Pattern`
- `typing.Type`

---
*Auto-generated documentation*
