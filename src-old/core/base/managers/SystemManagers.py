#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/managers/SystemManagers.description.md

# SystemManagers

**File**: `src\\core\base\\managers\\SystemManagers.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 28 imports  
**Lines**: 348  
**Complexity**: 33 (complex)

## Overview

Python module containing implementation for SystemManagers.

## Classes (6)

### `FilePriorityManager`

Manager for file priority and request ordering.

**Methods** (6):
- `__init__(self, config)`
- `set_pattern_priority(self, pattern, priority)`
- `set_extension_priority(self, extension, priority)`
- `get_priority(self, path)`
- `sort_by_priority(self, paths)`
- `filter_by_priority(self, paths, min_priority)`

### `ResponseCache`

Caches responses based on prompts. 
Supports Prompt Caching (Phase 128) by identifying prefix reusable contexts.

**Methods** (5):
- `__post_init__(self)`
- `_get_cache_key(self, prompt)`
- `set(self, prompt, response)`
- `get(self, prompt)`
- `invalidate(self, prompt)`

### `StatePersistence`

Persists agent state to disk.

**Methods** (2):
- `save(self, state)`
- `load(self, default)`

### `EventManager`

Manages agent events.

**Methods** (2):
- `on(self, event, handler)`
- `emit(self, event, data)`

### `HealthChecker`

Performs health checks on agent components.

**Methods** (10):
- `__init__(self, repo_root, recorder)`
- `add_check(self, name, check_func)`
- `record_request(self, success, latency_ms)`
- `get_metrics(self)`
- `check(self)`
- `check_agent_script(self, agent_name)`
- `check_git(self)`
- `check_python(self)`
- `run_all_checks(self)`
- `is_healthy(self)`

### `ProfileManager`

Manages configuration profiles and execution profiles.

**Methods** (8):
- `__init__(self)`
- `_register_defaults(self)`
- `add_profile(self, profile)`
- `activate(self, name)`
- `set_active(self, name)`
- `get_active_config(self)`
- `active(self)`
- `get_setting(self, key, default)`

## Dependencies

**Imports** (28):
- `__future__.annotations`
- `ast`
- `collections.abc.Callable`
- `dataclasses.dataclass`
- `dataclasses.field`
- `fnmatch`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.models.AgentEvent`
- `src.core.base.models.AgentHealthCheck`
- `src.core.base.models.ConfigProfile`
- `src.core.base.models.ExecutionProfile`
- `src.core.base.models.FilePriority`
- ... and 13 more

---
*Auto-generated documentation*
## Source: src-old/core/base/managers/SystemManagers.improvements.md

# Improvements for SystemManagers

**File**: `src\\core\base\\managers\\SystemManagers.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 348 lines (medium)  
**Complexity**: 33 score (complex)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SystemManagers_test.py` with pytest tests

### Code Organization
- [TIP] **6 classes in one file** - Consider splitting into separate modules

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
import json
import logging
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.core.base.models import (
    AgentEvent,
    AgentHealthCheck,
    ConfigProfile,
    ExecutionProfile,
    FilePriority,
    FilePriorityConfig,
    HealthStatus,
    _empty_agent_event_handlers,
    _empty_dict_str_str,
)

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
# Optional import for PluginManager
from src.core.base.version import VERSION

try:
    from src.infrastructure.fleet.VersionGate import VersionGate
except ImportError:
    VersionGate = None

__version__ = VERSION

# Phase 108: Multi-Agent Logic Harvesting.
# Intelligence operations are recorded via record_interaction in Agent classes.


class FilePriorityManager:
    """
    """
