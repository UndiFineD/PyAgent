#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/tools/run_auto_tests.description.md

# run_auto_tests

**File**: `src\tools\run_auto_tests.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 7 imports  
**Lines**: 64  
**Complexity**: 2 (simple)

## Overview

Run only generated `test_auto_*.py` tests under `tests/unit/`.
This script collects matching test files and invokes pytest on them directly to avoid
collecting unrelated tests.

## Functions (2)

### `_run_file(path_str)`

### `main()`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `argparse`
- `concurrent.futures`
- `os`
- `pathlib.Path`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/tools/run_auto_tests.improvements.md

# Improvements for run_auto_tests

**File**: `src\tools\run_auto_tests.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 64 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `run_auto_tests_test.py` with pytest tests

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

"""Run only generated `test_auto_*.py` tests under `tests/unit/`.
This script collects matching test files and invokes pytest on them directly to avoid
collecting unrelated tests.
"""
import argparse
import concurrent.futures
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS_DIR = ROOT / "tests" / "unit"


def _run_file(path_str: str) -> tuple[str, int]:
    p = subprocess.run([sys.executable, path_str])
    return (path_str, p.returncode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=0,
        help="Number of parallel workers (0=auto)",
    )
    args = parser.parse_args()

    files = sorted(TESTS_DIR.glob("test_auto_*.py"))
    if not files:
        print("No generated tests found (test_auto_*.py)")
        return 0

    # Many generated tests use top-level asserts; run each test file as a separate
    # Python process so top-level asserts execute and tests run in parallel.
    def os_cpu_count() -> int | None:
        try:
            return os.cpu_count()
        except Exception:
            return None

    workers = args.workers or min(len(files), (os_cpu_count() or 2))

    failures = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exc:
        futures = {exc.submit(_run_file, str(p)): p for p in files}
        for fut in concurrent.futures.as_completed(futures):
            path = futures[fut]
            try:
                _, code = fut.result()
            except Exception as e:
                failures += 1
                print("FAILED:", path, "-", e)
                continue
            if code != 0:
                failures += 1
                print("FAILED:", path, f"exit {code}")
    if failures:
        print(f"{failures} test files failed")
    else:
        print("All generated tests passed")
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
