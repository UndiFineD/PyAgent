#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/intelligence/CsvAgent.description.md

# CsvAgent

**File**: `src\\logic\agents\\intelligence\\CsvAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 42  
**Complexity**: 2 (simple)

## Overview

Agent specializing in CSV and tabular data processing.

## Classes (1)

### `CsvAgent`

**Inherits from**: BaseAgent

Agent for CSV data cleaning, analysis, and transformation.

**Methods** (2):
- `__init__(self, file_path)`
- `_get_default_content(self)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/intelligence/CsvAgent.improvements.md

# Improvements for CsvAgent

**File**: `src\\logic\agents\\intelligence\\CsvAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 42 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CsvAgent_test.py` with pytest tests

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


"""Agent specializing in CSV and tabular data processing."""

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function
from src.core.base.version import VERSION

__version__ = VERSION


class CsvAgent(BaseAgent):
    """Agent for CSV data cleaning, analysis, and transformation."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are a Data Analyst and CSV Expert. "
            "Focus on tabular data integrity, cleaning, and transformation. "
            "Identify missing values, deal with encoding issues, and suggest "
            "optimal structures for data interoperability (e.g., preparing for SQL import)."
        )

    def _get_default_content(self) -> str:
        return "header1,header2\nvalue1,value2\n"


if __name__ == "__main__":
    main = create_main_function(CsvAgent, "CSV Agent", "Path to CSV file (.csv)")
    main()
