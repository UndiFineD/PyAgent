#!/usr/bin/env python3
r"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/ValidationRuleManager.description.md

# ValidationRuleManager

**File**: `src\core\base\utils\ValidationRuleManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 111  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `ValidationRuleManager`

Manage custom validation rules per file type.

Example:
    manager=ValidationRuleManager()
    manager.add_rule(ValidationRule(
        name = "max_line_length",
        file_pattern = "*.py",
        validator=lambda content, path: all(len(l) <= 100 for l in content.split("\n")),
        error_message = "Line too long (>100 chars)",
    ))
    results=manager.validate(file_path, content)

**Methods** (5):
- `__init__(self)`
- `add_rule(self, rule)`
- `remove_rule(self, name)`
- `validate(self, file_path, content)`
- `get_rules_for_file(self, file_path)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `fnmatch`
- `pathlib.Path`
- `src.core.base.models.ValidationRule`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/ValidationRuleManager.improvements.md

# Improvements for ValidationRuleManager

**File**: `src\core\base\utils\ValidationRuleManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 111 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ValidationRuleManager_test.py` with pytest tests

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


r"""Auto-extracted class from agent.py"""
