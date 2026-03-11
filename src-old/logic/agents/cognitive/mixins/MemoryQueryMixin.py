"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/mixins/MemoryQueryMixin.description.md

# MemoryQueryMixin

**File**: `src\\logic\agents\\cognitive\\mixins\\MemoryQueryMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 66  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for MemoryQueryMixin.

## Classes (1)

### `MemoryQueryMixin`

Mixin for hierarchical memory querying in HierarchicalMemoryAgent.

**Methods** (1):
- `hierarchical_query(self, query, deep_search)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `json`
- `rust_core.search_with_tags_rust`
- `src.core.base.BaseUtilities.as_tool`
- `src.logic.agents.cognitive.HierarchicalMemoryAgent.HierarchicalMemoryAgent`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/mixins/MemoryQueryMixin.improvements.md

# Improvements for MemoryQueryMixin

**File**: `src\\logic\agents\\cognitive\\mixins\\MemoryQueryMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 66 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MemoryQueryMixin_test.py` with pytest tests

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
import json

from src.core.base.BaseUtilities import as_tool
from src.logic.agents.cognitive.HierarchicalMemoryAgent import HierarchicalMemoryAgent


class MemoryQueryMixin:
    """Mixin for hierarchical memory querying in HierarchicalMemoryAgent."""

    @as_tool
    def hierarchical_query(
        self: HierarchicalMemoryAgent, query: str, deep_search: bool = False
    ) -> str:
        """Searches across memory tiers starting from short-term."""
        search_tiers = ["short", "mid"]
        if deep_search:
            search_tiers += ["long", "archival"]

        # Collect all memory files
        all_data = []  # (tier, content, tags)
        for tier in search_tiers:
            tier_dir = self.memory_root / tier
            for mem_file in tier_dir.glob("*.json"):
                try:
                    with open(mem_file) as f:
                        data = json.load(f)
                    all_data.append(
                        (tier, data.get("content", ""), data.get("tags", []))
                    )
                except Exception:
                    continue

        if not all_data:
            return "No matching memories found."

        # Rust-accelerated search
        try:
            from rust_core import search_with_tags_rust

            contents = [d[1] for d in all_data]
            tags_list = [d[2] for d in all_data]
            matches = search_with_tags_rust(query, contents, tags_list)

            results = []
            for idx, score in matches:
                tier, content, _ = all_data[idx]
                results.append(f"[{tier.upper()}] {content[:100]}...")

            if not results:
                return "No matching memories found."
            return "### Memory Search Results\\n\\n" + "\\n".join(results)
        except (ImportError, Exception):
            pass  # Fall back to Python

        # Python fallback
        results = []
        for tier, content, tags in all_data:
            if query.lower() in content.lower() or any(
                query.lower() in t.lower() for t in tags
            ):
                results.append(f"[{tier.upper()}] {content[:100]}...")

        if not results:
            return "No matching memories found."

        return "### Memory Search Results\\n\\n" + "\\n".join(results)
