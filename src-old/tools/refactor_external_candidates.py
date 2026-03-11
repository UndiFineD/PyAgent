#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/tools/refactor_external_candidates.description.md

# refactor_external_candidates

**File**: `src\tools\refactor_external_candidates.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 3 imports  
**Lines**: 46  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for refactor_external_candidates.

## Functions (2)

### `sanitize(name)`

### `main()`

## Dependencies

**Imports** (3):
- `json`
- `pathlib.Path`
- `re`

---
*Auto-generated documentation*
## Source: src-old/tools/refactor_external_candidates.improvements.md

# Improvements for refactor_external_candidates

**File**: `src\tools\refactor_external_candidates.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 46 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `refactor_external_candidates_test.py` with pytest tests

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

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src" / "external_candidates" / "auto"
DEST_DIR = ROOT / "src" / "external_candidates" / "cleaned"


def sanitize(name: str) -> str:
    base = Path(name).stem
    s = base.lower()
    s = re.sub(r"[^0-9a-z_]", "_", s)
    s = re.sub(r"_+", "_", s)
    s = s.strip("_")
    if not s:
        s = "module"
    if s[0].isdigit():
        s = "_" + s
    return s + ".py"


def main():
    if not SRC_DIR.exists():
        print(f"Source dir not found: {SRC_DIR}")
        return
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    mapping = {}
    for p in sorted(SRC_DIR.iterdir()):
        if p.is_file() and p.suffix == ".py":
            new_name = sanitize(p.name)
            dest = DEST_DIR / new_name
            if dest.exists():
                print(f"Skipping existing: {dest}")
                mapping[str(p)] = str(dest)
                continue
            text = p.read_text(encoding="utf-8")
            header = f"# Extracted from: {p.resolve()}\n"
            dest.write_text(header + text, encoding="utf-8")
            mapping[str(p.relative_to(ROOT))] = str(dest.relative_to(ROOT))
            print(f"Wrote: {dest}")
    map_file = DEST_DIR / "refactor_map.json"
    map_file.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print(f"Wrote mapping to {map_file}")


if __name__ == "__main__":
    main()
