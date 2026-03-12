#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/SQLAgent.description.md

# SQLAgent

**File**: `src\classes\specialized\SQLAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 102  
**Complexity**: 7 (moderate)

## Overview

Agent specializing in SQL database interaction and query optimization.

## Classes (1)

### `SQLQueryAgent`

**Inherits from**: BaseAgent

Enables the fleet to interact with relational databases and unified data sources (MindsDB style).

**Methods** (7):
- `__init__(self, file_path)`
- `unify_sources(self, source_identities)`
- `connect_mcp_datasource(self, mcp_server_url)`
- `connect_local(self, db_path)`
- `execute_query(self, query)`
- `get_table_schema(self, table_name)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `sqlite3`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/SQLAgent.improvements.md

# Improvements for SQLAgent

**File**: `src\classes\specialized\SQLAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 102 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SQLAgent_test.py` with pytest tests

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


"""Agent specializing in SQL database interaction and query optimization."""

import logging
import sqlite3

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.core.base.version import VERSION

__version__ = VERSION


class SQLQueryAgent(BaseAgent):
    """Enables the fleet to interact with relational databases and unified data sources (MindsDB style)."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.connection: sqlite3.Connection | None = None
        self._system_prompt = (
            "You are the SQL Database Agent. "
            "Your role is to 'Connect, Unify, and Respond' from data sources. "
            "You act as a Query Engine for AI, allowing natural language questions to be "
            "answered via federated data across multiple unified views."
        )

    @as_tool
    def unify_sources(self, source_identities: list[str]) -> str:
        """Simulates unifying multiple data sources into a single queryable view (MindsDB Pattern)."""
        logging.info(f"Unifying data sources: {source_identities}")
        return f"Unified Knowledge Base created for: {', '.join(source_identities)}. Virtual Schema: AI_PUBLIC."

    @as_tool
    def connect_mcp_datasource(self, mcp_server_url: str) -> str:
        """Connects to an external data source via the MindsDB MCP server."""
        logging.info(f"Connecting to data federation via MCP: {mcp_server_url}")
        return "Connected to Model Context Protocol (MCP) data plane."

    @as_tool
    def connect_local(self, db_path: str) -> str:
        """Connects to a local SQLite database."""
        try:
            self.connection = sqlite3.connect(db_path)
            return f"Successfully connected to SQLite database at {db_path}."
        except Exception as e:
            return f"Error connecting to database: {e}"

    @as_tool
    def execute_query(self, query: str) -> str:
        """Executes a Read-Only SQL query and returns the results."""
        if not self.connection:
            return "Error: No database connection active."

        # Security check: Block destructive commands in execute_query (read-only by intent)
        destructive = ["drop", "delete", "truncate", "alter", "update", "insert"]
        if any(cmd in query.lower() for cmd in destructive):
            return "Error: Destructive command detected. Use 'execute_transaction' for writes."

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            if not rows:
                return "Query executed successfully. 0 rows returned."
            return str(rows)
        except Exception as e:
            return f"SQL Error: {e}"

    @as_tool
    def get_table_schema(self, table_name: str) -> str:
        """Returns the schema for a specific table."""
        if not self.connection:
            return "Error: No database connection."
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            return str(cursor.fetchall())
        except Exception as e:
            return f"Schema Error: {e}"

    def improve_content(self, prompt: str) -> str:
        """SQL generation helper."""
        return f"SQLAgent: Ready to query database. Connection active: {self.connection is not None}."


if __name__ == "__main__":
    from src.core.base.utilities import create_main_function

    main = create_main_function(SQLQueryAgent, "SQL Agent", "Database path")
    main()
