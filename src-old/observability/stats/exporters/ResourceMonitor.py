#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/exporters/ResourceMonitor.description.md

# ResourceMonitor

**File**: `src\observability\stats\exporters\ResourceMonitor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 80  
**Complexity**: 4 (simple)

## Overview

Engine for monitoring system resources (CPU, Memory, Disk).

## Classes (1)

### `ResourceMonitor`

Monitors local system load to inform agent execution strategies.

**Methods** (4):
- `__init__(self, workspace_root)`
- `get_current_stats(self)`
- `save_stats(self)`
- `get_execution_recommendation(self)`

## Dependencies

**Imports** (9):
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `platform`
- `psutil`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/exporters/ResourceMonitor.improvements.md

# Improvements for ResourceMonitor

**File**: `src\observability\stats\exporters\ResourceMonitor.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 80 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ResourceMonitor_test.py` with pytest tests

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

r"""Engine for monitoring system resources (CPU, Memory, Disk)."""
