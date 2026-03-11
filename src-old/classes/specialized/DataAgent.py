#!/usr/bin/env python3
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
    """Advanced agent for database interaction and data processing."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.conn = None
        self._system_prompt = (
            "You are the Advanced Data Agent. "
            "Your role is to manage databases, execute optimized SQL queries, and perform data analysis. "
            "You default to SQLite for local operations but can handle various dialects. "
            "Always verify query safety and performance before execution."
        )

    @as_tool
    def connect(self, db_path: str = ":memory:") -> str:
        """Connects to a SQLite database. Defaults to an in-memory database."""
        try:
            self.conn = sqlite3.connect(db_path)
            return f"Successfully connected to database: {db_path}"
        except Exception as e:
            return f"Error connecting to database: {e}"

    @as_tool
    def execute_sql(self, sql: str) -> str:
        """Executes a SQL query and returns the result as a formatted string."""
        import pandas as pd

        if not self.conn:
            return "Error: No database connection. Call 'connect' first."

        try:
            # Check if it's a SELECT query
            if sql.strip().upper().startswith("SELECT"):
                df = pd.read_sql_query(sql, self.conn)
                if df.empty:
                    return "Query returned no results."
                return df.to_string(index=False)
            else:
                cursor = self.conn.cursor()
                cursor.execute(sql)
                self.conn.commit()
                return "Command executed successfully."
        except Exception as e:
            return f"Error executing SQL: {e}"

    @as_tool
    def get_schema(self) -> str:
        """Retrieves the schema of the currently connected database."""
        if not self.conn:
            return "Error: No database connection."

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            schema_info = []
            for table in tables:
                table_name = table[0]
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                cols_str = ", ".join([f"{c[1]} ({c[2]})" for c in columns])
                schema_info.append(f"Table: {table_name} | Columns: {cols_str}")

            return (
                "\n".join(schema_info) if schema_info else "Database holds no tables."
            )
        except Exception as e:
            return f"Error retrieving schema: {e}"

    @as_tool
    def query_to_csv(self, sql: str, output_path: str) -> str:
        """Executes a query and saves the result to a CSV file."""
        import pandas as pd

        if not self.conn:
            return "Error: No database connection."

        try:
            df = pd.read_sql_query(sql, self.conn)
            df.to_csv(output_path, index=False)
            return f"Query results saved to {output_path}"
        except Exception as e:
            return f"Error saving to CSV: {e}"

    def improve_content(self, prompt: str) -> str:
        """Analyzes a data-related prompt and executes the appropriate tool."""
        return f"DataAgent processing: {prompt}\n(Use specific tools for execution)"


if __name__ == "__main__":
    main = create_main_function(DataAgent, "Data Agent", "Path to data log")
    main()
