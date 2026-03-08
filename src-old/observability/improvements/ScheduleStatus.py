#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/observability/improvements/ScheduleStatus.description.md

# ScheduleStatus

**File**: `src\observability\improvements\ScheduleStatus.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 30  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_improvements.py

## Classes (1)

### `ScheduleStatus`

**Inherits from**: Enum

Status of scheduled improvements.

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `enum.Enum`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/observability/improvements/ScheduleStatus.improvements.md

# Improvements for ScheduleStatus

**File**: `src\observability\improvements\ScheduleStatus.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 30 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ScheduleStatus_test.py` with pytest tests

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


"""Auto-extracted class from agent_improvements.py"""

from src.core.base.version import VERSION
from enum import Enum

__version__ = VERSION


class ScheduleStatus(Enum):
    """Status of scheduled improvements."""

    UNSCHEDULED = "unscheduled"
    SCHEDULED = "scheduled"
    IN_SPRINT = "in_sprint"
    BLOCKED = "blocked"
    OVERDUE = "overdue"
