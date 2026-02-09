# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\tools\crawl4ai_tools.py
from agno.agent import Agent
from agno.tools.crawl4ai import Crawl4aiTools

agent = Agent(tools=[Crawl4aiTools(max_length=None)], show_tool_calls=True)
agent.print_response("Tell me about https://github.com/agno-agi/agno.")
