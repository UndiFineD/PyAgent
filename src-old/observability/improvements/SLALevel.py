#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/observability/improvements/SLALevel.description.md

# SLALevel

**File**: `src\observability\improvements\SLALevel.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 30  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_improvements.py

## Classes (1)

### `SLALevel`

**Inherits from**: Enum

SLA priority levels.

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `enum.Enum`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/observability/improvements/SLALevel.improvements.md

# Improvements for SLALevel

**File**: `src\observability\improvements\SLALevel.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 30 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SLALevel_test.py` with pytest tests

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


"""Auto-extracted class from agent_improvements.py"""

from enum import Enum

from src.core.base.version import VERSION

__version__ = VERSION


class SLALevel(Enum):
    """SLA priority levels."""

    P0 = 1  # 24 hours
    P1 = 2  # 3 days
    P2 = 3  # 1 week
    P3 = 4  # 2 weeks
    P4 = 5  # 1 month
