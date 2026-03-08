#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/ChangelogAnalyticsMixin.description.md

# ChangelogAnalyticsMixin

**File**: `src\logic\agents\swarm\ChangelogAnalyticsMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 45  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for ChangelogAnalyticsMixin.

## Classes (1)

### `ChangelogAnalyticsMixin`

Mixin for calculating statistics and analytics for changelogs.

**Methods** (1):
- `calculate_statistics(self)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `re`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/ChangelogAnalyticsMixin.improvements.md

# Improvements for ChangelogAnalyticsMixin

**File**: `src\logic\agents\swarm\ChangelogAnalyticsMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 45 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ChangelogAnalyticsMixin_test.py` with pytest tests

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

import re
from typing import Any


class ChangelogAnalyticsMixin:
    """Mixin for calculating statistics and analytics for changelogs."""

    def calculate_statistics(self) -> dict[str, Any]:
        """Calculate statistics for the changelog."""
        content = getattr(self, "current_content", "") or getattr(
            self, "previous_content", ""
        )
        if not content:
            return {}

        # Count versions
        version_pattern = r"##\s*\[?(\d+\.\d+\.\d+|\d{4}\.\d{2}\.\d{2})\]?"
        versions = re.findall(version_pattern, content)

        # Count entries per category
        categories: dict[str, int] = {}
        for section in [
            "Added",
            "Changed",
            "Deprecated",
            "Removed",
            "Fixed",
            "Security",
        ]:
            pattern = rf"###\s*{section}\s*\n(.*?)(?=###|\Z)"
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                entries = [
                    line
                    for line in matches[0].split("\n")
                    if line.strip().startswith("-")
                ]
                categories[section] = len(entries)

        # Count contributors
        contributor_pattern = r"@(\w+)"
        contributors = set(re.findall(contributor_pattern, content))

        stats = {
            "version_count": len(versions),
            "latest_version": versions[0] if versions else None,
            "entries_by_category": categories,
            "total_entries": sum(categories.values()) if categories else 0,
            "contributor_count": len(contributors),
            "contributors": list(contributors),
            "line_count": len(content.split("\n")),
            "character_count": len(content),
        }
        setattr(self, "_statistics", stats)
        return stats
