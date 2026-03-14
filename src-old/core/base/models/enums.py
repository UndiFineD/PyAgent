#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/models/enums.description.md

# enums

**File**: `src\\core\base\\models\\enums.py`  
**Type**: Python Module  
**Summary**: 17 classes, 0 functions, 3 imports  
**Lines**: 155  
**Complexity**: 0 (simple)

## Overview

Enum definitions for PyAgent models.

## Classes (17)

### `AgentState`

**Inherits from**: Enum

Agent lifecycle states.

### `ResponseQuality`

**Inherits from**: Enum

AI response quality levels.

### `EventType`

**Inherits from**: Enum

Agent event types for hooks.

### `AuthMethod`

**Inherits from**: Enum

Authentication methods for backends.

### `SerializationFormat`

**Inherits from**: Enum

Custom serialization formats.

### `FilePriority`

**Inherits from**: Enum

File priority levels for request prioritization.

### `InputType`

**Inherits from**: Enum

Input types for multimodal support.

### `AgentType`

**Inherits from**: Enum

Agent type classifications.

### `MessageRole`

**Inherits from**: Enum

Roles for conversation messages.

### `AgentEvent`

**Inherits from**: Enum

Agent event types.

### `AgentExecutionState`

**Inherits from**: Enum

Execution state for an agent run.

### `AgentPriority`

**Inherits from**: Enum

Priority level for agent execution.

### `ConfigFormat`

**Inherits from**: Enum

Configuration file format.

### `DiffOutputFormat`

**Inherits from**: Enum

Output format for diff preview.

### `HealthStatus`

**Inherits from**: Enum

Health status for components.

### `LockType`

**Inherits from**: Enum

File locking type.

### `RateLimitStrategy`

**Inherits from**: Enum

Rate limiting strategy for API calls.

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `enum.Enum`
- `enum.auto`

---
*Auto-generated documentation*
## Source: src-old/core/base/models/enums.improvements.md

# Improvements for enums

**File**: `src\\core\base\\models\\enums.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 155 lines (medium)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `enums_test.py` with pytest tests

### Code Organization
- [TIP] **17 classes in one file** - Consider splitting into separate modules

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

r"""Enum definitions for PyAgent models."""
