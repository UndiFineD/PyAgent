# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\tools\langchain\you-search.py
from langchain_community.utilities.you import YouSearchAPIWrapper
from praisonaiagents import Agent, PraisonAIAgents

data_agent = Agent(instructions="Gather the weather data for Barcelona", tools=[YouSearchAPIWrapper])
editor_agent = Agent(instructions="Breifly describe the weather in Barcelona")

agents = PraisonAIAgents(agents=[data_agent, editor_agent])
agents.start()
