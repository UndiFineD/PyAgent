# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/knowledge_mixins/KnowledgeSymbolMixin.description.md

# KnowledgeSymbolMixin

**File**: `src\logic\agents\cognitive\context\engines\knowledge_mixins\KnowledgeSymbolMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 57  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for KnowledgeSymbolMixin.

## Classes (1)

### `KnowledgeSymbolMixin`

Methods for symbol extraction from various formats.

**Methods** (4):
- `extract_symbols(self, content, pattern)`
- `extract_python_symbols(self, content)`
- `extract_markdown_backlinks(self, content)`
- `build_symbol_map(self, directory, patterns)`

## Dependencies

**Imports** (4):
- `pathlib.Path`
- `re`
- `rust_core`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/knowledge_mixins/KnowledgeSymbolMixin.improvements.md

# Improvements for KnowledgeSymbolMixin

**File**: `src\logic\agents\cognitive\context\engines\knowledge_mixins\KnowledgeSymbolMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 57 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `KnowledgeSymbolMixin_test.py` with pytest tests

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
from typing import Any
from pathlib import Path

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class KnowledgeSymbolMixin:
    """Methods for symbol extraction from various formats."""

    def extract_symbols(self, content: str, pattern: str) -> list[str]:
        """Generic symbol extractor using optimized regex."""
        if not content:
            return []
        return re.findall(pattern, content)

    def extract_python_symbols(self, content: str) -> list[str]:
        """Extracts class and function names from Python content."""
        if HAS_RUST:
            try:
                return rust_core.extract_python_symbols(content)  # type: ignore[attr-defined]
            except Exception:
                pass
        return self.extract_symbols(
            content, r"(?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)"
        )

    def extract_markdown_backlinks(self, content: str) -> list[str]:
        """Extracts [[WikiStyle]] backlinks from markdown content."""
        if HAS_RUST:
            try:
                return rust_core.extract_markdown_backlinks(content)  # type: ignore[attr-defined]
            except Exception:
                pass
        return self.extract_symbols(content, r"\[\[(.*?)\]\]")

    def build_symbol_map(
        self, directory: Any, patterns: dict[str, str]
    ) -> dict[str, list[str]]:
        """Scans a directory for symbols according to provided patterns."""
        symbol_map: dict[str, list[str]] = {}
        dir_path = Path(directory)
        for ext, pattern in patterns.items():
            # Use non-recursive glob to avoid scanning the whole repo in tests
            for file_path in dir_path.glob(f"*{ext}"):
                try:
                    content = file_path.read_text(encoding="utf-8")
                    symbols = self.extract_symbols(content, pattern)
                    if symbols:
                        symbol_map[file_path.name] = symbols
                except Exception:
                    continue
        return symbol_map
