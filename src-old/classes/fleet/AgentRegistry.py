#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/AgentRegistry.description.md

# AgentRegistry

**File**: `src\\classes\fleet\\AgentRegistry.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 16 imports  
**Lines**: 351  
**Complexity**: 21 (complex)

## Overview

Registry for mapping agent names to their implementations and initialization logic.

## Classes (2)

### `LazyAgentMap`

**Inherits from**: dict

A dictionary that instantiates agents only when they are first accessed.

**Methods** (20):
- `__init__(self, workspace_root, registry_configs, fleet_instance)`
- `_scan_workspace_for_agents(self)`
- `_load_manifests(self)`
- `try_reload(self, key)`
- `check_for_registry_cycles(self)`
- `__contains__(self, key)`
- `keys(self)`
- `__iter__(self)`
- `__len__(self)`
- `items(self)`
- ... and 10 more methods

### `AgentRegistry`

Registry for mapping agent names to their implementations via lazy loading.

**Methods** (1):
- `get_agent_map(workspace_root, fleet_instance)`

## Dependencies

**Imports** (16):
- `AgentRegistryCore.AgentRegistryCore`
- `BootstrapConfigs.BOOTSTRAP_AGENTS`
- `FleetManager.FleetManager`
- `ResilientStubs.ResilientStub`
- `__future__.annotations`
- `collections.abc.Iterable`
- `importlib`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.Version.SDK_VERSION`
- `src.core.base.Version.VERSION`
- `src.logic.agents.system.MCPAgent.MCPAgent`
- `typing.Any`
- ... and 1 more

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/AgentRegistry.improvements.md

# Improvements for AgentRegistry

**File**: `src\\classes\fleet\\AgentRegistry.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 351 lines (medium)  
**Complexity**: 21 score (complex)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentRegistry_test.py` with pytest tests

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
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.core.base.Version import VERSION

if TYPE_CHECKING:
    from .FleetManager import FleetManager
from collections.abc import Iterable

from src.logic.agents.system.MCPAgent import MCPAgent

from .AgentRegistryCore import AgentRegistryCore
from .BootstrapConfigs import BOOTSTRAP_AGENTS
from .ResilientStubs import ResilientStub

# Import local version for gatekeeping
__version__ = VERSION


class LazyAgentMap(dict):
    """
    """
