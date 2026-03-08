"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/mixins/AccessibilityLogicMixin.description.md

# AccessibilityLogicMixin

**File**: `src\logic\agents\development\mixins\AccessibilityLogicMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 52  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for AccessibilityLogicMixin.

## Classes (1)

### `AccessibilityLogicMixin`

Mixin for entry-point analysis logic and rule management in AccessibilityAgent.

**Methods** (4):
- `analyze_file(self, file_path)`
- `analyze_content(self, content, file_type)`
- `enable_rule(self, wcag_criterion)`
- `disable_rule(self, wcag_criterion)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.types.AccessibilityReport.AccessibilityReport`
- `src.logic.agents.development.AccessibilityAgent.AccessibilityAgent`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/mixins/AccessibilityLogicMixin.improvements.md

# Improvements for AccessibilityLogicMixin

**File**: `src\logic\agents\development\mixins\AccessibilityLogicMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 52 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AccessibilityLogicMixin_test.py` with pytest tests

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

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
from src.logic.agents.development.AccessibilityAgent import AccessibilityAgent

from typing import TYPE_CHECKING
from src.core.base.types.AccessibilityReport import AccessibilityReport
from pathlib import Path

class AccessibilityLogicMixin:
    """Mixin for entry-point analysis logic and rule management in AccessibilityAgent."""

    def analyze_file(self: AccessibilityAgent, file_path: str) -> AccessibilityReport:
        """Analyze a file for accessibility issues."""
        self.issues.clear()
        path = Path(file_path)
        if not path.exists():
            return AccessibilityReport(file_path=file_path)
        content = path.read_text(encoding="utf-8")
        # Analyze based on file type
        if path.suffix in (".html", ".htm"):
            self._analyze_html(content)
        elif path.suffix == ".py":
            self._analyze_python_ui(content)
        elif path.suffix in (".js", ".jsx", ".ts", ".tsx"):
            self._analyze_javascript_ui(content)
        return self._generate_report(file_path)

    def analyze_content(
        self: AccessibilityAgent, content: str, file_type: str = "html"
    ) -> AccessibilityReport:
        """Analyze content string for accessibility issues."""
        self.issues.clear()
        if file_type == "html":
            self._analyze_html(content)
        elif file_type == "python":
            self._analyze_python_ui(content)
        elif file_type in ("javascript", "react"):
            self._analyze_javascript_ui(content)
        return self._generate_report("content")

    def enable_rule(self: AccessibilityAgent, wcag_criterion: str) -> None:
        """Enable a specific WCAG rule."""
        if wcag_criterion in self.rules:
            self.rules[wcag_criterion] = True

    def disable_rule(self: AccessibilityAgent, wcag_criterion: str) -> None:
        """Disable a specific WCAG rule."""
        if wcag_criterion in self.rules:
            self.rules[wcag_criterion] = False
