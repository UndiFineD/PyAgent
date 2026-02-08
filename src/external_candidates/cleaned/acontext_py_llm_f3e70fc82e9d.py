# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\schema.py\llm_f3e70fc82e9d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\llm.py

from typing import Any, Literal, Optional

from pydantic import BaseModel


class FunctionSchema(BaseModel):
    name: str

    description: str

    parameters: dict


class ToolSchema(BaseModel):
    function: FunctionSchema

    type: Literal["function"] = "function"


class LLMFunction(BaseModel):
    name: str

    arguments: dict[str, Any]


class LLMToolCall(BaseModel):
    id: str

    function: Optional[LLMFunction] = None

    type: Literal["function"]


class LLMResponse(BaseModel):
    role: Literal["user", "assistant", "system", "tool"]

    raw_response: BaseModel

    content: Optional[str] = None

    json_content: Optional[dict] = None

    tool_calls: Optional[list[LLMToolCall]] = None
