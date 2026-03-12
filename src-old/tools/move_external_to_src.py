#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/tools/move_external_to_src.description.md

# move_external_to_src

**File**: `src\tools\\move_external_to_src.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 6 imports  
**Lines**: 55  
**Complexity**: 0 (simple)

## Overview

Move files from top-level external_candidates into src/external_candidates.
Tries `git mv` for tracked files, falls back to shutil.move for others.
Preserves directory structure and removes empty source dirs afterwards.

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `os`
- `pathlib.Path`
- `shutil`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/tools/move_external_to_src.improvements.md

# Improvements for move_external_to_src

**File**: `src\tools\\move_external_to_src.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 55 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `move_external_to_src_test.py` with pytest tests

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

"""Move files from top-level external_candidates into src/external_candidates.
Tries `git mv` for tracked files, falls back to shutil.move for others.
Preserves directory structure and removes empty source dirs afterwards.
"""
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = ROOT / "src" / "external_candidates"
SRC_TOP = ROOT / "external_candidates"


def main() -> int:
    """Move files from top-level external_candidates into src/external_candidates.

    Returns 0 on success, non-zero on failure. Safe to import without side effects.
    """
    if not SRC_TOP.exists():
        print("No top-level 'external_candidates' directory found; nothing to move.")
        return 0

    moved: list[tuple[str, str]] = []
    for dirpath, dirnames, filenames in os.walk(SRC_TOP):
        rel_dir = os.path.relpath(dirpath, SRC_TOP)
        if rel_dir == ".":
            rel_dir = ""
        target_dir = SRC_ROOT / rel_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        for fn in filenames:
            srcf = Path(dirpath) / fn
            dstf = target_dir / fn
            try:
                # try git mv first
                ret = subprocess.run(
                    ["git", "mv", str(srcf), str(dstf)], cwd=ROOT, check=False
                )
                if ret.returncode != 0:
                    # fallback
                    shutil.move(str(srcf), str(dstf))
            except Exception:
                shutil.move(str(srcf), str(dstf))
            moved.append((str(srcf), str(dstf)))

    # remove empty directories under SRC_TOP
    for dirpath, dirnames, filenames in os.walk(SRC_TOP, topdown=False):
        try:
            os.rmdir(dirpath)
        except Exception:
            pass

    print(f"Moved {len(moved)} files into {SRC_ROOT}")
    for a, b in moved[:200]:
        print(a, "->", b)

    if len(moved) == 0:
        print("No files moved.")
    else:
        print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
