#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/processing/data_parsing_core.description.md

# data_parsing_core

**File**: `src\\core\base\\logic\\processing\\data_parsing_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 65  
**Complexity**: 3 (simple)

## Overview

Module: data_parsing_core
Core logic for data parsing operations.
Implements XML/HTML parsing patterns from ADSyncDump-BOF.

## Classes (1)

### `DataParsingCore`

Core class for data parsing operations.

**Methods** (3):
- `html_unescape(self, text)`
- `extract_xml_value(self, xml, tag_pattern)`
- `find_pattern(self, haystack, needle)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `html`
- `re`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/processing/data_parsing_core.improvements.md

# Improvements for data_parsing_core

**File**: `src\\core\base\\logic\\processing\\data_parsing_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 65 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `data_parsing_core_test.py` with pytest tests

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
Module: data_parsing_core
Core logic for data parsing operations.
Implements XML/HTML parsing patterns from ADSyncDump-BOF.
"""


import html
from typing import Optional


class DataParsingCore:
    """Core class for data parsing operations."""

    def html_unescape(self, text: str) -> str:
        """Unescape HTML entities in text."""
        return html.unescape(text)

    def extract_xml_value(self, xml: str, tag_pattern: str) -> Optional[str]:
        """Extract value from XML using tag pattern."""
        try:
            # Simple pattern-based extraction
            start_pattern = f"<{tag_pattern}>"
            end_pattern = f"</{tag_pattern}>"

            start_pos = xml.find(start_pattern)
            if start_pos == -1:
                return None

            start_pos += len(start_pattern)
            end_pos = xml.find(end_pattern, start_pos)
            if end_pos == -1:
                return None

            value = xml[start_pos:end_pos]
            return self.html_unescape(value)

        except Exception:
            return None

    def find_pattern(self, haystack: str, needle: str) -> Optional[str]:
        """Find pattern in text using simple string scanning."""
        try:
            pos = haystack.find(needle)
            if pos == -1:
                return None
            return haystack[pos:]
        except Exception:
            return None
