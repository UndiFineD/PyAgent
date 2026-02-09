# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\ollama-agents.py
from praisonaiagents import Agent

agent = Agent(instructions="You are a helpful assistant", llm="ollama/qwen3")

agent.start("Why sky is Blue?")
