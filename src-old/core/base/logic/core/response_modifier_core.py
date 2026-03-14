#!/usr/bin/env python3
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

r"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/response_modifier_core.description.md

# response_modifier_core

**File**: `src\\core\base\\logic\\core\response_modifier_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 10 imports  
**Lines**: 291  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for response_modifier_core.

## Classes (3)

### `ResponseModificationRule`

Rule for modifying HTTP responses

### `ModifiedResponse`

Container for modified response data

### `ResponseModifierCore`

**Inherits from**: BaseCore

HTTP Response Modifier Core for security testing and analysis.

Provides capabilities to modify HTTP response codes and content
for testing purposes, similar to Burp Suite extensions.
Useful for bypassing client-side validations and testing error handling.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (10):
- `asyncio`
- `dataclasses.dataclass`
- `re`
- `src.core.base.logic.core.base_core.BaseCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/response_modifier_core.improvements.md

# Improvements for response_modifier_core

**File**: `src\\core\base\\logic\\core\response_modifier_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 291 lines (medium)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `response_modifier_core_test.py` with pytest tests

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
# Response Modifier Core - HTTP Response Code Manipulation
# Based on patterns from 200-OK-Modifier Burp extension

import asyncio
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from src.core.base.logic.core.base_core import BaseCore


@dataclass
class ResponseModificationRule:
    """
    """
