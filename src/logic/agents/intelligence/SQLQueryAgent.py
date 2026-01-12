#!/usr/bin/env python3
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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Agent specializing in SQL database interaction and query optimization."""



import sqlite3
import logging
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool


class SQLQueryAgent(BaseAgent):
    """Enables the fleet to interact with relational databases and unified data sources (MindsDB style)."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.connection: Optional[sqlite3.Connection] = None
        self._system_prompt = (
            "You are the SQL Database Agent. "
            "Your role is to 'Connect, Unify, and Respond' from data sources. "
            "You act as a Query Engine for AI, allowing natural language questions to be "
            "answered via federated data across multiple unified views."
        )

    @as_tool
    def unify_sources(self, source_identities: List[str]) -> str:
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
    main = create_main_function(SQLAgent, "SQL Agent", "Database path")
    main()
