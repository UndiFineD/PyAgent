#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/run_full_pipeline.description.md

# run_full_pipeline

**File**: `src\tools\run_full_pipeline.py`  
**Type**: Python Module  
**Summary**: 0 classes, 8 functions, 20 imports  
**Lines**: 662  
**Complexity**: 8 (moderate)

## Overview

Orchestrate the full external->src pipeline end-to-end with no prompts.

Steps (non-interactive):
  1. Run `batch_extract.py` to extract candidates into `src/external_candidates/auto/`
  2. Run `run_static_checks.py` against the extracted candidates
  3. Run `run_auto_tests.py` to execute generated tests
  4. Run `move_completed.py` to move completed tracking rows (idempotent)
  5. Regenerate `docs/architecture/external_integration.md` summary

This script returns a non-zero exit code if critical steps fail.

## Functions (8)

### `run(cmd, fatal)`

### `compute_sha(path_str)`

Compute sha256 for a file path string (module-level worker).

### `run_checks_for_sha(args)`

Run bandit/semgrep/python-only checks for a single file and write per-sha outputs.
Args: (sha, path_str)
Returns: (sha, results dict)

### `summarize_and_write_doc()`

### `update_refactor_report(report_path, extracted_files)`

### `write_refactor_report_md(report_path, md_path)`

### `_is_init(p)`

### `main()`

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `ast`
- `concurrent.futures`
- `datetime.datetime`
- `hashlib`
- `json`
- `os`
- `pathlib.Path`
- `shutil`
- `sqlite3`
- `src.tools.apply_safe_fixes`
- `src.tools.prepare_refactor_patches`
- `src.tools.run_auto_tests`
- `src.tools.run_static_checks`
- `subprocess`
- ... and 5 more

---
*Auto-generated documentation*
## Source: src-old/tools/run_full_pipeline.improvements.md

# Improvements for run_full_pipeline

**File**: `src\tools\run_full_pipeline.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 662 lines (large)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `run_full_pipeline_test.py` with pytest tests

### File Complexity
- [!] **Large file** (662 lines) - Consider refactoring

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


"""Orchestrate the full external->src pipeline end-to-end with no prompts.

Steps (non-interactive):
  1. Run `batch_extract.py` to extract candidates into `src/external_candidates/auto/`
  2. Run `run_static_checks.py` against the extracted candidates
  3. Run `run_auto_tests.py` to execute generated tests
  4. Run `move_completed.py` to move completed tracking rows (idempotent)
  5. Regenerate `docs/architecture/external_integration.md` summary

This script returns a non-zero exit code if critical steps fail.
"""
import ast
import concurrent.futures
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "src" / "tools"
REPORT = ROOT / ".external" / "refactor_report.json"
EXTRACT_TARGET = ROOT / "src" / "external_candidates" / "auto"
STATIC_DIR = ROOT / ".external" / "static_checks"
DOC = ROOT / "docs" / "architecture" / "external_integration.md"


def run(cmd: list[str], fatal: bool = True) -> int:
    print("RUN:", " ".join(cmd))
    p = subprocess.run(cmd)
    if p.returncode != 0:
        print("Command failed:", cmd, "exit", p.returncode)
        if fatal:
            raise SystemExit(p.returncode)
    return p.returncode


def compute_sha(path_str: str) -> tuple[str, str]:
    """
    """
