#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/search/SearchAgent.description.md

# SearchAgent

**File**: `src\classes\search\SearchAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 181  
**Complexity**: 8 (moderate)

## Overview

Agent for performing web searches and deep research.

## Classes (1)

### `SearchAgent`

**Inherits from**: BaseAgent

Agent that specializes in researching topics via web search.

**Methods** (8):
- `__init__(self, context)`
- `_get_default_content(self)`
- `_record(self, provider, query, result)`
- `_search_duckduckgo(self, query, max_results)`
- `_search_bing(self, query, max_results)`
- `_search_google(self, query, max_results)`
- `perform_search(self, query)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (14):
- `SearchCore.SearchCore`
- `__future__.annotations`
- `duckduckgo_search.DDGS`
- `logging`
- `os`
- `pathlib.Path`
- `requests`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `time`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/search/SearchAgent.improvements.md

# Improvements for SearchAgent

**File**: `src\classes\search\SearchAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 181 lines (medium)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SearchAgent_test.py` with pytest tests

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


r"""Agent for performing web searches and deep research."""
