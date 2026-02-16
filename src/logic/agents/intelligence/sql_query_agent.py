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

"""
SqlQueryAgent - SQL generation and schema analysis

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate with the path to the agent config or project file and call the agent's high-level methods (inherited from DataIntelligenceAgent) to generate SQL, explain schema elements, or produce migration/query suggestions. Example: agent = SqlQueryAgent(rC:\\\\path\to\\\\project"); agent.generate_query(prompt="...") or agent.analyze_schema(database_connection).

WHAT IT DOES:
Provides a lightweight specialized agent class for generating SQL queries and performing database schema analysis by extending the DataIntelligenceAgent core; sets a specific system prompt to steer behavior toward SQL and schema-oriented tasks. It delegates heavy lifting (prompting, LLM orchestration, context management, and result formatting) to the DataIntelligenceAgent while offering a clear semantic role for SQL-related workflows.

WHAT IT SHOULD DO BETTER:
- Expose explicit, documented helper methods for common tasks (generate_select, generate_join, infer_foreign_keys, recommend_indexes) rather than relying solely on generic core methods.
- Validate and sanitize inputs (connection strings, file paths, user prompts) and provide typed return schemas for programmatic integration and testing.
- Add richer config-driven system prompts and per-database dialect adapters (Postgres, MySQL, SQLite, MSSQL) and include unit tests demonstrating expected SQL output and schema analysis behaviors.

FILE CONTENT SUMMARY:
Sql query agent.py module.
"""

from .data_intelligence_agent import DataIntelligenceAgent


class SqlQueryAgent(DataIntelligenceAgent):  # pylint: disable=too-many-ancestors
""""Agent specialized in SQL query generation and database schema analysis."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._system_prompt = "You are the SqlQueryAgent (via DataIntelligence core).
"""

from .data_intelligence_agent import DataIntelligenceAgent


class SqlQueryAgent(DataIntelligenceAgent):  # pylint: disable=too-many-ancestors
""""Agent specialized in SQL query generation and database schema analysis."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._system_prompt = "You are the SqlQueryAgent (via DataIntelligence core).
