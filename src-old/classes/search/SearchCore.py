#!/usr/bin/env python3
"""
LLM_CONTEXT_START

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

from src.core.base.version import VERSION
from typing import List, Dict, Any

__version__ = VERSION


class SearchCore:
    """Pure logic core for search result processing."""

    @staticmethod
    def parse_bing_results(data: dict[str, Any]) -> list[str]:
        """Parses Bing web search results into Markdown blocks."""
        results: list[str] = []
        for v in data.get("webPages", {}).get("value", []):
            name = v.get("name", "Untitled Result")
            url = v.get("url", "#")
            snippet = v.get("snippet", "No snippet available.")
            results.append(f"### {name}\nURL: {url}\n{snippet}\n")
        return results

    @staticmethod
    def parse_google_results(data: dict[str, Any]) -> list[str]:
        """Parses Google Custom Search results into Markdown blocks."""
        results: list[str] = []
        for item in data.get("items", []):
            title = item.get("title", "Untitled Result")
            link = item.get("link", "#")
            snippet = item.get("snippet", "No snippet available.")
            results.append(f"### {title}\nURL: {link}\n{snippet}\n")
        return results

    @staticmethod
    def parse_ddg_results(data: list[dict[str, Any]]) -> list[str]:
        """Parses DuckDuckGo results from ddg_search library format."""
        results: list[str] = []
        for r in data:
            title = r.get("title", "Untitled Result")
            href = r.get("href", "#")
            body = r.get("body", "No description available.")
            results.append(f"### {title}\nURL: {href}\n{body}\n")
        return results

    @staticmethod
    def format_results_block(results: list[str], provider: str) -> str:
        """Combines list of results into a single string with a provider-specific indicator."""
        if not results:
            return f"No {provider} results found."
        return "\n".join(results)
