# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentkit.py\backend.py\app.py\app.py\schemas.py\streaming_schema_e668fa1bea2d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\app\schemas\streaming_schema.py

# -*- coding: utf-8 -*-

from enum import Enum

from typing import Any

from pydantic import BaseModel


class StreamingDataTypeEnum(Enum):
    TEXT = "text"

    LLM = "llm"

    APPENDIX = "appendix"

    ACTION = "action"

    SIGNAL = "signal"


class StreamingSignalsEnum(Enum):
    START = "START"

    END = "END"

    TOOL_END = "TOOL_END"

    LLM_END = "LLM_END"


class StreamingData(BaseModel):
    data: str

    data_type: StreamingDataTypeEnum = StreamingDataTypeEnum.TEXT

    metadata: dict[
        str,
        Any,
    ] = {}
