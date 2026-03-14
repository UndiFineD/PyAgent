#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/run_static_checks.description.md

# run_static_checks

**File**: `src\tools\run_static_checks.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 7 imports  
**Lines**: 143  
**Complexity**: 3 (simple)

## Overview

Run static-safety checks on extracted candidates.
Tries to run `bandit` and `semgrep` if available. Writes JSON outputs under ./.external/static_checks/
Usage:
  python src/tools/run_static_checks.py src/external_candidates/auto

## Functions (3)

### `run_python_only_checks(target)`

Run fast AST-based checks for banned imports/names and dangerous calls.
Returns a mapping of file -> list of findings.

### `run_check(check, target)`

### `main(argv)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ast`
- `json`
- `pathlib.Path`
- `shutil`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/tools/run_static_checks.improvements.md

# Improvements for run_static_checks

**File**: `src\tools\run_static_checks.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 143 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `run_static_checks_test.py` with pytest tests

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


"""Run static-safety checks on extracted candidates.
Tries to run `bandit` and `semgrep` if available. Writes JSON outputs under ./.external/static_checks/
Usage:
  python src/tools/run_static_checks.py src/external_candidates/auto
"""
import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / ".external" / "static_checks"

CHECKS = [
    {
        "name": "bandit",
        "cmd": lambda target, out: [
            "bandit",
            "-r",
            str(target),
            "-f",
            "json",
            "-o",
            str(out),
        ],
        "out_suffix": "bandit.json",
        "install_hint": "pip install bandit",
    },
    {
        "name": "semgrep",
        "cmd": lambda target, out: [
            "semgrep",
            "--config",
            "auto",
            "--json",
            "--output",
            str(out),
            str(target),
        ],
        "out_suffix": "semgrep.json",
        "install_hint": "pip install semgrep",
    },
]


def run_python_only_checks(target: Path) -> dict:
    """
    """
