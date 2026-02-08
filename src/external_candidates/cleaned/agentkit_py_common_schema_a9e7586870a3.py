# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentkit.py\backend.py\app.py\app.py\schemas.py\common_schema_a9e7586870a3.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\app\schemas\common_schema.py

# -*- coding: utf-8 -*-

from caseconverter import camelcase

from pydantic import BaseModel


class QueryBase(BaseModel):
    """Query base schema."""

    class Config:
        populate_by_name = True

        @staticmethod
        def alias_generator(
            s: str,
        ) -> str:
            return camelcase(s)
