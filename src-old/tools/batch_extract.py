#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/batch_extract.description.md

# batch_extract

**File**: `src\tools\batch_extract.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 10 imports  
**Lines**: 111  
**Complexity**: 4 (simple)

## Overview

Batch extractor: split a large refactor report into chunks and run
`extract_candidates.py` in parallel subprocesses.

This script creates temporary chunked reports under `.external/tmp_reports/`
and invokes the extractor on each chunk. It forwards relaxed flags so you can
extract broadly. Use `--allow-top-level` and `--allow-no-defs` to be permissive.

WARNING: this automates extraction at scale and may produce many files. Do not
run on untrusted machines unless you understand the risks.

## Functions (4)

### `chunk_files(report, chunk_size)`

### `make_chunk_report(chunk, idx)`

### `run_chunk(report_path, args_extra)`

### `main()`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `argparse`
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.as_completed`
- `json`
- `math`
- `pathlib.Path`
- `shutil`
- `subprocess`
- `tempfile`

---
*Auto-generated documentation*
## Source: src-old/tools/batch_extract.improvements.md

# Improvements for batch_extract

**File**: `src\tools\batch_extract.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 111 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `batch_extract_test.py` with pytest tests

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


r"""Batch extractor: split a large refactor report into chunks and run
`extract_candidates.py` in parallel subprocesses.

This script creates temporary chunked reports under `.external/tmp_reports/`
and invokes the extractor on each chunk. It forwards relaxed flags so you can
extract broadly. Use `--allow-top-level` and `--allow-no-defs` to be permissive.

WARNING: this automates extraction at scale and may produce many files. Do not
run on untrusted machines unless you understand the risks.
"""
