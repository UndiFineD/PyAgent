"""LLM_CONTEXT_START

## Source: src-old/logic/agents/system/core/EntropyCore.description.md

# EntropyCore

**File**: `src\\logic\agents\\system\\core\\EntropyCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 67  
**Complexity**: 3 (simple)

## Overview

Core logic for Entropy Measurement (Phase 172).
Calculates structural complexity metrics.

## Classes (1)

### `EntropyCore`

Class EntropyCore implementation.

**Methods** (3):
- `calculate_cyclomatic_complexity(code)`
- `get_file_metrics(file_path)`
- `scan_directory_metrics(directory)`

## Dependencies

**Imports** (2):
- `ast`
- `os`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/core/EntropyCore.improvements.md

# Improvements for EntropyCore

**File**: `src\\logic\agents\\system\\core\\EntropyCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 67 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: EntropyCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `EntropyCore_test.py` with pytest tests

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

"""
Core logic for Entropy Measurement (Phase 172).
Calculates structural complexity metrics.
"""

import ast
import os


class EntropyCore:
    @staticmethod
    def calculate_cyclomatic_complexity(code: str) -> int:
        """Estimates cyclomatic complexity based on AST nodes.
        CC = E - N + 2P (approximate using decision points)
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 0

        complexity = 1
        for node in ast.walk(tree):
            if isinstance(
                node, (ast.If, ast.While, ast.For, ast.And, ast.Or, ast.ExceptHandler)
            ):
                complexity += 1
        return complexity

    @staticmethod
    def get_file_metrics(file_path: str) -> dict:
        """Returns size and estimated complexity for a single file.
        """
        if not os.path.exists(file_path):
            return {}

        with open(file_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        return {
            "size_bytes": len(content),
            "lines": len(content.splitlines()),
            "complexity": EntropyCore.calculate_cyclomatic_complexity(content),
        }

    @staticmethod
    def scan_directory_metrics(directory: str) -> dict:
        """Scans a directory and returns aggregate metrics.
        """
        all_metrics = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    metrics = EntropyCore.get_file_metrics(os.path.join(root, file))
                    if metrics:
                        all_metrics.append(metrics)

        if not all_metrics:
            return {}

        count = len(all_metrics)
        return {
            "avg_size": sum(m["size_bytes"] for m in all_metrics) / count,
            "avg_complexity": sum(m["complexity"] for m in all_metrics) / count,
            "max_complexity": max(m["complexity"] for m in all_metrics),
            "file_count": count,
        }
