#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/base_agent/ConnectivityManager.description.md

# ConnectivityManager

**File**: `src\\classes\base_agent\\ConnectivityManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 107  
**Complexity**: 11 (moderate)

## Overview

Centralized connectivity management with TTL-based status caching.

## Classes (1)

### `ConnectivityManager`

Manages connection status for external APIs with persistent 15-minute TTL caching.

**Methods** (11):
- `__new__(cls)`
- `__init__(self, workspace_root)`
- `_load_status(self)`
- `_save_status(self)`
- `get_preferred_endpoint(self, group)`
- `set_preferred_endpoint(self, group, endpoint_id)`
- `is_endpoint_available(self, endpoint_id)`
- `update_status(self, endpoint_id, working)`
- `is_online(self, endpoint)`
- `set_status(self, endpoint, online)`
- ... and 1 more methods

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/base_agent/ConnectivityManager.improvements.md

# Improvements for ConnectivityManager

**File**: `src\\classes\base_agent\\ConnectivityManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 107 lines (medium)  
**Complexity**: 11 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConnectivityManager_test.py` with pytest tests

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
from __future__ import annotations


r"""Centralized connectivity management with TTL-based status caching."""
