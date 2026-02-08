# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\tools\arxiv_tools.py
from agno.agent import Agent
from agno.tools.arxiv import ArxivTools

agent = Agent(tools=[ArxivTools()], show_tool_calls=True)
agent.print_response("Search arxiv for 'language models'", markdown=True)
