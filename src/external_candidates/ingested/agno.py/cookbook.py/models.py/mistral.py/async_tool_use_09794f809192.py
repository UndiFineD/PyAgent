# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\mistral\async_tool_use.py
"""
Async example using Mistral with tool calls.
"""

import asyncio

from agno.agent import Agent
from agno.models.mistral.mistral import MistralChat
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=MistralChat(id="mistral-large-latest"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)

asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
