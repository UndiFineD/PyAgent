# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/knowledge_mixins/KnowledgeProcessMixin.description.md

# KnowledgeProcessMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\knowledge_mixins\\KnowledgeProcessMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 1 imports  
**Lines**: 38  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for KnowledgeProcessMixin.

## Classes (1)

### `KnowledgeProcessMixin`

Methods for processing file content and computing similarity.

**Methods** (2):
- `process_file_content(self, rel_path, content, extension)`
- `compute_similarity(self, text_a, text_b)`

## Dependencies

**Imports** (1):
- `re`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/knowledge_mixins/KnowledgeProcessMixin.improvements.md

# Improvements for KnowledgeProcessMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\knowledge_mixins\\KnowledgeProcessMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 38 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `KnowledgeProcessMixin_test.py` with pytest tests

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


class KnowledgeProcessMixin:
    """Methods for processing file content and computing similarity."""

    def process_file_content(
        self, rel_path: str, content: str, extension: str
    ) -> list[tuple[str, str, str, str]]:
        """Parses content and returns a list of (symbol, path, category, snippet) tuples.
        """
        results: list[tuple[str, str, str, str]] = []

        if extension == ".py":
            symbols = self.extract_python_symbols(content)
            for s in symbols:
                results.append((s, rel_path, "python_symbol", content[:500]))
        elif extension == ".md":
            links = self.extract_markdown_backlinks(content)
            for link in links:
                results.append(
                    (f"link:{link}", rel_path, "markdown_link", content[:500])
                )

        return results

    def compute_similarity(self, text_a: str, text_b: str) -> float:
        """Computes basic string similarity (Jaccard) for symbol matching."""
        set_a = set(re.findall(r"\w+", text_a.lower()))
        set_b = set(re.findall(r"\w+", text_b.lower()))
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return float(intersection) / union
