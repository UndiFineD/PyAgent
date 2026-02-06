# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\mistral\tool_use.py
"""Run `pip install duckduckgo-search` to install dependencies."""

from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=MistralChat(
        id="mistral-large-latest",
    ),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)

agent.print_response("Whats happening in France?", stream=True)
