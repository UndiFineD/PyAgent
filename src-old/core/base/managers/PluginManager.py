#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/managers/PluginManager.description.md

# PluginManager

**File**: `src\\core\base\\managers\\PluginManager.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 12 imports  
**Lines**: 271  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for PluginManager.

## Classes (2)

### `PluginMetadata`

Strictly typed metadata for a plugin.

**Methods** (1):
- `get(self, key, default)`

### `PluginManager`

Modernized PluginManager (Phase 226).
Handles discovery, manifest enforcement, health tracking, and graceful shutdown.

**Methods** (9):
- `__init__(self, workspace_root)`
- `discover(self)`
- `validate_version(self, required_version)`
- `load_plugin(self, plugin_name)`
- `_load_sandboxed_plugin(self, name, meta)`
- `_setup_permission_proxy(self, name, meta)`
- `shutdown_all(self)`
- `activate_all(self)`
- `deactivate(self, name)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `dataclasses.dataclass`
- `docker`
- `importlib`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.AgentPluginBase.AgentPluginBase`
- `src.core.base.Version.SDK_VERSION`
- `src.infrastructure.fleet.VersionGate.VersionGate`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/core/base/managers/PluginManager.improvements.md

# Improvements for PluginManager

**File**: `src\\core\base\\managers\\PluginManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 271 lines (medium)  
**Complexity**: 10 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `PluginManager_test.py` with pytest tests

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


import importlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path

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
from typing import Any

from src.core.base.AgentPluginBase import AgentPluginBase
from src.core.base.Version import SDK_VERSION

    # Optional import for VersionGate
try:
    from src.infrastructure.fleet.VersionGate import VersionGate
except ImportError:
    VersionGate = None


@dataclass
class PluginMetadata:
    """
    """
