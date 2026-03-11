#!/usr/bin/env python3

"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/VersionGate.description.md

# VersionGate

**File**: `src\\classes\fleet\\VersionGate.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 55  
**Complexity**: 2 (simple)

## Overview

Unified Version Gatekeeper for PyAgent Fleet.
Handles semantic versioning checks and capability validation.

## Classes (1)

### `VersionGate`

Pure logic for version compatibility checks.
Designed for future Rust porting (Core/Shell pattern).

**Methods** (2):
- `is_compatible(current, required)`
- `filter_by_capability(available, required)`

## Dependencies

**Imports** (3):
- `logging`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/VersionGate.improvements.md

# Improvements for VersionGate

**File**: `src\\classes\fleet\\VersionGate.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 55 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `VersionGate_test.py` with pytest tests

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
Unified Version Gatekeeper for PyAgent Fleet.
Handles semantic versioning checks and capability validation.
"""

import logging
from typing import List


class VersionGate:
    """Pure logic for version compatibility checks.
    Designed for future Rust porting (Core/Shell pattern).
    """

    @staticmethod
    def is_compatible(current: str, required: str) -> bool:
        """Checks if the current version meets the requirement using semantic logic.
        Major version must match or current must be higher (if backward compatible).
        """
        try:
            curr_parts = [int(x) for x in current.split(".")]
            req_parts = [int(x) for x in required.split(".")]

            # Pad to 3 parts (major, minor, patch)
            curr_parts += [0] * (3 - len(curr_parts))
            req_parts += [0] * (3 - len(req_parts))

            # Major check: Breaking changes occur on major version bumps
            if curr_parts[0] > req_parts[0]:
                # In this ecosystem, newer majors are generally backward compatible
                # unless explicitly flagged otherwise.
                return True
            if curr_parts[0] < req_parts[0]:
                return False

            # Minor check: Feature match
            if curr_parts[1] > req_parts[1]:
                return True
            if curr_parts[1] < req_parts[1]:
                return False

            # Patch check
            return curr_parts[2] >= req_parts[2]
        except Exception as e:
            logging.debug(
                f"VersionGate: Failed to parse version '{current}' or '{required}': {e}"
            )
            # Fail safe: if we can't parse, assume it's legacy (compatible)
            return True

    @staticmethod
    def filter_by_capability(available: List[str], required: List[str]) -> List[str]:
        """Filters a list of providers by required capabilities."""
        return [p for p in available if all(cap in p for cap in required)]
