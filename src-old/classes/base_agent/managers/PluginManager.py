#!/usr/bin/env python3
"""
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
    """Strictly typed metadata for a plugin."""
    module_path: str
    class_name: str
    needs_fleet: bool = True
    min_sdk_version: str = "1.0.0"
    version: str = "0.1.0"
    author: str = "Unknown"
    description: str = ""

class PluginManager:
    """
    Modernized PluginManager (Phase 226).
    Handles discovery, manifest enforcement, health tracking, and graceful shutdown.
    """
    
    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        self.workspace_root = workspace_root or Path.cwd()
        self.plugins_dir = self.workspace_root / "plugins"
        self.registry_path = self.plugins_dir / "manifest.json"
        self.loaded_meta: Dict[str, PluginMetadata] = {}
        self.active_plugins: Dict[str, AgentPluginBase] = {}
        self.logger = logging.getLogger("PluginManager")
        
        if not self.plugins_dir.exists():
            try:
                self.plugins_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    def discover(self) -> List[str]:
        """Scans manifest and directory for compatible plugins."""
        discovered = []
        
        # 1. Manifest Enforcement (Priority)
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    data = json.load(f)
                    for key, raw_meta in data.items():
                        try:
                            # Enforce structure
                            if isinstance(raw_meta, list):
                                # Legacy list format support with conversion
                                meta = PluginMetadata(
                                    module_path=raw_meta[0],
                                    class_name=raw_meta[1],
                                    needs_fleet=raw_meta[2] if len(raw_meta) > 2 else True,
                                    min_sdk_version=raw_meta[3] if len(raw_meta) > 3 else "1.0.0"
                                )
                            else:
                                meta = PluginMetadata(**raw_meta)

                            if self.validate_version(meta.min_sdk_version):
                                self.loaded_meta[key] = meta
                                discovered.append(key)
                            else:
                                self.logger.warning(f"Ignoring '{key}': Incompatible SDK requirement {meta.min_sdk_version}")
                        except (TypeError, KeyError) as e:
                            self.logger.error(f"Malformed metadata for '{key}': {e}")
            except Exception as e:
                self.logger.error(f"Failed to read manifest: {e}")
        
        # 2. Dynamic Directory Scan (Flexible Fallback)
        for item in self.plugins_dir.iterdir():
            if item.name == "manifest.json" or item.stem in discovered or item.name.startswith("__"):
                continue
            
            if (item.is_file() and item.suffix == ".py") or (item.is_dir() and (item / "__init__.py").exists()):
                plugin_name = item.stem if item.is_file() else item.name
                discovered.append(plugin_name)
                self.loaded_meta[plugin_name] = PluginMetadata(
                    module_path=f"plugins.{plugin_name}",
                    class_name=plugin_name if "_" not in plugin_name else plugin_name.replace("_", "")
                )
                self.logger.debug(f"Dynamically discovered '{plugin_name}'")
                
        return discovered

    def validate_version(self, required_version: str) -> bool:
        """Centralized semantic version gatekeeper."""
        if not VersionGate:
            return True 
        return VersionGate.is_compatible(SDK_VERSION, required_version)

    def load_plugin(self, plugin_name: str) -> Optional[AgentPluginBase]:
        """Loads and initializes a plugin instance."""
        if plugin_name not in self.loaded_meta:
            return None
        
        meta = self.loaded_meta[plugin_name]
        try:
            module = importlib.import_module(meta.module_path)
            plugin_class = getattr(module, meta.class_name)
            
            instance = plugin_class()
            instance.setup()
            
            # Health check immediately after setup
            health = instance.health_check()
            if health.status != "healthy":
                self.logger.error(f"Plugin '{plugin_name}' failed health check: {health.message}")
                return None
            
            self.active_plugins[plugin_name] = instance
            return instance
        except Exception as e:
            self.logger.error(f"Failed to load plugin '{plugin_name}': {e}")
            return None

    def shutdown_all(self) -> None:
        """Gracefully shuts down all active plugins."""
        for name, plugin in list(self.active_plugins.items()):
            try:
                self.logger.info(f"Shutting down plugin: {name}")
                plugin.shutdown()
                del self.active_plugins[name]
            except Exception as e:
                self.logger.error(f"Error during shutdown of '{name}': {e}")

    # Legacy Compatibility Stubs
    def activate_all(self) -> None:
        for name in self.loaded_meta:
            self.load_plugin(name)

    def deactivate(self, name: str) -> None:
        if name in self.active_plugins:
            try:
                self.active_plugins[name].shutdown()
                del self.active_plugins[name]
            except Exception as e:
                self.logger.error(f"Deactivation failed for '{name}': {e}")
