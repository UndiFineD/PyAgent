#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/tools/move_completed.description.md

# move_completed

**File**: `src\tools\\move_completed.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 3 imports  
**Lines**: 94  
**Complexity**: 3 (simple)

## Overview

Move completed rows from .external/tracking.md to .external/completed.md

Idempotent: will not duplicate entries already present in completed.md.
It treats table rows where the second column (status) contains
case-insensitive 'completed'|'done'|'finished' as completed.

## Functions (3)

### `parse_row(line)`

### `is_completed_status(s)`

### `main()`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `datetime`
- `pathlib.Path`

---
*Auto-generated documentation*
## Source: src-old/tools/move_completed.improvements.md

# Improvements for move_completed

**File**: `src\tools\\move_completed.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 94 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `move_completed_test.py` with pytest tests

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

"""Move completed rows from .external/tracking.md to .external/completed.md

Idempotent: will not duplicate entries already present in completed.md.
It treats table rows where the second column (status) contains
case-insensitive 'completed'|'done'|'finished' as completed.
"""
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRACK = ROOT / ".external" / "tracking.md"
COMP = ROOT / ".external" / "completed.md"


def parse_row(line: str) -> list[str] | None:
    if not line.strip().startswith("|"):
        return None
    parts = [p.strip() for p in line.strip().split("|")[1:-1]]
    return parts


def is_completed_status(s: str) -> bool:
    if not s:
        return False
    s2 = s.lower()
    for kw in ("completed", "done", "finished", "closed"):
        if kw in s2:
            return True
    return False


def main():
    if not TRACK.exists():
        print("tracking file missing:", TRACK)
        return 2
    text = TRACK.read_text(encoding="utf-8", errors="ignore").splitlines()
    header_lines = []
    rows = []
    moved = []
    started_rows = False
    for ln in text:
        if ln.strip().startswith("|"):
            started_rows = True
            rows.append(ln)
        else:
            if not started_rows:
                header_lines.append(ln)
            else:
                # footer or blank after table
                header_lines.append(ln)

    # load completed existing set
    existing = set()
    if COMP.exists():
        for ln in COMP.read_text(encoding="utf-8", errors="ignore").splitlines():
            existing.add(ln.strip())

    keep = []
    for r in rows:
        parts = parse_row(r)
        if parts is None or len(parts) < 2:
            keep.append(r)
            continue
        status = parts[1]
        if is_completed_status(status):
            if r.strip() not in existing:
                moved.append(r)
        else:
            keep.append(r)

    if moved:
        COMP.parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.datetime.utcnow().isoformat() + "Z"
        with COMP.open("a", encoding="utf-8") as f:
            f.write(f"<!-- moved on {stamp} -->\n")
            for r in moved:
                f.write(r + "\n")
        print("Moved", len(moved), "rows to", COMP)
        # write back tracking with header_lines + keep rows
        out_lines = []
        out_lines.extend(header_lines)
        out_lines.append("")
        out_lines.extend(keep)
        TRACK.write_text("\n".join(out_lines), encoding="utf-8")
    else:
        print("No completed rows found")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
