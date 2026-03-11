#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/base/mixins/database_access_mixin.description.md

# database_access_mixin

**File**: `src\\core\base\\mixins\\database_access_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 52  
**Complexity**: 5 (moderate)

## Overview

Module: database_access_mixin
Database access mixin for BaseAgent, implementing ODBC database operations.
Inspired by ADSyncDump-BOF database connection patterns.

## Classes (1)

### `DatabaseAccessMixin`

Mixin providing database access features using ODBC.

**Methods** (5):
- `__init__(self)`
- `connect_odbc(self, connection_string)`
- `execute_query(self, query)`
- `disconnect(self)`
- `get_last_error(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `platform`
- `src.core.base.logic.processing.database_access_core.DatabaseAccessCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/database_access_mixin.improvements.md

# Improvements for database_access_mixin

**File**: `src\\core\base\\mixins\\database_access_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 52 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `database_access_mixin_test.py` with pytest tests

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
Module: database_access_mixin
Database access mixin for BaseAgent, implementing ODBC database operations.
Inspired by ADSyncDump-BOF database connection patterns.
"""


import platform
from typing import Any, Dict, List, Optional

from src.core.base.logic.processing.database_access_core import DatabaseAccessCore


class DatabaseAccessMixin:
    """Mixin providing database access features using ODBC."""

    def __init__(self, **kwargs: Any) -> None:
        if platform.system() != "Windows":
            raise RuntimeError("DatabaseAccessMixin is only supported on Windows")

        self.db_core = DatabaseAccessCore()

    def connect_odbc(self, connection_string: str) -> bool:
        """Connect to database using ODBC connection string."""
        return self.db_core.connect(connection_string)

    def execute_query(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Execute SQL query and return results."""
        return self.db_core.execute_query(query)

    def disconnect(self) -> None:
        """Disconnect from database."""
        self.db_core.disconnect()

    def get_last_error(self) -> str:
        """Get last database error message."""
        return self.db_core.get_last_error()
