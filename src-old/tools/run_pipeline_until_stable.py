#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/tools/run_pipeline_until_stable.description.md

# run_pipeline_until_stable

**File**: `src\tools\run_pipeline_until_stable.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 5 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

Run run_full_pipeline.py repeatedly until no further changes are detected.
Exit when run_full_pipeline.py returns exit code 10 (stable), or after max iterations.

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `pathlib.Path`
- `subprocess`
- `sys`
- `time`

---
*Auto-generated documentation*
## Source: src-old/tools/run_pipeline_until_stable.improvements.md

# Improvements for run_pipeline_until_stable

**File**: `src\tools\run_pipeline_until_stable.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 34 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `run_pipeline_until_stable_test.py` with pytest tests

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

"""Run run_full_pipeline.py repeatedly until no further changes are detected.
Exit when run_full_pipeline.py returns exit code 10 (stable), or after max iterations.
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RFP = ROOT / "src" / "tools" / "run_full_pipeline.py"
PY = sys.executable


def main() -> int:
    """Run `run_full_pipeline.py` until stable. Returns exit code.

    Safe to import: no top-level sys.exit() or long-running loops.
    """
    MAX_ITER = 50
    SLEEP_BETWEEN = 1

    for i in range(1, MAX_ITER + 1):
        print(f"Run {i}/{MAX_ITER}: invoking pipeline...")
        start = time.time()
        p = subprocess.run([PY, str(RFP)])
        elapsed = time.time() - start
        print(f"Pipeline run {i} exited {p.returncode} in {elapsed:.1f}s")
        if p.returncode == 10:
            print("No changed files detected — stable. Stopping loop.")
            return 0
        if p.returncode != 0:
            print("Pipeline returned non-zero; stopping early.")
            return p.returncode
        # otherwise, changes were processed; loop again
        time.sleep(SLEEP_BETWEEN)

    print(f"Reached max iterations ({MAX_ITER}); stopping.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
