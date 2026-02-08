# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\multi-agents-api.py
from praisonaiagents import Agent, Agents, Tools

research_agent = Agent(
    name="Research",
    instructions="You are a research agent to search internet about AI 2024",
    tools=[Tools.internet_search],
)
summarise_agent = Agent(name="Summarise", instructions="You are a summarize agent to summarise in points")
agents = Agents(agents=[research_agent, summarise_agent])
agents.launch(path="/agents", port=3030)
