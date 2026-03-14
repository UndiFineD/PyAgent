#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/mixins/task_manager_mixin.description.md

# task_manager_mixin

**File**: `src\\core\base\\mixins\task_manager_mixin.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 12 imports  
**Lines**: 282  
**Complexity**: 7 (moderate)

## Overview

Task Management Mixin for BaseAgent.
Provides structured task tracking and management, inspired by Adorable's todo tool.

## Classes (2)

### `TaskItem`

Represents a single task item.

**Methods** (4):
- `to_dict(self)`
- `from_dict(cls, data)`
- `complete(self)`
- `reset(self)`

### `TaskManagerMixin`

Mixin providing structured task management capabilities.
Inspired by Adorable's todo tool for tracking agent tasks and workflows.

**Methods** (3):
- `__init__(self)`
- `_load_tasks(self)`
- `_save_tasks(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.common.models.communication_models.CascadeContext`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/task_manager_mixin.improvements.md

# Improvements for task_manager_mixin

**File**: `src\\core\base\\mixins\task_manager_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 282 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `task_manager_mixin_test.py` with pytest tests

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

"""
Task Management Mixin for BaseAgent.
Provides structured task tracking and management, inspired by Adorable's todo tool.
"""
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.base.common.models.communication_models import CascadeContext


@dataclass
class TaskItem:
    """
    """
