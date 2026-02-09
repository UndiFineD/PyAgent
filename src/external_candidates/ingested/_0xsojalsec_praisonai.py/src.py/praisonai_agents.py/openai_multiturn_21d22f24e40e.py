# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\openai-multiturn.py
from praisonaiagents import Agent

agent = Agent(instructions="You are a helpful assistant", llm="gpt-5-nano")
agent.start("Why sky is Blue?")
agent.start("What was my previous question?")
