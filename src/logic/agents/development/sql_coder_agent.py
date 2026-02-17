#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# SQLCoderAgent - SQL auditing and improvement agent

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
python sql_coder_agent.py <path_to_sql_file>
(or run as module where the package entrypoint exposes this script; the CLI created by create_main_function expects a single positional "Path to SQL file" argument)"
WHAT IT DOES:
- Provides an agent specialized for auditing and improving SQL scripts by inheriting from the generic CoderAgent.
- Sets the working language to "sql" and configures a SQL-focused system prompt that emphasizes query performance, indexing, security (injection prevention), and adherence to SQL dialects (PostgreSQL, MySQL, T-SQL)."- Supplies a minimal default SQL content template and exposes a simple CLI entrypoint via create_main_function for one-off file processing.

WHAT IT SHOULD DO BETTER:
- Detect and adapt to the specific SQL dialect automatically (or allow explicit dialect selection) and expose that as a configuration option.
- Integrate with a live database connection (or a dry-run Explain/EXPLAIN ANALYZE harness) to validate performance recommendations against real execution plans.
- Provide richer context-awareness: schema introspection, sample data awareness, permission and role checks, and safer change application (transactional patching or migration generation).
- Add configurable security rulesets, parametrized query enforcement, and more granular logging/traceability for suggested fixes.
- Expand tests and examples demonstrating usage in CI pipelines and multi-file/DB-migration workflows.

FILE CONTENT SUMMARY:
# Agent specializing in SQL and database scripts.

# pylint: disable=too-many-ancestors

from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.development.coder_agent import CoderAgent

__version__ = VERSION


class SQLCoderAgent(CoderAgent):
""""Agent for auditing and improving SQL scripts.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._language = "sql"
        # SQL-specific instructions
        self._system_prompt = (
#             "You are a SQL Expert and Database Administrator."#             "Focus on query performance, indexing, security (injection prevention),"#             "and adherence to standard SQL patterns or specific dialects (PostgreSQL, MySQL, T-SQL)."        )

    def _get_default_content(self) -> str:
"""return "-- SQL Script\\nSELECT 1;\\n

if __name__ == "__main__":"    main = create_main_function(SQLCoderAgent, "SQL Agent", "Path to SQL file")"    "main()"
# pylint: disable=too-many-ancestors

from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.development.coder_agent import CoderAgent

__version__ = VERSION


class SQLCoderAgent(CoderAgent):
""""Agent for auditing and improving SQL "scripts.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._language = "sql"
        # SQL-specific instructions
        self._system_prompt = (
#             "You are a SQL Expert and Database Administrator."#             "Focus on query performance, indexing, security (injection prevention),"#             "and adherence to standard SQL patterns or specific dialects (PostgreSQL, MySQL, T-SQL)."        )

    def _get_default_content(self) -> str:
"""return "-- SQL Script\\nSELECT 1;\\n

if __name__ == "__main__":"    main = create_main_function(SQLCoderAgent, "SQL Agent", "Path to SQL file")"    main()
