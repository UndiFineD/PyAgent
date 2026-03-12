# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/knowledge_mixins/KnowledgeSearchMixin.description.md

# KnowledgeSearchMixin

**File**: `src\logic\agents\cognitive\context\engines\knowledge_mixins\KnowledgeSearchMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 1 imports  
**Lines**: 60  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for KnowledgeSearchMixin.

## Classes (1)

### `KnowledgeSearchMixin`

Methods for workspace search and snippet extraction.

**Methods** (2):
- `search_index(self, query, index, root)`
- `perform_fallback_scan(self, query, root, indexed_paths)`

## Dependencies

**Imports** (1):
- `pathlib.Path`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/knowledge_mixins/KnowledgeSearchMixin.improvements.md

# Improvements for KnowledgeSearchMixin

**File**: `src\logic\agents\cognitive\context\engines\knowledge_mixins\KnowledgeSearchMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 60 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `KnowledgeSearchMixin_test.py` with pytest tests

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

from pathlib import Path

class KnowledgeSearchMixin:
    """Methods for workspace search and snippet extraction."""

    def search_index(self, query: str, index: dict, root: Path) -> list[str]:
        """Extracts code snippets based on index hits."""
        snippets = []
        hits = index.get(query, [])
        for hit in hits:
            rel_path = hit["path"] if isinstance(hit, dict) else hit
            p = root / rel_path
            try:
                content = p.read_text(encoding="utf-8")
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if f"def {query}" in line or f"class {query}" in line or query in line:
                        start, end = max(0, i - 5), min(len(lines), i + 15)
                        snippet = "\n".join(lines[start:end])
                        snippets.append(
                            f"> [!CODE] File: {rel_path} (from index)\n> ```python\n"
                            + "\n".join([f"> {sl}" for sl in snippet.splitlines()])
                            + "\n> ```\n"
                        )
                        break
            except Exception:
                pass
            if len(snippets) > 5:
                break
        return snippets

    def perform_fallback_scan(self, query: str, root: Path, indexed_paths: list) -> list[str]:
        """Performs a deep grep fallback search across the workspace."""
        snippets = []
        for p in root.rglob("*.py"):
            rel_path = str(p.relative_to(root))
            if any(part in rel_path for part in ["__pycache__", "venv", ".git"]) or rel_path in indexed_paths:
                continue
            try:
                content = p.read_text(encoding="utf-8")
                if query.lower() in content.lower():
                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if query.lower() in line.lower():
                            start, end = max(0, i - 5), min(len(lines), i + 10)
                            snippet = "\n".join(lines[start:end])
                            snippets.append(
                                f"> [!CODE] File: {rel_path}\n> ```python\n"
                                + "\n".join([f"> {sl}" for sl in snippet.splitlines()])
                                + "\n> ```\n"
                            )
                            break
            except Exception:
                pass
            if len(snippets) > 5:
                break
        return snippets
