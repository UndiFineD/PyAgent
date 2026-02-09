# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\agents\websearch-agent.py
from praisonaiagents import Agent, Tools
from praisonaiagents.tools import duckduckgo

agent = Agent(instructions="You are a Web Search Agent", tools=[duckduckgo])
agent.start("Search about AI 2024")
