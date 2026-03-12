"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/system/mixins/FederationMixin.description.md

# FederationMixin

**File**: `src\logic\agents\system\mixins\FederationMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 32  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for FederationMixin.

## Classes (1)

### `FederationMixin`

Mixin for multi-project federation in TopologicalNavigator.

**Methods** (1):
- `federate_with_external_project(self, external_root)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.BaseUtilities.as_tool`
- `src.logic.agents.system.TopologicalNavigator.TopologicalNavigator`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/mixins/FederationMixin.improvements.md

# Improvements for FederationMixin

**File**: `src\logic\agents\system\mixins\FederationMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 32 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `FederationMixin_test.py` with pytest tests

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
from src.logic.agents.system.TopologicalNavigator import TopologicalNavigator

from pathlib import Path
from typing import TYPE_CHECKING
from src.core.base.BaseUtilities import as_tool

class FederationMixin:
    """Mixin for multi-project federation in TopologicalNavigator."""

    @as_tool
    def federate_with_external_project(
        self: TopologicalNavigator, external_root: str
    ) -> str:
        """Indexes an external project and merges its graph into the current map.
        This enables 'Federated Project Intelligence' for multi-repo ecosystems.
        """
        ext_path = Path(external_root)
        if not ext_path.exists():
            return f"Error: External path {external_root} not found."

        # Store previous root to restore later if needed
        original_root = self.root_dir
        self.root_dir = ext_path.absolute()

        try:
            report = self.build_dependency_map(".")
            return f"Federation Success: {report} (External Root: {external_root})"
        finally:
            self.root_dir = original_root
