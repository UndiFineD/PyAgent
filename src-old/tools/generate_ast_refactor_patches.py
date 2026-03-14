#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/tools/generate_ast_refactor_patches.description.md

# generate_ast_refactor_patches

**File**: `src\tools\\generate_ast_refactor_patches.py`  
**Type**: Python Module  
**Summary**: 1 classes, 4 functions, 7 imports  
**Lines**: 128  
**Complexity**: 5 (moderate)

## Overview

Generate conservative AST-based refactor patch proposals for top-priority files.

This script:
- Loads the bandit report (.external/static_checks/bandit.json) or uses the prepared
  bandit_report.md to find top files by score.
- For each top file present under `src/external_candidates/auto/`, it transforms
  function-level calls to dangerous subprocess APIs into calls to a
  `safe_subprocess_run(...)` wrapper and inserts a conservative wrapper stub.
- Writes unified-diff patch files to `.external/patches_ast/` for human review.

Notes:
- This only writes patch proposals and does not modify source files.

## Classes (1)

### `SubprocessTransformer`

**Inherits from**: NodeTransformer

Class SubprocessTransformer implementation.

**Methods** (1):
- `visit_Call(self, node)`

## Functions (4)

### `load_bandit_results()`

### `top_files_from_bandit(results, top_n)`

### `create_patch_for_file(path)`

### `main()`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ast`
- `difflib`
- `json`
- `pathlib.Path`
- `re`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/tools/generate_ast_refactor_patches.improvements.md

# Improvements for generate_ast_refactor_patches

**File**: `src\tools\\generate_ast_refactor_patches.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 128 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: SubprocessTransformer

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `generate_ast_refactor_patches_test.py` with pytest tests

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


"""Generate conservative AST-based refactor patch proposals for top-priority files.

This script:
- Loads the bandit report (.external/static_checks/bandit.json) or uses the prepared
  bandit_report.md to find top files by score.
- For each top file present under `src/external_candidates/auto/`, it transforms
  function-level calls to dangerous subprocess APIs into calls to a
  `safe_subprocess_run(...)` wrapper and inserts a conservative wrapper stub.
- Writes unified-diff patch files to `.external/patches_ast/` for human review.

Notes:
- This only writes patch proposals and does not modify source files.
"""
import ast
import difflib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANDIT_JSON = ROOT / ".external" / "static_checks" / "bandit.json"
PATCH_DIR = ROOT / ".external" / "patches_ast"
TARGET_PREFIX = ROOT / "src" / "external_candidates" / "auto"


def load_bandit_results():
    if not BANDIT_JSON.exists():
        return {}
    try:
        return json.loads(BANDIT_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}


def top_files_from_bandit(results: dict, top_n: int = 30) -> list[str]:
    files = {}
    for r in results.get("results", []):
        fn = r.get("filename")
        sev = r.get("issue_severity", "LOW").upper()
        weight = {"LOW": 1, "MEDIUM": 5, "HIGH": 10}.get(sev, 1)
        files.setdefault(fn, 0)
        files[fn] += weight
    items = sorted(files.items(), key=lambda kv: kv[1], reverse=True)
    return [k for k, _ in items[:top_n]]


class SubprocessTransformer(ast.NodeTransformer):
    DANGEROUS_ATTRS = {"Popen", "call", "run", "check_output"}

    def visit_Call(self, node):
        # transform subprocess.<attr>(...) -> safe_subprocess_run(...)
        func = node.func
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            if func.value.id == "subprocess" and func.attr in self.DANGEROUS_ATTRS:
                new = ast.copy_location(
                    ast.Call(
                        func=ast.Name(id="safe_subprocess_run", ctx=ast.Load()),
                        args=node.args,
                        keywords=node.keywords,
                    ),
                    node,
                )
                return ast.fix_missing_locations(new)
        # direct Popen(...) or run(...) when imported directly
        if isinstance(func, ast.Name) and func.id in self.DANGEROUS_ATTRS:
            new = ast.copy_location(
                ast.Call(
                    func=ast.Name(id="safe_subprocess_run", ctx=ast.Load()),
                    args=node.args,
                    keywords=node.keywords,
                ),
                node,
            )
            return ast.fix_missing_locations(new)
        return self.generic_visit(node)


SAFE_WRAPPER_SRC = '''def safe_subprocess_run(*args, **kwargs):
    """
    """
    '''
