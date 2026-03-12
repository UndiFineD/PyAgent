#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/base_agent.description.md

# base_agent

**File**: `src\core\base\base_agent.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 2 imports  
**Lines**: 25  
**Complexity**: 0 (simple)

## Overview

Compatibility shim for older imports expecting `src.core.base.base_agent`.

This module re-exports the modern BaseAgent implementation located under
`src.core.base.lifecycle.base_agent` to maintain backward compatibility with
external code and tests.

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `src.core.base.lifecycle.base_agent.BaseAgent`

---
*Auto-generated documentation*
## Source: src-old/core/base/base_agent.improvements.md

# Improvements for base_agent

**File**: `src\core\base\base_agent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 25 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `base_agent_test.py` with pytest tests

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
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Compatibility shim for older imports expecting `src.core.base.base_agent`.

This module re-exports the modern BaseAgent implementation located under
`src.core.base.lifecycle.base_agent` to maintain backward compatibility with
external code and tests.
"""

from src.core.base.lifecycle.base_agent import BaseAgent  # noqa: F401

__all__ = ["BaseAgent"]
