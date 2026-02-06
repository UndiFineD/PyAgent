# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\openai\responses\tool_use_stream.py
"""Run `pip install duckduckgo-search` to install dependencies."""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIResponses(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Whats happening in France?", stream=True)
