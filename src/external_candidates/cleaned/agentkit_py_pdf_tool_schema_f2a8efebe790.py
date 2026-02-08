# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentkit.py\backend.py\app.py\app.py\schemas.py\tool_schemas.py\pdf_tool_schema_f2a8efebe790.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\app\schemas\tool_schemas\pdf_tool_schema.py

# -*- coding: utf-8 -*-

from typing import List, Optional

from pydantic import BaseModel, Field


class PdfAppendix(BaseModel):
    doc_id: str

    page_numbers: List[int]

    reference_text: str


class MarkdownMetadata(BaseModel):
    type: str

    source: str

    header1: Optional[str] = Field(None, alias="Header 1")
