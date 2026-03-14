#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/agent/FileLockManager.description.md

# FileLockManager

**File**: `src\\classes\agent\\FileLockManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 133  
**Complexity**: 4 (simple)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `FileLockManager`

Manages file locks to prevent concurrent modifications.

Provides advisory file locking to coordinate access between
multiple agent instances or processes.

Attributes:
    locks: Dict of active file locks.
    lock_timeout: Default lock timeout in seconds.

**Methods** (4):
- `__init__(self, lock_timeout)`
- `acquire_lock(self, file_path, lock_type, timeout)`
- `release_lock(self, file_path)`
- `_cleanup_expired_locks(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.models.LockType`
- `src.core.base.utils.FileLock.FileLock`
- `src.core.base.version.VERSION`
- `threading`
- `time`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/FileLockManager.improvements.md

# Improvements for FileLockManager

**File**: `src\\classes\agent\\FileLockManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 133 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `FileLockManager_test.py` with pytest tests

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
