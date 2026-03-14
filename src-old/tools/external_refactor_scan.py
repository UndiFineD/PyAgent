#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/external_refactor_scan.description.md

# external_refactor_scan

**File**: `src\tools\\external_refactor_scan.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 7 imports  
**Lines**: 175  
**Complexity**: 6 (moderate)

## Overview

Safe scanner for `.external` repository snapshots.
- Reads `.external/tracking.md` and extracts completed/integrated table rows.
- Builds a per-directory candidate list of files and exported functions/classes.
- Does NOT execute any external code; it only reads and regex-parses files.
- Produces `.external/refactor_report.md` and `.external/refactor_report.json`.

Usage (PowerShell):
python -m src.tools.external_refactor_scan

Run only after reviewing and ensuring safety.

## Functions (6)

### `extract_completed_from_tracking(tracking_path)`

### `scan_directory_for_candidates(dirpath)`

### `is_definition_in_src(name, src_root)`

### `build_reuse_report(external_root, src_root)`

### `write_reports(report, md_path, json_path)`

### `main()`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `json`
- `os`
- `pathlib.Path`
- `re`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/tools/external_refactor_scan.improvements.md

# Improvements for external_refactor_scan

**File**: `src\tools\\external_refactor_scan.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 175 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `external_refactor_scan_test.py` with pytest tests

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


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""
Safe scanner for `.external` repository snapshots.
- Reads `.external/tracking.md` and extracts completed/integrated table rows.
- Builds a per-directory candidate list of files and exported functions/classes.
- Does NOT execute any external code; it only reads and regex-parses files.
- Produces `.external/refactor_report.md` and `.external/refactor_report.json`.

Usage (PowerShell):
python -m src.tools.external_refactor_scan

Run only after reviewing and ensuring safety.
"""
