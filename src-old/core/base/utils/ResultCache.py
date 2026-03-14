#!/usr/bin/env python3
r"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/ResultCache.description.md

# ResultCache

**File**: `src\core\base\utils\ResultCache.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 123  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `ResultCache`

Cache agent results for reuse.

Example:
    cache=ResultCache()

    # Check cache
    result=cache.get("test.py", "coder", content_hash)
    if result is None:
        result=run_coder("test.py")
        cache.set("test.py", "coder", content_hash, result)

**Methods** (6):
- `__init__(self, cache_dir)`
- `_make_key(self, file_path, agent_name, content_hash)`
- `get(self, file_path, agent_name, content_hash)`
- `set(self, file_path, agent_name, content_hash, result, ttl_seconds)`
- `invalidate(self, file_path)`
- `clear(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.models.CachedResult`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/ResultCache.improvements.md

# Improvements for ResultCache

**File**: `src\core\base\utils\ResultCache.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 123 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ResultCache_test.py` with pytest tests

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


r"""Auto-extracted class from agent.py"""
