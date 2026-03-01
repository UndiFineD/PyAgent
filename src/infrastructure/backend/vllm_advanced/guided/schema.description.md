# schema

**File**: `src\infrastructure\backend\vllm_advanced\guided\schema.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 167  
**Complexity**: 10 (moderate)

## Overview

JSON Schema builder for guided decoding.

## Classes (1)

### `JsonSchema`

JSON Schema builder for guided decoding.

**Methods** (10):
- `add_property(self, name, prop_type, required, description, enum, minimum, maximum, min_length, max_length, pattern, items, default)`
- `add_string(self, name, required)`
- `add_integer(self, name, required)`
- `add_number(self, name, required)`
- `add_boolean(self, name, required)`
- `add_array(self, name, items_type, required, min_items, max_items)`
- `add_object(self, name, nested_schema, required)`
- `add_enum(self, name, values, required)`
- `build(self)`
- `to_guided_config(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `models.GuidedConfig`
- `models.GuidedMode`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
