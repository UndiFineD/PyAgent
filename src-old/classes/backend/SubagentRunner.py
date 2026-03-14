#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/backend/SubagentRunner.description.md

# SubagentRunner

**File**: `src\\classes\backend\\SubagentRunner.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 366  
**Complexity**: 18 (moderate)

## Overview

Implementation of subagent running logic.

## Classes (1)

### `SubagentRunner`

Handles running subagents with multiple backend support and fallback logic.

**Methods** (18):
- `_resolve_repo_root()`
- `_command_available(command)`
- `__init__(self)`
- `clear_response_cache(self)`
- `get_metrics(self)`
- `reset_metrics(self)`
- `_get_cache_key(self, prompt, model)`
- `validate_response_content(self, response, content_types)`
- `estimate_tokens(self, text)`
- `estimate_cost(self, tokens, model, rate_per_1k_input)`
- ... and 8 more methods

## Dependencies

**Imports** (18):
- `DiskCache.DiskCache`
- `LLMClient.LLMClient`
- `LocalContextRecorder.LocalContextRecorder`
- `RunnerBackends.BackendHandlers`
- `__future__.annotations`
- `hashlib`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `requests`
- `subprocess`
- `time`
- `typing.Any`
- `typing.Dict`
- ... and 3 more

---
*Auto-generated documentation*
## Source: src-old/classes/backend/SubagentRunner.improvements.md

# Improvements for SubagentRunner

**File**: `src\\classes\backend\\SubagentRunner.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 366 lines (medium)  
**Complexity**: 18 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SubagentRunner_test.py` with pytest tests

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


r"""Implementation of subagent running logic."""
