# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\recommendation-agent.py
from praisonaiagents import Agent, Tools
from praisonaiagents.tools import duckduckgo

agent = Agent(instructions="You are a Recommendation Agent", tools=[duckduckgo])
agent.start("Recommend me a good movie to watch in 2025")
