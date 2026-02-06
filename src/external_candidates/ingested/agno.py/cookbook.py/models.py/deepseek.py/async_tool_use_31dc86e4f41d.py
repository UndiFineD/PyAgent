# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\deepseek\async_tool_use.py
"""
Async example using DeepSeek with tool calls.
"""

import asyncio

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=DeepSeek(id="deepseek-chat"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
