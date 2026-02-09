# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\aws\bedrock\tool_use_stream.py
"""Run `pip install duckduckgo-search` to install dependencies."""

from agno.agent import Agent
from agno.models.aws import AwsBedrock
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=AwsBedrock(id="amazon.nova-lite-v1:0"),
    tools=[DuckDuckGoTools()],
    instructions="You are a helpful assistant that can use the following tools to answer questions.",
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Whats happening in France?", stream=True)
