# extract_candidates

**File**: `src\tools\extract_candidates.py`  
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
