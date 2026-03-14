#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/extract_candidates.description.md

# extract_candidates

**File**: `src\tools\\extract_candidates.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 8 imports  
**Lines**: 195  
**Complexity**: 6 (moderate)

## Overview

AST-based extractor: reads .external/refactor_report.json, selects safe Python files,
and extracts them into `src/external_candidates/auto/` with provenance headers.
Also generates minimal tests in `tests/unit/` that import the extracted file via
importlib and assert presence of top-level defs.

Safety checks (static-only):
- file suffix must be .py
- file size and line count under configurable limits
- module top-level must contain only imports, defs, and module docstring (no exec code)
- disallow imports of dangerous modules and banned names (ctypes, subprocess, eval, exec, compile, importlib, socket, os.system)

Usage:
  python src/tools/extract_candidates.py --report .external/refactor_report.json --limit 10

This script makes small, reversible changes: writes new files under src/external_candidates/auto
and tests under tests/unit/. It does not modify `.external`.

## Functions (6)

### `safe_module(ast_mod, allow_top_level, allow_no_defs, allow_banned_imports)`

Return (is_safe, list_of_defs)

allow_top_level: when True, permit assignments and other top-level statements
allow_no_defs: when True, accept modules with no defs (useful for data or constants)
allow_banned_imports: when True, skip checking banned imports

### `sanitize_filename(s)`

### `write_extracted(source_path, dest_path, provenance, content)`

### `make_test(module_path, defs, test_path)`

### `extract_candidates(report_file, limit, max_lines, max_bytes, allow_top_level, allow_no_defs, allow_banned_imports)`

### `main()`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `argparse`
- `ast`
- `importlib.util`
- `json`
- `pathlib.Path`
- `re`
- `textwrap`

---
*Auto-generated documentation*
## Source: src-old/tools/extract_candidates.improvements.md

# Improvements for extract_candidates

**File**: `src\tools\\extract_candidates.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 195 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `extract_candidates_test.py` with pytest tests

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


"""
AST-based extractor: reads .external/refactor_report.json, selects safe Python files,
and extracts them into `src/external_candidates/auto/` with provenance headers.
Also generates minimal tests in `tests/unit/` that import the extracted file via
importlib and assert presence of top-level defs.

Safety checks (static-only):
- file suffix must be .py
- file size and line count under configurable limits
- module top-level must contain only imports, defs, and module docstring (no exec code)
- disallow imports of dangerous modules and banned names (ctypes, subprocess, eval, exec, compile, importlib, socket, os.system)

Usage:
  python src/tools/extract_candidates.py --report .external/refactor_report.json --limit 10

This script makes small, reversible changes: writes new files under src/external_candidates/auto
and tests under tests/unit/. It does not modify `.external`.
"""
import argparse
import ast
import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = ROOT / ".external" / "refactor_report.json"
OUT_DIR = ROOT / "src" / "external_candidates" / "auto"
TESTS_DIR = ROOT / "tests" / "unit"

MAX_LINES = 800
MAX_BYTES = 200 * 1024

BANNED_IMPORTS = {
    "ctypes",
    "cffi",
    "subprocess",
    "multiprocessing",
    "socket",
    "ssl",
    "paramiko",
}
BANNED_NAMES = {"eval", "exec", "compile", "execfile", "open", "os.system"}


def safe_module(
    ast_mod: ast.Module,
    allow_top_level: bool = False,
    allow_no_defs: bool = False,
    allow_banned_imports: bool = False,
) -> tuple[bool, list[str]]:
    """
    """
