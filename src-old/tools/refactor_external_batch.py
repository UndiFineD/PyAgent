#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/refactor_external_batch.description.md

# refactor_external_batch

**File**: `src\tools\refactor_external_batch.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 6 imports  
**Lines**: 178  
**Complexity**: 6 (moderate)

## Overview

Batch-safe refactor/copy of .external Python files into src/external_candidates.

Features:
- Recursively scans ROOT/.external for .py files
- Performs lightweight AST safety checks to detect `eval`, `exec`, `os.system`, `subprocess` usages
- Sanitizes filenames to snake_case and writes to a mirrored directory under `src/external_candidates/ingested`
- Produces a JSON mapping and log file, supports `--limit` and `--dry-run`

## Functions (6)

### `parse_allowlist(s)`

### `sanitize_filename(name)`

### `is_ast_safe(src, filename, allow_modules, allow_attrs, allow_names, allow_limited_shell, allow_eval)`

### `file_hash(p)`

### `process(limit, start, dry_run, verbose, allow_modules, allow_attrs, allow_names, allow_limited_shell, allow_eval)`

### `main()`

## Dependencies

**Imports** (6):
- `argparse`
- `ast`
- `hashlib`
- `json`
- `pathlib.Path`
- `re`

---
*Auto-generated documentation*
## Source: src-old/tools/refactor_external_batch.improvements.md

# Improvements for refactor_external_batch

**File**: `src\tools\refactor_external_batch.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 178 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `refactor_external_batch_test.py` with pytest tests

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

r"""Batch-safe refactor/copy of .external Python files into src/external_candidates.

Features:
- Recursively scans ROOT/.external for .py files
- Performs lightweight AST safety checks to detect `eval`, `exec`, `os.system`, `subprocess` usages
- Sanitizes filenames to snake_case and writes to a mirrored directory under `src/external_candidates/ingested`
- Produces a JSON mapping and log file, supports `--limit` and `--dry-run`
"""
