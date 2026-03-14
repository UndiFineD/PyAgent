#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/DataAgent.description.md

# DataAgent

**File**: `src\classes\specialized\DataAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 116  
**Complexity**: 6 (moderate)

## Overview

Agent specializing in advanced SQL operations, data analysis, and database management.
Provides execution capabilities and schema discovery.

## Classes (1)

### `DataAgent`

**Inherits from**: BaseAgent

Advanced agent for database interaction and data processing.

**Methods** (6):
- `__init__(self, file_path)`
- `connect(self, db_path)`
- `execute_sql(self, sql)`
- `get_schema(self)`
- `query_to_csv(self, sql, output_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pandas`
- `sqlite3`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/DataAgent.improvements.md

# Improvements for DataAgent

**File**: `src\classes\specialized\DataAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 116 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `DataAgent_test.py` with pytest tests

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


"""Agent specializing in advanced SQL operations, data analysis, and database management.
Provides execution capabilities and schema discovery.
"""
import sqlite3

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool, create_main_function
from src.core.base.version import VERSION

# Lazy loaded: pandas moved to localized usage
__version__ = VERSION


class DataAgent(BaseAgent):
    """
    """
