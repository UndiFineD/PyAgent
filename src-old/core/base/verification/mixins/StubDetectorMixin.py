# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
LLM_CONTEXT_START

## Source: src-old/core/base/verification/mixins/StubDetectorMixin.description.md

# StubDetectorMixin

**File**: `src\core\base\verification\mixins\StubDetectorMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 73  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for StubDetectorMixin.

## Classes (1)

### `StubDetectorMixin`

Methods for detecting stub nodes in the AST.

**Methods** (1):
- `_is_stub_node(node)`

## Dependencies

**Imports** (2):
- `StubDetectorMixin.StubDetectorMixin`
- `ast`

---
*Auto-generated documentation*
## Source: src-old/core/base/verification/mixins/StubDetectorMixin.improvements.md

# Improvements for StubDetectorMixin

**File**: `src\core\base\verification\mixins\StubDetectorMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 73 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `StubDetectorMixin_test.py` with pytest tests

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

import ast

class StubDetectorMixin:
    """Methods for detecting stub nodes in the AST."""

    @staticmethod
    def _is_stub_node(node: ast.AST) -> bool | str:
        """Determines if a node is an empty stub (pass/NotImplementedError)."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = [
                s
                for s in node.body
                if not (
                    isinstance(s, ast.Expr)
                    and isinstance(s.value, ast.Constant)
                    and isinstance(s.value.value, str)
                )
            ]
            if not body:
                return True
            if len(body) > 1:
                return False
            stmt = body[0]
            if isinstance(stmt, ast.Pass):
                return True
            if (
                isinstance(stmt, ast.Expr)
                and isinstance(stmt.value, ast.Constant)
                and stmt.value.value is Ellipsis
            ):
                return True
            if isinstance(stmt, ast.Raise):
                exc_name = ""
                if isinstance(stmt.exc, ast.Call) and isinstance(
                    stmt.exc.func, ast.Name
                ):
                    exc_name = stmt.exc.func.id
                elif isinstance(stmt.exc, ast.Name):
                    exc_name = stmt.exc.id
                if exc_name == "NotImplementedError":
                    return True
            return False

        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id in ("ABC", "Protocol"):
                    return "IS_ABC"
            body = [
                s
                for s in node.body
                if not (
                    isinstance(s, ast.Expr)
                    and isinstance(s.value, ast.Constant)
                    and isinstance(s.value.value, str)
                )
            ]
            if not body:
                return True
            for item in body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    from .StubDetectorMixin import StubDetectorMixin
                    res = StubDetectorMixin._is_stub_node(item)
                    if res is False:
                        return False
                    if res == "IS_ABC":
                        return "IS_ABC"
                elif not isinstance(item, ast.Pass):
                    return False
            return True
        return True
