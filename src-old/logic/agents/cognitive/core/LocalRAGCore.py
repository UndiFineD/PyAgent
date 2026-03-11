"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/core/LocalRAGCore.description.md

# LocalRAGCore

**File**: `src\\logic\agents\\cognitive\\core\\LocalRAGCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 3 imports  
**Lines**: 45  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for LocalRAGCore.

## Classes (2)

### `RAGShard`

Metadata for a localized vector shard.

### `LocalRAGCore`

Pure logic for hyper-localized RAG and vector sharding.
Handles shard selection, path-based routing, and context relevance.

**Methods** (3):
- `route_query_to_shards(self, query, query_path, available_shards)`
- `calculate_rerank_score(self, original_score, path_proximity)`
- `extract_local_context_markers(self, content)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `dataclasses.dataclass`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/core/LocalRAGCore.improvements.md

# Improvements for LocalRAGCore

**File**: `src\\logic\agents\\cognitive\\core\\LocalRAGCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 45 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `LocalRAGCore_test.py` with pytest tests

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

from dataclasses import dataclass


@dataclass(frozen=True)
class RAGShard:
    """Metadata for a localized vector shard."""

    path: str
    tags: list[str]
    document_count: int
    last_updated: float


class LocalRAGCore:
    """Pure logic for hyper-localized RAG and vector sharding.
    Handles shard selection, path-based routing, and context relevance.
    """

    def route_query_to_shards(
        self, query: str, query_path: str, available_shards: list[RAGShard]
    ) -> list[str]:
        """Routes a query to the most relevant localized shards based on file path."""
        # Preference: direct path match > parent path match > tag match
        selected = []
        for shard in available_shards:
            if query_path.startswith(shard.path):
                selected.append(shard.path)
            elif any(tag in query.lower() for tag in shard.tags):
                selected.append(shard.path)

        return selected

    def calculate_rerank_score(
        self, original_score: float, path_proximity: int
    ) -> float:
        """Boosts relevance score based on how close the source is to the active file."""
        # path_proximity = depth difference between query_path and shard_path
        boost = 1.0 / (1.0 + path_proximity)
        return original_score * (1.0 + boost)

    def extract_local_context_markers(self, content: str) -> list[str]:
        """Identifies key symbols/imports to use as local context anchors."""
        markers = []
        if "import" in content:
            # Simple heuristic for anchors
            for line in content.splitlines()[:10]:
                if "import" in line:
                    markers.append(line.split()[-1])
        return list(set(markers))
