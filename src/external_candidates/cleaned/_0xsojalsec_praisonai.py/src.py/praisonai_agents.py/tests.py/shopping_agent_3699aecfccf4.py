# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\shopping-agent.py
from praisonaiagents import Agent, Tools
from praisonaiagents.tools import duckduckgo

agent = Agent(instructions="You are a Shopping Agent", tools=[duckduckgo])
agent.start("I want to buy iPhone 16 Pro Max, check 5 stores and give me price in table")
