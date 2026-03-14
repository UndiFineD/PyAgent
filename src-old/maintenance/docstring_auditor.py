#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/maintenance/docstring_auditor.description.md

# docstring_auditor

**File**: `src\maintenance\docstring_auditor.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 4 imports  
**Lines**: 78  
**Complexity**: 3 (simple)

## Overview

Docstring auditor utilities.

Parses the analyzer output (e.g., docs/prompt/prompt4.txt) and extracts a list
of Python modules flagged with missing module-level docstrings. Provides a
helper to generate a small next-batch file listing modules to address.

## Functions (3)

### `parse_prompt_file(prompt_path)`

Parse analyzer output and return file paths with missing docstring markers.

Args:
    prompt_path: Path to the analyzer output file (plain text).

Returns:
    List of relative file paths (POSIX-style) like "src/core/lazy_loader.py".

### `file_path_to_module_name(path)`

Convert a filesystem path to a module import path.

Example: "src/core/lazy_loader.py" -> "src.core.lazy_loader"

### `generate_next_batch(prompt_path, out_path, max_entries)`

Generate the next small batch of modules to fix.

Writes a newline-separated list of module names to `out_path` and returns
the list. Modules are chosen in the order they appear in the prompt.

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `pathlib.Path`
- `re`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/maintenance/docstring_auditor.improvements.md

# Improvements for docstring_auditor

**File**: `src\maintenance\docstring_auditor.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 78 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `docstring_auditor_test.py` with pytest tests

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


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

"""Docstring auditor utilities.

Parses the analyzer output (e.g., docs/prompt/prompt4.txt) and extracts a list
of Python modules flagged with missing module-level docstrings. Provides a
helper to generate a small next-batch file listing modules to address.
"""
import re
from pathlib import Path
from typing import List

MISSING_DOCSTRING_MARKER = "Missing Docstring: Module-level docstring is missing"


def parse_prompt_file(prompt_path: str | Path) -> List[str]:
    """
    """
