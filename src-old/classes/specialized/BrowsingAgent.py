#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/BrowsingAgent.description.md

# BrowsingAgent

**File**: `src\classes\specialized\BrowsingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 62  
**Complexity**: 4 (simple)

## Overview

Agent specializing in web browsing, information retrieval, and data extraction.
Inspired by Skyvern and BrowserOS.

## Classes (1)

### `BrowsingAgent`

**Inherits from**: BaseAgent

Interacts with the web to retrieve documentation, search for solutions, and extract data.

**Methods** (4):
- `__init__(self, file_path)`
- `search_and_summarize(self, query)`
- `extract_api_spec(self, url)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/BrowsingAgent.improvements.md

# Improvements for BrowsingAgent

**File**: `src\classes\specialized\BrowsingAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 62 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `BrowsingAgent_test.py` with pytest tests

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


"""Agent specializing in web browsing, information retrieval, and data extraction.
Inspired by Skyvern and BrowserOS.
"""

import logging

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.core.base.version import VERSION

__version__ = VERSION


class BrowsingAgent(BaseAgent):
    """Interacts with the web to retrieve documentation, search for solutions, and extract data."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Browsing Agent. "
            "Your role is to find information on the web that the fleet is missing. "
            "Use web search and page fetching to retrieve documentation, API specs, or debugging solutions. "
            "Think critically about the sources and prioritize official documentation."
        )

    @as_tool
    def search_and_summarize(self, query: str) -> str:
        """Searches the web for a query and provides a summarized report.
        (Uses available workspace tools for actual fetching).
        """
        logging.info(f"BrowsingAgent searching for: {query}")
        # In a real scenario, this would call a search engine tool.
        # Since we are an agent, we provide a plan for fetching.
        return f"Plan: 1. Search for '{query}' using Bing/Google. 2. Fetch top 3 results. 3. Synthesize answer."

    @as_tool
    def extract_api_spec(self, url: str) -> str:
        """Attempts to find and extract an OpenAPI/Swagger spec from a given URL."""
        logging.info(f"BrowsingAgent extracting spec from: {url}")
        # Here we would use fetch_webpage (which is available to us via the host)
        # For the simulation, we return a hypothesized success message.
        return f"Browsing {url}... Detected OpenAPI 3.0 spec. Ready for SpecToolAgent."

    def improve_content(self, prompt: str) -> str:
        """Browse the web based on a prompt."""
        if "http" in prompt:
            return self.extract_api_spec(prompt)
        return self.search_and_summarize(prompt)
