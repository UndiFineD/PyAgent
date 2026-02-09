# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\ollama_tools\tool_use_stream.py
"""Run `pip install duckduckgo-search` to install dependencies."""

from agno.agent import Agent
from agno.models.ollama import OllamaTools
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OllamaTools(id="llama3.1:8b"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Whats happening in France?", stream=True)
