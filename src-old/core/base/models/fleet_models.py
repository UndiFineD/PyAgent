#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/models/fleet_models.description.md

# fleet_models

**File**: `src\\core\base\\models\fleet_models.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 14 imports  
**Lines**: 84  
**Complexity**: 4 (simple)

## Overview

Models for fleet - wide state and resource management.

## Classes (5)

### `HealthCheckResult`

Result of agent health check.

### `IncrementalState`

State for incremental processing.

### `RateLimitConfig`

Configuration for rate limiting.

### `TokenBudget`

Manages token allocation.

**Methods** (4):
- `used(self)`
- `remaining(self)`
- `allocate(self, name, tokens)`
- `release(self, name)`

### `ShutdownState`

State for graceful shutdown.

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `base_models._empty_dict_str_any`
- `base_models._empty_dict_str_float`
- `base_models._empty_dict_str_int`
- `base_models._empty_dict_str_str`
- `base_models._empty_list_str`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enums.RateLimitStrategy`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/models/fleet_models.improvements.md

# Improvements for fleet_models

**File**: `src\\core\base\\models\fleet_models.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 84 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `fleet_models_test.py` with pytest tests

### Code Organization
- [TIP] **5 classes in one file** - Consider splitting into separate modules

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

r"""Models for fleet - wide state and resource management."""
