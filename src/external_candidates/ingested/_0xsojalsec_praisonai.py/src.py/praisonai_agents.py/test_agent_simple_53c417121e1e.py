# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\test_agent_simple.py
#!/usr/bin/env python3

from praisonaiagents import Agent

print("Creating agent...")
agent = Agent(instructions="You are a helpful assistant", llm="gpt-5-nano")

print("Starting agent...")
result = agent.start("Why is the sky blue?")

print("Agent completed successfully!")
print(f"Result: {result}")
print("Script finished normally.")
