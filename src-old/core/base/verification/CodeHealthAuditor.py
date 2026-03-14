# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

r"""LLM_CONTEXT_START

## Source: src-old/core/base/verification/CodeHealthAuditor.description.md

# CodeHealthAuditor

**File**: `src\\core\base\verification\\CodeHealthAuditor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 14  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for CodeHealthAuditor.

## Classes (1)

### `CodeHealthAuditor`

**Inherits from**: WorkspaceAuditorMixin, StubDetectorMixin

Phase 316: Performs static analysis to detect technical debt and quality issues.

**Methods** (1):
- `get_code_metrics(self, content)`

## Dependencies

**Imports** (3):
- `mixins.StubDetectorMixin.StubDetectorMixin`
- `mixins.WorkspaceAuditorMixin.WorkspaceAuditorMixin`
- `src.core.rust_bridge.RustBridge`

---
*Auto-generated documentation*
## Source: src-old/core/base/verification/CodeHealthAuditor.improvements.md

# Improvements for CodeHealthAuditor

**File**: `src\\core\base\verification\\CodeHealthAuditor.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 14 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CodeHealthAuditor_test.py` with pytest tests

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

from src.core.rust_bridge import RustBridge

from .mixins.StubDetectorMixin import StubDetectorMixin
from .mixins.WorkspaceAuditorMixin import WorkspaceAuditorMixin


class CodeHealthAuditor(WorkspaceAuditorMixin, StubDetectorMixin):
    """Phase 316: Performs static analysis to detect technical debt and quality issues."""

    def get_code_metrics(self, content: str) -> dict:
        """Phase 318: Returns Rust-accelerated code metrics."""
        return RustBridge.calculate_metrics(content)
