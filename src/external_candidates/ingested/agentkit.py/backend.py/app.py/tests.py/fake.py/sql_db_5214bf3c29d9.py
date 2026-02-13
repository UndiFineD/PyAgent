# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\tests\fake\sql_db.py
# -*- coding: utf-8 -*-
from typing import List, Sequence

from app.db.SQLDatabaseExtended import SQLDatabaseExtended
from pydantic import BaseModel
from sqlalchemy.engine.result import Row
from sqlalchemy.sql import column
from sqlalchemy.sql.sqltypes import String


class FakeTable(BaseModel):
    name: str
    structure: str


class FakeDBInfo(BaseModel):
    tables: List[FakeTable]


class FakeSQLDatabase(SQLDatabaseExtended):
    def __init__(self, db_info: FakeDBInfo):
        self.db_info = db_info

    def run_no_str(
        self, command: str, fetch: str = "all"
    ) -> Sequence | Row | List[Row] | None:
        return ["col1, col2; value1, value2"]
