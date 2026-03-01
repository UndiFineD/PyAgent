# base_models

**File**: `src\core\base\models\base_models.py`  
**Type**: Python Module  
**Summary**: 9 classes, 16 functions, 16 imports  
**Lines**: 174  
**Complexity**: 18 (moderate)

## Overview

Base model classes and utility functions.

## Classes (9)

### `CacheEntry`

Cached response entry.

### `AuthConfig`

Authentication configuration.

### `SerializationConfig`

Configuration for custom serialization.

### `FilePriorityConfig`

Configuration for file priority.

### `ExecutionCondition`

A condition for agent execution.

### `ValidationRule`

Consolidated validation rule for Phase 126.

**Methods** (1):
- `__post_init__(self)`

### `ModelConfig`

Model configuration.

### `ConfigProfile`

Configuration profile.

**Methods** (1):
- `get(self, key, default)`

### `DiffResult`

Result of a diff operation.

## Functions (16)

### `_empty_agent_event_handlers()`

### `_empty_list_str()`

### `_empty_list_int()`

### `_empty_list_float()`

### `_empty_list_dict_str_any()`

### `_empty_dict_str_float()`

### `_empty_dict_str_any()`

### `_empty_dict_str_int()`

### `_empty_dict_str_str()`

### `_empty_dict_str_callable_any_any()`

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `collections.abc.Callable`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enums.AgentEvent`
- `enums.AuthMethod`
- `enums.DiffOutputFormat`
- `enums.FilePriority`
- `enums.SerializationFormat`
- `pathlib.Path`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 1 more

---
*Auto-generated documentation*
