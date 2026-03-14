#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/agent/AgentFileManager.description.md

# AgentFileManager

**File**: `src\\classes\agent\\AgentFileManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 227  
**Complexity**: 9 (moderate)

## Overview

Python module containing implementation for AgentFileManager.

## Classes (1)

### `AgentFileManager`

Manages file discovery, filtering, and snapshots for the Agent.

**Methods** (9):
- `__init__(self, repo_root, agents_only, ignored_patterns)`
- `is_ignored(self, path)`
- `find_code_files(self, max_files)`
- `load_cascading_codeignore(self, directory)`
- `create_file_snapshot(self, file_path)`
- `restore_from_snapshot(self, file_path, snapshot_id)`
- `cleanup_old_snapshots(self, max_age_days, max_snapshots_per_file)`
- `_group_snapshots_by_filename(self, snapshot_dir)`
- `_prune_snapshot_groups(self, groups, current_time, max_age_seconds, max_count)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `hashlib`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.AgentCore.BaseCore`
- `src.core.base.utils.core_utils.load_codeignore`
- `src.core.base.version.VERSION`
- `time`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/AgentFileManager.improvements.md

# Improvements for AgentFileManager

**File**: `src\\classes\agent\\AgentFileManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 227 lines (medium)  
**Complexity**: 9 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentFileManager_test.py` with pytest tests

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


import hashlib
import logging
import os
import time
from pathlib import Path

from src.core.base.AgentCore import BaseCore
from src.core.base.utils.core_utils import load_codeignore

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
from src.core.base.version import VERSION

__version__ = VERSION


class AgentFileManager:
    """
    """
