# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\deepseek-reasoning-agents.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are helpful Assisant",
    llm="deepseek-reasoner",
    reasoning_steps=True,
)

result = agent.start("Why sky is Blue?")
print(result)
