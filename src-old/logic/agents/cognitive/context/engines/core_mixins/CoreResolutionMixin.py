# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/core_mixins/CoreResolutionMixin.description.md

# CoreResolutionMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\core_mixins\\CoreResolutionMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 58  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for CoreResolutionMixin.

## Classes (1)

### `CoreResolutionMixin`

Methods for conflict resolution and fact preparation.

**Methods** (4):
- `prepare_fact(self, key, value)`
- `prepare_insight(self, insight, source_agent)`
- `merge_entity_info(self, existing, new_attributes)`
- `resolve_conflict(self, existing, incoming, strategy)`

## Dependencies

**Imports** (2):
- `datetime.datetime`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/core_mixins/CoreResolutionMixin.improvements.md

# Improvements for CoreResolutionMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\core_mixins\\CoreResolutionMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 58 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CoreResolutionMixin_test.py` with pytest tests

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

from datetime import datetime
from typing import Any


class CoreResolutionMixin:
    """Methods for conflict resolution and fact preparation."""

    def prepare_fact(self, key: str, value: Any) -> dict[str, Any]:
        """Prepares a fact entry with timestamp."""
        return {"value": value, "updated_at": datetime.now().isoformat()}

    def prepare_insight(self, insight: str, source_agent: str) -> dict[str, Any]:
        """Prepares an insight entry."""
        return {
            "text": insight,
            "source": source_agent,
            "timestamp": datetime.now().isoformat(),
        }

    def merge_entity_info(
        self, existing: dict[str, Any], new_attributes: dict[str, Any]
    ) -> dict[str, Any]:
        """Merges new attributes into an entity record."""
        updated = existing.copy()
        updated.update(new_attributes)
        updated["last_modified"] = datetime.now().isoformat()
        return updated

    def resolve_conflict(
        self, existing: Any, incoming: Any, strategy: str = "latest"
    ) -> Any:
        """Logic to resolve conflicts when multiple agents update the same key."""
        if strategy == "latest":
            if isinstance(existing, dict) and isinstance(incoming, dict):
                e_ts = existing.get("updated_at", "")
                i_ts = incoming.get("updated_at", "")
                return incoming if i_ts >= e_ts else existing
            return incoming

        if strategy == "merge":
            if isinstance(existing, dict) and isinstance(incoming, dict):
                merged = existing.copy()
                merged.update(incoming)
                return merged
            if isinstance(existing, list) and isinstance(incoming, list):
                return list(set(existing + incoming))
            return incoming

        if strategy == "accumulate":
            if isinstance(existing, (int, float)) and isinstance(
                incoming, (int, float)
            ):
                return existing + incoming
            return incoming

        return incoming
