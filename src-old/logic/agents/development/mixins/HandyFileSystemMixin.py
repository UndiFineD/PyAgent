"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/HandyFileSystemMixin.description.md

# HandyFileSystemMixin

**File**: `src\logic\agents\development\mixins\HandyFileSystemMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 40  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for HandyFileSystemMixin.

## Classes (1)

### `HandyFileSystemMixin`

Mixin for file system operations in HandyAgent.

**Methods** (1):
- `fast_find(self, query, path)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `shutil`
- `src.core.base.BaseUtilities.as_tool`
- `src.logic.agents.development.HandyAgent.HandyAgent`
- `subprocess`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/mixins/HandyFileSystemMixin.improvements.md

# Improvements for HandyFileSystemMixin

**File**: `src\logic\agents\development\mixins\HandyFileSystemMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 40 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `HandyFileSystemMixin_test.py` with pytest tests

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

import subprocess
import shutil
from typing import TYPE_CHECKING
from src.core.base.BaseUtilities import as_tool

from src.logic.agents.development.HandyAgent import HandyAgent


class HandyFileSystemMixin:
    """Mixin for file system operations in HandyAgent."""

    @as_tool
    def fast_find(self: HandyAgent, query: str, path: str = ".") -> str:
        """Intelligently find files using system tools (find/fd or git ls-files)."""
        try:
            # Check if fd is available, otherwise use find
            if shutil.which("fd"):
                result = subprocess.check_output(["fd", query, path], text=True)
            elif shutil.which("git"):
                # git ls-files | grep required shell or manual piping
                # Added # nosec to suppress security warning for git/grep chain as it is manually piped
                p1 = subprocess.Popen(
                    ["git", "ls-files"], stdout=subprocess.PIPE
                )  # nosec
                result = subprocess.check_output(
                    ["grep", query], stdin=p1.stdout, text=True
                )  # nosec
                p1.stdout.close()
            else:
                result = subprocess.check_output(
                    ["find", path, "-name", f"*{query}*"], text=True
                )

            return (
                f"### 🔍 Search Results for '{query}':\n```text\n{result[:1000]}\n```"
            )
        except Exception as e:
            return f"Search failed: {e}"
