#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/base/exceptions.description.md

# exceptions

**File**: `src\\core\base\\exceptions.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 2 imports  
**Lines**: 40  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for exceptions.

## Classes (7)

### `PyAgentException`

**Inherits from**: Exception

Base exception for all PyAgent errors.

**Methods** (1):
- `__init__(self, message, error_code)`

### `InfrastructureError`

**Inherits from**: PyAgentException

Errors related to system infrastructure (I/O, Network).

### `LogicError`

**Inherits from**: PyAgentException

Errors related to agent logic or reasoning failure.

### `SecurityError`

**Inherits from**: PyAgentException

Errors related to unauthorized access or safety violations.

### `ModelError`

**Inherits from**: PyAgentException

Errors related to LLM connectivity or output parsing.

### `ConfigurationError`

**Inherits from**: PyAgentException

Errors in settings or manifest validation.

### `CycleInterrupt`

**Inherits from**: PyAgentException

Interruption of an agent cycle (e.g., quota exceeded).

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/exceptions.improvements.md

# Improvements for exceptions

**File**: `src\\core\base\\exceptions.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 40 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `exceptions_test.py` with pytest tests

### Code Organization
- [TIP] **7 classes in one file** - Consider splitting into separate modules

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

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


class PyAgentException(Exception):
    """Base exception for all PyAgent errors."""

    def __init__(self, message: str, error_code: str | None = None) -> None:
        super().__init__(message)
        self.error_code = error_code

class InfrastructureError(PyAgentException):
    """Errors related to system infrastructure (I/O, Network)."""

class LogicError(PyAgentException):
    """Errors related to agent logic or reasoning failure."""

class SecurityError(PyAgentException):
    """Errors related to unauthorized access or safety violations."""

class ModelError(PyAgentException):
    """Errors related to LLM connectivity or output parsing."""

class ConfigurationError(PyAgentException):
    """Errors in settings or manifest validation."""

class CycleInterrupt(PyAgentException):
    """Interruption of an agent cycle (e.g., quota exceeded)."""
