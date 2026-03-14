#!/usr/bin/env python3
r"""
LLM_CONTEXT_START

## Source: src-old/classes/base_agent/managers/PluginManager.description.md

# PluginManager

**File**: `src\classes\base_agent\managers\PluginManager.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 19 imports  
**Lines**: 169  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for PluginManager.

## Classes (2)

### `PluginMetadata`

Strictly typed metadata for a plugin.

### `PluginManager`

Modernized PluginManager (Phase 226).
Handles discovery, manifest enforcement, health tracking, and graceful shutdown.

**Methods** (7):
- `__init__(self, workspace_root)`
- `discover(self)`
- `validate_version(self, required_version)`
- `load_plugin(self, plugin_name)`
- `shutdown_all(self)`
- `activate_all(self)`
- `deactivate(self, name)`

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `importlib`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.AgentPluginBase.AgentPluginBase`
- `src.core.base.version.SDK_VERSION`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.VersionGate.VersionGate`
- `sys`
- `typing.Any`
- `typing.Dict`
- ... and 4 more

---
*Auto-generated documentation*
## Source: src-old/classes/base_agent/managers/PluginManager.improvements.md

# Improvements for PluginManager

**File**: `src\classes\base_agent\managers\PluginManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 169 lines (medium)  
**Complexity**: 7 score (moderate)

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


import importlib
import json
import logging
import os
import sys
from src.core.base.AgentPluginBase import AgentPluginBase
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TYPE_CHECKING

from src.core.base.version import VERSION, SDK_VERSION

    pass

    # Optional import for VersionGate
try:
    from src.infrastructure.fleet.VersionGate import VersionGate
except ImportError:
    VersionGate = None

@dataclass
class PluginMetadata:
    """
    """
