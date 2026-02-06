# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\fireworks\tool_use.py
"""Run `pip install duckduckgo-search` to install dependencies."""

from agno.agent import Agent
from agno.models.fireworks import Fireworks
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Fireworks(id="accounts/fireworks/models/llama-v3p1-405b-instruct"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Whats happening in France?", stream=True)
