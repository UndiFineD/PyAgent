# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\app\schemas\agent_schema.py
# -*- coding: utf-8 -*-
from typing import Dict, Optional

from app.schemas.tool_schema import LLMType, ToolsLibrary
from pydantic.v1 import (
    BaseModel,  # TODO: Remove this line when langchain upgrades to pydantic v2
)


class ActionPlan(BaseModel):
    name: str
    description: str
    actions: list[list[str]]


class ActionPlans(BaseModel):
    action_plans: Dict[str, ActionPlan]


class AgentAndToolsConfig(BaseModel):
    llm: LLMType
    fast_llm: LLMType
    fast_llm_token_limit: int
    max_token_length: int


class AgentConfig(BaseModel):
    common: AgentAndToolsConfig
    tools: list[str]
    action_plans: ActionPlans
    prompt_message: str
    system_context: str
    tools_library: ToolsLibrary
    api_key: Optional[str] = None
