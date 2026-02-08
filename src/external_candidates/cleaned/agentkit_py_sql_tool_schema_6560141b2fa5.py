# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentkit.py\backend.py\app.py\app.py\schemas.py\tool_schemas.py\sql_tool_schema_6560141b2fa5.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\app\schemas\tool_schemas\sql_tool_schema.py

# -*- coding: utf-8 -*-

from typing import Any, List

from app.schemas.common_schema import QueryBase

from pydantic import BaseModel


class TableInfo(BaseModel):
    """Table information."""

    schema_name: str

    table_name: str

    structure: str

    @property
    def name(
        self,
    ) -> str:
        return self.schema_name + "." + self.table_name


class DatabaseInfo(BaseModel):
    """Database information."""

    tables: List[TableInfo]


class ExecutionResult(QueryBase):
    raw_result: List[
        dict[
            str,
            Any,
        ]
    ]

    affected_rows: int | None = None

    error: str | None = None
