# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_web_navigator.py\src.py\tool.py\thinking_f6a36373080c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\src\tool\thinking.py

from pydantic import BaseModel, Field

from src.tool import Tool


class Thinking(BaseModel):
    thought: str = Field(..., description="Your extended thinking goes here")


@Tool("Thinking Tool", params=Thinking)
async def thinking_tool(thought: str, context=None):
    """

    To think about something. It will not obtain new information or make any changes, but just log the thought.

    Use it when complex reasoning or brainstorming is needed.

    """

    return thought
