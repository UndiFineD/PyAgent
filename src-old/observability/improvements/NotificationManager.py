#!/usr/bin/env python3
r"""
LLM_CONTEXT_START

## Source: src-old/observability/improvements/NotificationManager.description.md

# NotificationManager

**File**: `src\observability\improvements\NotificationManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 50  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent_improvements.py

## Classes (1)

### `NotificationManager`

Notifies subscribers about improvement changes.

**Methods** (5):
- `__init__(self)`
- `subscribe(self, improvement_id, subscriber)`
- `get_subscribers(self, improvement_id)`
- `on_notification(self, callback)`
- `notify_status_change(self, improvement_id, old_status, new_status)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `collections.abc.Callable`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/observability/improvements/NotificationManager.improvements.md

# Improvements for NotificationManager

**File**: `src\observability\improvements\NotificationManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 50 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `NotificationManager_test.py` with pytest tests

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


r"""Auto-extracted class from agent_improvements.py"""
