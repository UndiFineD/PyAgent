#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/mixins/ContextDataMixin.description.md

# ContextDataMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\mixins\\ContextDataMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 98  
**Complexity**: 5 (moderate)

## Overview

Data manipulation logic for GlobalContextEngine.

## Classes (1)

### `ContextDataMixin`

Mixin for fundamental context data operations.

**Methods** (5):
- `get(self, category, key)`
- `set_with_conflict_resolution(self, category, key, value, strategy)`
- `add_fact(self, key, value)`
- `add_insight(self, insight, source_agent)`
- `add_constraint(self, constraint)`

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/mixins/ContextDataMixin.improvements.md

# Improvements for ContextDataMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\mixins\\ContextDataMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 98 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextDataMixin_test.py` with pytest tests

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

r"""Data manipulation logic for GlobalContextEngine."""
