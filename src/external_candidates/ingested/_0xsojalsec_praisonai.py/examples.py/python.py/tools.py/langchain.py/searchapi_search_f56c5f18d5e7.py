# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\tools\langchain\searchapi-search.py
from langchain_community.utilities import SearchApiAPIWrapper
from praisonaiagents import Agent, PraisonAIAgents

data_agent = Agent(
    instructions="I am looking for the top google searches of 2025",
    tools=[SearchApiAPIWrapper],
)
editor_agent = Agent(instructions="Analyze the data and derive insights")

agents = PraisonAIAgents(agents=[data_agent, editor_agent])
agents.start()
