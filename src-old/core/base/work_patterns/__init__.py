#!/usr/bin/env python3
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

"""LLM_CONTEXT_START

## Source: src-old/core/base/work_patterns/__init__.description.md

# __init__

**File**: `src\\core\base\\work_patterns\\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 3 imports  
**Lines**: 25  
**Complexity**: 0 (simple)

## Overview

Work patterns for PyAgent swarm collaboration.

## Dependencies

**Imports** (3):
- `base_pattern.WorkPattern`
- `debate_pattern.DebateWorkPattern`
- `peer_pattern.PeerWorkPattern`

---
*Auto-generated documentation*
## Source: src-old/core/base/work_patterns/__init__.improvements.md

# Improvements for __init__

**File**: `src\\core\base\\work_patterns\\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 25 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `__init___test.py` with pytest tests

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

"""Work patterns for PyAgent swarm collaboration."""

from .base_pattern import WorkPattern
from .debate_pattern import DebateWorkPattern
from .peer_pattern import PeerWorkPattern

__all__ = [
    "WorkPattern",
    "PeerWorkPattern",
    "DebateWorkPattern",
]
