"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/system/mixins/MapBuilderMixin.description.md

# MapBuilderMixin

**File**: `src\logic\agents\system\mixins\MapBuilderMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 81  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for MapBuilderMixin.

## Classes (1)

### `MapBuilderMixin`

Mixin for mapping and parsing code entities in TopologicalNavigator.

**Methods** (3):
- `_get_entity_id(self, file_path, entity_name)`
- `build_dependency_map(self, target_dir)`
- `_parse_file(self, file_path)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `ast`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.BaseUtilities.as_tool`
- `src.logic.agents.system.TopologicalNavigator.TopologicalNavigator`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/mixins/MapBuilderMixin.improvements.md

# Improvements for MapBuilderMixin

**File**: `src\logic\agents\system\mixins\MapBuilderMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 81 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MapBuilderMixin_test.py` with pytest tests

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

import os
import ast
import logging
from src.logic.agents.system.TopologicalNavigator import TopologicalNavigator
from pathlib import Path
from typing import TYPE_CHECKING
from src.core.base.BaseUtilities import as_tool

class MapBuilderMixin:
    """Mixin for mapping and parsing code entities in TopologicalNavigator."""

    def _get_entity_id(
        self: TopologicalNavigator, file_path: Path, entity_name: str = ""
    ) -> str:
        """Generates a unique ID for a code entity."""
        rel_path = file_path.relative_to(self.root_dir)
        module_path = str(rel_path).replace(os.path.sep, ".").replace(".py", "")
        if entity_name:
            return f"{module_path}.{entity_name}"
        return module_path

    @as_tool
    def build_dependency_map(
        self: TopologicalNavigator, target_dir: str = "src"
    ) -> str:
        """Scans the specified directory to build a full dependency graph."""
        target_path = self.root_dir / target_dir
        if not target_path.exists():
            return f"Error: Path {target_dir} does not exist."

        count = 0
        for py_file in target_path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            self._parse_file(py_file)
            count += 1

        return f"Dependency map built successfully. Indexed {count} files. Total nodes: {len(self.graph)}"

    def _parse_file(self: TopologicalNavigator, file_path: Path) -> None:
        """Extracts imports and class/function definitions from a file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                tree = ast.parse(f.read())

            module_id = self._get_entity_id(file_path)
            if module_id not in self.graph:
                self.graph[module_id] = set()

            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    # Extract imports to find module-level dependencies
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.graph[module_id].add(alias.name)
                    else:
                        if node.module:
                            self.graph[module_id].add(node.module)

                elif isinstance(node, ast.ClassDef):
                    class_id = self._get_entity_id(file_path, node.name)
                    if class_id not in self.graph:
                        self.graph[class_id] = set()
                    # Add class as dependee of module
                    self.graph[module_id].add(class_id)

                    # Track base classes
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            self.graph[class_id].add(base.id)

                elif isinstance(node, ast.FunctionDef):
                    func_id = self._get_entity_id(file_path, node.name)
                    if func_id not in self.graph:
                        self.graph[func_id] = set()
                    self.graph[module_id].add(func_id)

        except Exception as e:
            logging.error(f"Failed to parse {file_path}: {e}")
