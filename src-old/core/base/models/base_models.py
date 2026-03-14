#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/models/base_models.description.md

# base_models

**File**: `src\\core\base\\models\base_models.py`  
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
## Source: src-old/core/base/models/base_models.improvements.md

# Improvements for base_models

**File**: `src\\core\base\\models\base_models.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 174 lines (medium)  
**Complexity**: 18 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `base_models_test.py` with pytest tests

### Code Organization
- [TIP] **9 classes in one file** - Consider splitting into separate modules

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""
from __future__ import annotations


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Base model classes and utility functions."""
