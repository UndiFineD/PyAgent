#!/usr/bin/env python3
"""
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
    """Run a focused pytest subset based on changed file names.

    Args:
        files: Iterable of changed file paths (relative or absolute).
        timeout: Timeout in seconds for the pytest invocation.

    Returns:
        (success: bool, output: str)

    Behavior:
        - Extracts base names from files and builds a -k expression joining with 'or'.
        - If no file names can be extracted, runs the entire `tests/unit` suite as a conservative fallback.
    """
    basenames = []
    for p in files:
        try:
            pn = Path(p).name
            stem = Path(pn).stem
            if stem:
                basenames.append(stem)
        except Exception:
            continue

    if basenames:
        # Create a -k expression that matches test names/modules containing any file stem
        kexpr = " or ".join(shlex.quote(b) for b in basenames[:10])
        cmd = _build_pytest_command(kexpr=kexpr)
    else:
        # Fallback to running all unit tests
        cmd = ["python", "-m", "pytest", "tests/unit", "-q"]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = proc.stdout + "\n" + proc.stderr
        return proc.returncode == 0, output
    except subprocess.TimeoutExpired as e:
        return False, f"Timed out after {timeout}s while running pytest: {e}"
    except FileNotFoundError as e:
        return False, f"Pytest runner not found: {e}"
    except Exception as e:
        return False, f"Error running pytest: {e}"
