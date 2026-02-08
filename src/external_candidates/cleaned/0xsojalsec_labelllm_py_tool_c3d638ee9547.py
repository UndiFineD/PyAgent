# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\app.py\schemas.py\tool_c3d638ee9547.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\schemas\tool.py

from typing import Literal

from pydantic import BaseModel


class ToolTranslateResponse(BaseModel):
    text: str


class ToolTranslateRequest(BaseModel):
    text: str

    source: Literal["EN", "ZH"]

    target: Literal["EN-GB", "EN-US", "ZH"]


class ToolGoogleTranslateResponse(BaseModel):
    text: str

    source: Literal["ar", "cs", "hu", "sr", "ru", "ko", "vi", "th", "de", "fr", "ja", "zh", "en"]

    target: Literal["ar", "cs", "hu", "sr", "ru", "ko", "vi", "th", "de", "fr", "ja", "zh", "en"]
