#!/usr/bin/env python3
r"""
LLM_CONTEXT_START

## Source: src-old/tools/update_tracking_from_report.description.md

# update_tracking_from_report

**File**: `src\tools\update_tracking_from_report.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 2 imports  
**Lines**: 116  
**Complexity**: 6 (moderate)

## Overview

Small utility: parse .external/refactor_report.json and update
.external/tracking.md and .external/completed.md, plus generate
.external/candidates.md with prioritized candidates.

This script is read-only for scanned files and only appends/edits
the tracking/completed/candidates files in-place. It does not
execute any code found in .external.

## Functions (6)

### `load_report()`

### `append_tracking(rows)`

### `move_completed_rows()`

### `build_candidates(report, limit)`

### `write_candidates(cands)`

### `main()`

## Dependencies

**Imports** (2):
- `json`
- `pathlib.Path`

---
*Auto-generated documentation*
## Source: src-old/tools/update_tracking_from_report.improvements.md

# Improvements for update_tracking_from_report

**File**: `src\tools\update_tracking_from_report.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 116 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `update_tracking_from_report_test.py` with pytest tests

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

"""
Small utility: parse .external/refactor_report.json and update
.external/tracking.md and .external/completed.md, plus generate
.external/candidates.md with prioritized candidates.

This script is read-only for scanned files and only appends/edits
the tracking/completed/candidates files in-place. It does not
execute any code found in .external.
"""
