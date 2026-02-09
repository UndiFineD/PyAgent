# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\basic-agents.py
from praisonaiagents import Agent

agent = Agent(instructions="You are a helpful assistant", llm="gpt-5-nano")

agent.start("Why sky is Blue?")
