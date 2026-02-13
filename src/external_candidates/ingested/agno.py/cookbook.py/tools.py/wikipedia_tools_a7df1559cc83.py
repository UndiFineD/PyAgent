# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\tools\wikipedia_tools.py
from agno.agent import Agent
from agno.tools.wikipedia import WikipediaTools

agent = Agent(tools=[WikipediaTools()], show_tool_calls=True)
agent.print_response("Search wikipedia for 'ai'")
