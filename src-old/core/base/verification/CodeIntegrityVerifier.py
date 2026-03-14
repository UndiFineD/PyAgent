# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

r"""LLM_CONTEXT_START

## Source: src-old/core/base/verification/CodeIntegrityVerifier.description.md

# CodeIntegrityVerifier

**File**: `src\\core\base\verification\\CodeIntegrityVerifier.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 81  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for CodeIntegrityVerifier.

## Classes (1)

### `CodeIntegrityVerifier`

Phase 316: Scans codebase for structural integrity issues, specifically import paths.

**Methods** (2):
- `verify_imports(root_dir)`
- `get_symbol_map(self, root_dir)`

## Dependencies

**Imports** (2):
- `ast`
- `pathlib.Path`

---
*Auto-generated documentation*
## Source: src-old/core/base/verification/CodeIntegrityVerifier.improvements.md

# Improvements for CodeIntegrityVerifier

**File**: `src\\core\base\verification\\CodeIntegrityVerifier.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 81 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CodeIntegrityVerifier_test.py` with pytest tests

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

import ast
from pathlib import Path


class CodeIntegrityVerifier:
    """Phase 316: Scans codebase for structural integrity issues, specifically import paths."""

    @staticmethod
    def verify_imports(root_dir: str = "src") -> dict[str, list[str]]:
        """Scans all Python files in the given directory for broken internal imports.
        Specifically looks for 'from src.xxx' or 'import src.xxx' and verifies existence.
        """
        root_path = Path(root_dir)
        if not root_path.exists():
            return {"errors": [f"Directory {root_dir} not found"]}

        report = {"broken_imports": [], "syntax_errors": []}

        # Get all python files in the workspace (relative to project root)
        # assuming the script is run from project root.
        py_files = list(root_path.rglob("*.py"))

        for file_path in py_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
            except Exception as e:
                report["syntax_errors"].append(f"{file_path}: {e}")
                continue

            for node in ast.walk(tree):
                targets = []
                if isinstance(node, ast.Import):
                    targets = [n.name for n in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    # For 'from x import y', we only check the module 'x'
                    if node.level == 0:
                        targets = [node.module]

                for target in targets:
                    # We only care about verifying our own 'src' hierarchy
                    if target.startswith("src.") or target == "src":
                        parts = target.split(".")
                        # Check if it's a directory (module) or a file (.py)
                        # We use Path(".") as base to refer to project root
                        target_path = Path(".").joinpath(*parts)

                        exists = (
                            target_path.with_suffix(".py").exists()
                            or target_path.joinpath("__init__.py").exists()
                        )

                        if not exists:
                            report["broken_imports"].append(
                                f"{file_path}: Broken import '{target}'"
                            )

        return report

    def get_symbol_map(self, root_dir: Path) -> dict[str, str]:
        """Maps all class names in the directory to their relative file paths (indexing).
        """
        mapping = {}
        for py_file in root_dir.rglob("*.py"):
            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
                classes = [
                    node.name
                    for node in ast.walk(tree)
                    if isinstance(node, ast.ClassDef)
                ]
                rel_path = str(py_file.relative_to(root_dir.parent)).replace("\\", "/")
                for cls in classes:
                    mapping[cls] = rel_path
            except Exception:
                continue
        return mapping
