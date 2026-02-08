# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\tools\website_tools.py
from agno.agent import Agent
from agno.tools.website import WebsiteTools

agent = Agent(tools=[WebsiteTools()], show_tool_calls=True)

agent.print_response("Search web page: 'https://docs.agno.com/introduction'", markdown=True)
