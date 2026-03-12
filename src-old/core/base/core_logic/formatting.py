# Copyright 2026 PyAgent Authors
"""
LLM_CONTEXT_START

## Source: src-old/core/base/core_logic/formatting.description.md

# formatting

**File**: `src\core\base\core_logic\formatting.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 39  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for formatting.

## Classes (1)

### `FormattingCore`

Class FormattingCore implementation.

**Methods** (3):
- `fix_markdown(self, content)`
- `normalize_response(self, response)`
- `calculate_diff(self, old_content, new_content, filename)`

## Dependencies

**Imports** (4):
- `difflib`
- `re`
- `rust_core`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/base/core_logic/formatting.improvements.md

# Improvements for formatting

**File**: `src\core\base\core_logic\formatting.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 39 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: FormattingCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `formatting_test.py` with pytest tests

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

import re
import difflib
from typing import List

try:
    import rust_core as rc
except ImportError:
    rc = None


class FormattingCore:
    def fix_markdown(self, content: str) -> str:
        """Pure logic to normalize markdown content."""
        lines = content.splitlines()
        fixed_lines = []
        for line in lines:
            if line.startswith("#") and not line.startswith("# "):
                line = re.sub(r"^(#+)", r"\1 ", line)
            fixed_lines.append(line)
        return "\n".join(fixed_lines)

    def normalize_response(self, response: str) -> str:
        """Normalize response text for consistency."""
        if rc:
            try:
                return rc.normalize_response(response)
            except Exception:
                pass
        normalized = response.strip().replace("\r\n", "\n")
        return " ".join(normalized.split())

    def calculate_diff(self, old_content: str, new_content: str, filename: str) -> str:
        """Logic for generating a unified diff."""
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        diff_lines = list(
            difflib.unified_diff(
                old_lines, new_lines, fromfile=f"a/{filename}", tofile=f"b/{filename}"
            )
        )
        return "".join(diff_lines)
