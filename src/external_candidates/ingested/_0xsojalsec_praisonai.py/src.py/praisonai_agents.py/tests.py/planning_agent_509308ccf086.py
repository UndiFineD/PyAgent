# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\planning-agent.py
from praisonaiagents import Agent, Tools
from praisonaiagents.tools import duckduckgo

agent = Agent(instructions="You are a Planning Agent", tools=[duckduckgo])
agent.start("I want to go London next week, find me a good hotel and flight")
