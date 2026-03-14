#!/usr/bin/env python3
r"""
LLM_CONTEXT_START

## Source: src-old/core/base/common/utils/test_runner.description.md

# test_runner

**File**: `src\core\base\common\utils\test_runner.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 7 imports  
**Lines**: 70  
**Complexity**: 2 (simple)

## Overview

Test runner utilities.

Provides a small helper to execute focused pytest runs and return results.
Used by agents to verify changes before committing.

## Functions (2)

### `_build_pytest_command(kexpr, extra_args)`

### `run_focused_tests_for_files(files, timeout)`

Run a focused pytest subset based on changed file names.

Args:
    files: Iterable of changed file paths (relative or absolute).
    timeout: Timeout in seconds for the pytest invocation.

Returns:
    (success: bool, output: str)

Behavior:
    - Extracts base names from files and builds a -k expression joining with 'or'.
    - If no file names can be extracted, runs the entire `tests/unit` suite as a conservative fallback.

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `pathlib.Path`
- `shlex`
- `subprocess`
- `typing.Iterable`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/core/base/common/utils/test_runner.improvements.md

# Improvements for test_runner

**File**: `src\core\base\common\utils\test_runner.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 70 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `test_runner_test.py` with pytest tests

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

"""Test runner utilities.

Provides a small helper to execute focused pytest runs and return results.
Used by agents to verify changes before committing.
"""
import shlex
import subprocess
from pathlib import Path
from typing import Iterable, Tuple, Optional


def _build_pytest_command(
    kexpr: Optional[str] = None, extra_args: Optional[Iterable[str]] = None
) -> list[str]:
    cmd = ["python", "-m", "pytest", "-q"]
    if kexpr:
        cmd.extend(["-k", kexpr])
    if extra_args:
        cmd.extend(list(extra_args))
    return cmd


def run_focused_tests_for_files(
    files: Iterable[str], timeout: int = 300
) -> Tuple[bool, str]:
    """
    """
