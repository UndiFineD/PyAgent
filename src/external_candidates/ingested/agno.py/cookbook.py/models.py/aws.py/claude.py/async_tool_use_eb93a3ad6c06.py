# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\aws\claude\async_tool_use.py
"""
Async example using Claude with tool calls.
"""

import asyncio

from agno.agent import Agent
from agno.models.aws import Claude
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Claude(id="anthropic.claude-3-5-sonnet-20240620-v1:0"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)

asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
