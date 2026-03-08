#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/observability/errors/ErrorPattern.description.md

# ErrorPattern

**File**: `src\observability\errors\ErrorPattern.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_errors.py

## Classes (1)

### `ErrorPattern`

A recognized error pattern.

## Dependencies

**Imports** (5):
- `ErrorCategory.ErrorCategory`
- `ErrorSeverity.ErrorSeverity`
- `__future__.annotations`
- `dataclasses.dataclass`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/observability/errors/ErrorPattern.improvements.md

# Improvements for ErrorPattern

**File**: `src\observability\errors\ErrorPattern.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 34 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ErrorPattern_test.py` with pytest tests

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


"""Auto-extracted class from agent_errors.py"""

from src.core.base.version import VERSION
from .ErrorCategory import ErrorCategory
from .ErrorSeverity import ErrorSeverity
from dataclasses import dataclass

__version__ = VERSION


@dataclass
class ErrorPattern:
    """A recognized error pattern."""

    name: str
    regex: str
    severity: ErrorSeverity
    category: ErrorCategory
    suggested_fix: str = ""
    occurrences: int = 0
