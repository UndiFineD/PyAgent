#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/WebCore.description.md

# WebCore

**File**: `src\classes\specialized\WebCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 70  
**Complexity**: 2 (simple)

## Overview

WebCore logic for PyAgent.
Pure logic for cleaning and processing web content.
No I/O or side effects.

## Classes (1)

### `WebCore`

Pure logic core for Web navigation and extraction.

**Methods** (2):
- `clean_html(html_content)`
- `extract_links(html_content, base_url)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `bs4.BeautifulSoup`
- `src.core.base.version.VERSION`
- `typing.List`
- `typing.Optional`
- `urllib.parse`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/WebCore.improvements.md

# Improvements for WebCore

**File**: `src\classes\specialized\WebCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 70 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `WebCore_test.py` with pytest tests

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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
WebCore logic for PyAgent.
Pure logic for cleaning and processing web content.
No I/O or side effects.
"""


from bs4 import BeautifulSoup
from src.core.base.version import VERSION

__version__ = VERSION


class WebCore:
    """Pure logic core for Web navigation and extraction."""

    @staticmethod
    def clean_html(html_content: str) -> str:
        """Removes script/style tags and simplifies text from HTML."""
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, "html.parser")

        # Remove navigation, scripts, and styles
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return "\n".join(chunk for chunk in chunks if chunk)

    @staticmethod
    def extract_links(html_content: str, base_url: str | None = None) -> list[str]:
        """Extracts all absolute links from HTML content."""
        import urllib.parse

        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if base_url:
                href = urllib.parse.urljoin(base_url, href)
            links.append(href)
        return list(set(links))
