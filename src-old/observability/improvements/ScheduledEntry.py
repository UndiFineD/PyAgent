#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/observability/improvements/ScheduledEntry.description.md

# ScheduledEntry

**File**: `src\observability\improvements\ScheduledEntry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 32  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_improvements.py

## Classes (1)

### `ScheduledEntry`

Compatibility scheduled entry used by tests.

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `src.core.base.version.VERSION`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/observability/improvements/ScheduledEntry.improvements.md

# Improvements for ScheduledEntry

**File**: `src\observability\improvements\ScheduledEntry.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 32 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ScheduledEntry_test.py` with pytest tests

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

from src.core.base.version import VERSION
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

__version__ = VERSION


@dataclass
class ScheduledEntry:
    """Compatibility scheduled entry used by tests."""

    improvement_id: str
    start_date: datetime
    resources: list[str] = field(default_factory=list)  # type: ignore[assignment]
