"""LLM_CONTEXT_START

## Source: src-old/observability/reports/core/DeduplicationCore.description.md

# DeduplicationCore

**File**: `src\\observability\reports\\core\\DeduplicationCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 53  
**Complexity**: 3 (simple)

## Overview

Core logic for Report Deduplication (Phase 183).
Handles similarity calculations and JSONL export.

## Classes (1)

### `DeduplicationCore`

Class DeduplicationCore implementation.

**Methods** (3):
- `jaccard_similarity(s1, s2)`
- `deduplicate_items(items, key, threshold)`
- `export_to_jsonl(items, output_path)`

## Dependencies

**Imports** (4):
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/observability/reports/core/DeduplicationCore.improvements.md

# Improvements for DeduplicationCore

**File**: `src\\observability\reports\\core\\DeduplicationCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 53 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: DeduplicationCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `DeduplicationCore_test.py` with pytest tests

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
Core logic for Report Deduplication (Phase 183).
Handles similarity calculations and JSONL export.
"""

import json
from typing import Any


class DeduplicationCore:
    @staticmethod
    def jaccard_similarity(s1: str, s2: str) -> float:
        """Calculates Jaccard similarity between two strings based on words.
        """
        set1 = set(s1.lower().split())
        set2 = set(s2.lower().split())
        if not set1 or not set2:
            return 0.0
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)

    @staticmethod
    def deduplicate_items(
        items: list[dict[str, Any]], key: str = "message", threshold: float = 0.8
    ) -> list[dict[str, Any]]:
        """Removes items that are too similar to already seen items.
        """
        unique_items = []
        seen_messages: list[str] = []

        for item in items:
            msg = item.get(key, "")
            is_duplicate = False
            for seen in seen_messages:
                if DeduplicationCore.jaccard_similarity(msg, seen) > threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_items.append(item)
                seen_messages.append(msg)

        return unique_items

    @staticmethod
    def export_to_jsonl(items: list[dict[str, Any]], output_path: str) -> None:
        """Exports a list of dicts to a JSONL file.
        """
        with open(output_path, "w", encoding="utf-8") as f:
            for item in items:
                f.write(json.dumps(item) + "\n")
