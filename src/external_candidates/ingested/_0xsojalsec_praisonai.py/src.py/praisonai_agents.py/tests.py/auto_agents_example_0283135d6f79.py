# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\auto_agents_example.py
from praisonaiagents import AutoAgents
from praisonaiagents.tools import duckduckgo

agents = AutoAgents(
    instructions="Search for information about AI Agents",
    tools=[duckduckgo],
    process="sequential",
    verbose=True,
)

agents.start()
