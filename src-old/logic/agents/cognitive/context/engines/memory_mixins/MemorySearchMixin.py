# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/memory_mixins/MemorySearchMixin.description.md

# MemorySearchMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\memory_mixins\\MemorySearchMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 99  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for MemorySearchMixin.

## Classes (1)

### `MemorySearchMixin`

Methods for searching memories.

**Methods** (2):
- `get_lessons_learned(self, query, limit, min_utility)`
- `search_memories(self, query, limit)`

## Dependencies

**Imports** (2):
- `logging`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/memory_mixins/MemorySearchMixin.improvements.md

# Improvements for MemorySearchMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\memory_mixins\\MemorySearchMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 99 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MemorySearchMixin_test.py` with pytest tests

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

import logging
from typing import Any


class MemorySearchMixin:
    """Methods for searching memories."""

    def get_lessons_learned(
        self, query: str = "", limit: int = 5, min_utility: float = 0.0
    ) -> list[dict[str, Any]]:
        """Retrieves past episodes relevant to the query, filtered by high utility."""
        if not query:
            # Return recent high utility episodes
            candidates = [
                ep
                for ep in self.episodes
                if ep.get("utility_score", 0.5) >= min_utility
            ]
            return candidates[-limit:]

        collection = self._init_db()
        if collection:
            try:
                # Build specific filter for utility if Chroma version supports it
                where_clause = (
                    {"utility_score": {"$gte": min_utility}}
                    if min_utility > 0
                    else None
                )
                results = collection.query(
                    query_texts=[query], n_results=limit, where=where_clause
                )

                semantic_results = []
                for i, doc in enumerate(results.get("documents", [[]])[0]):
                    meta = results["metadatas"][0][i]
                    semantic_results.append(
                        {
                            "task": "Semantic Memory",
                            "outcome": doc,
                            "success": meta.get("success") == "True",
                            "agent": meta.get("agent", "Self"),
                            "utility_score": meta.get("utility_score", 0.5),
                        }
                    )
                return semantic_results
            except Exception as e:
                logging.error(f"Memory search error: {e}")

        # Fallback to simple keyword matching
        relevant = []
        q = query.lower()
        for ep in reversed(self.episodes):
            if (
                q in ep["task"].lower()
                or q in ep["outcome"].lower()
                or q in ep["agent"].lower()
            ):
                relevant.append(ep)
            if len(relevant) >= limit:
                break
        return relevant

    def search_memories(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Public interface for semantic search across episodic memories."""
        collection = self._init_db()
        if not collection:
            # Fallback to simple matching if Chroma is not available
            return [
                {
                    "content": ep["outcome"],
                    "metadata": {
                        "file_path": ep.get("metadata", {}).get("file_path", "unknown"),
                        "agent": ep["agent"],
                    },
                    "score": 0.5,
                }
                for ep in self.get_lessons_learned(query, limit)
            ]

        try:
            results = collection.query(query_texts=[query], n_results=limit)
            matches = []
            for i in range(len(results.get("documents", [[]])[0])):
                matches.append(
                    {
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "score": (
                            results["distances"][0][i] if "distances" in results else 0
                        ),
                    }
                )
            return matches
        except Exception as e:
            logging.error(f"search_memories error: {e}")
            return []
