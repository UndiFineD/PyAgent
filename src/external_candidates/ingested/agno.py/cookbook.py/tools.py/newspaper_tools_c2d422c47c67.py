# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\tools\newspaper_tools.py
from agno.agent import Agent
from agno.tools.newspaper import NewspaperTools

agent = Agent(tools=[NewspaperTools()])
agent.print_response("Please summarize https://en.wikipedia.org/wiki/Language_model")
