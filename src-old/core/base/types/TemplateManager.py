#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/types/TemplateManager.description.md

# TemplateManager

**File**: `src\\core\base\types\\TemplateManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 101  
**Complexity**: 4 (simple)

## Overview

Auto-extracted class from agent_changes.py

## Classes (1)

### `TemplateManager`

Manages entry templates with placeholders.

Provides template storage and application functionality.

Attributes:
    templates: Dictionary of templates by name.

Example:
    >>> manager=TemplateManager()
    >>> manager.add_template("bug_fix", "Fixed {issue} in {component}")
    >>> text=manager.apply_template("bug_fix", {"issue": "#123", "component": "auth"})

**Methods** (4):
- `__init__(self)`
- `add_template(self, name, template_text, description)`
- `apply_template(self, name, values)`
- `get_template_placeholders(self, name)`

## Dependencies

**Imports** (6):
- `EntryTemplate.EntryTemplate`
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/base/types/TemplateManager.improvements.md

# Improvements for TemplateManager

**File**: `src\\core\base\types\\TemplateManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 101 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TemplateManager_test.py` with pytest tests

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


r"""Auto-extracted class from agent_changes.py"""
