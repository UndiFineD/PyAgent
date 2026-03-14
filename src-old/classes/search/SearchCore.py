#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/search/SearchCore.description.md

# SearchCore

**File**: `src\classes\search\SearchCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 69  
**Complexity**: 4 (simple)

## Overview

SearchCore logic for PyAgent.
Pure logic for parsing search results from various providers.
No I/O or side effects.

## Classes (1)

### `SearchCore`

Pure logic core for search result processing.

**Methods** (4):
- `parse_bing_results(data)`
- `parse_google_results(data)`
- `parse_ddg_results(data)`
- `format_results_block(results, provider)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/search/SearchCore.improvements.md

# Improvements for SearchCore

**File**: `src\classes\search\SearchCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 69 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SearchCore_test.py` with pytest tests

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


"""
SearchCore logic for PyAgent.
Pure logic for parsing search results from various providers.
No I/O or side effects.
"""
from typing import Any

from src.core.base.version import VERSION

__version__ = VERSION


class SearchCore:
    """
    """
