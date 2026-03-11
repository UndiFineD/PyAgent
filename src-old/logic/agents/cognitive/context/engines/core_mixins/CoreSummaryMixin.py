# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/core_mixins/CoreSummaryMixin.description.md

# CoreSummaryMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\core_mixins\\CoreSummaryMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 1 imports  
**Lines**: 41  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for CoreSummaryMixin.

## Classes (1)

### `CoreSummaryMixin`

Methods for summary generation and pruning.

**Methods** (2):
- `prune_lessons(self, lessons, max_lessons)`
- `generate_markdown_summary(self, memory)`

## Dependencies

**Imports** (1):
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/core_mixins/CoreSummaryMixin.improvements.md

# Improvements for CoreSummaryMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\core_mixins\\CoreSummaryMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 41 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CoreSummaryMixin_test.py` with pytest tests

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

from typing import Any


class CoreSummaryMixin:
    """Methods for summary generation and pruning."""

    def prune_lessons(
        self, lessons: list[dict[str, Any]], max_lessons: int = 20
    ) -> list[dict[str, Any]]:
        """Prunes lessons to keep only the most recent."""
        return lessons[-max_lessons:]

    def generate_markdown_summary(self, memory: dict[str, Any]) -> str:
        """Logic for formatting the cognitive summary."""
        summary = ["# 🧠 Long-Term Memory Summary"]

        if memory.get("facts"):
            summary.append("\n## 📋 Project Facts")
            for k, v in memory["facts"].items():
                summary.append(f"- **{k}**: {v['value']}")

        if memory.get("constraints"):
            summary.append("\n## ⚠️ Constraints")
            for c in memory["constraints"]:
                summary.append(f"- {c}")

        if memory.get("insights"):
            summary.append("\n## 💡 Key Insights")
            for i in memory["insights"][-5:]:  # Show last 5
                summary.append(f"- {i['text']} (via {i['source']})")

        if memory.get("lessons_learned"):
            summary.append("\n## 🎓 Lessons Learned")
            for lesson in memory["lessons_learned"][-3:]:
                summary.append(
                    f"- **Issue**: {lesson['failure']} | **Fix**: {lesson['correction']}"
                )

        return "\n".join(summary)
