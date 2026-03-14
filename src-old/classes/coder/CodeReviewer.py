#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/CodeReviewer.description.md

# CodeReviewer

**File**: `src\\classes\\coder\\CodeReviewer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 121  
**Complexity**: 3 (simple)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `CodeReviewer`

Automated code review system.

Provides automated code review with actionable suggestions
across multiple categories.

Attributes:
    findings: List of review findings.

Example:
    >>> reviewer=CodeReviewer()
    >>> findings=reviewer.review_code("def foo():\n    pass")

**Methods** (3):
- `__init__(self)`
- `review_code(self, content)`
- `get_summary(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `re`
- `src.core.base.types.ReviewCategory.ReviewCategory`
- `src.core.base.types.ReviewFinding.ReviewFinding`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/CodeReviewer.improvements.md

# Improvements for CodeReviewer

**File**: `src\\classes\\coder\\CodeReviewer.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 121 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CodeReviewer_test.py` with pytest tests

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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

r"""Auto-extracted class from agent_coder.py"""
