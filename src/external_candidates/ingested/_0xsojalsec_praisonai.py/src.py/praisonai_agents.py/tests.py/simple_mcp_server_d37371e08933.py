# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\simple-mcp-server.py
from praisonaiagents import Agent

agent = Agent(instructions="Create a Tweet")
agent.launch(port=8080, protocol="mcp")
