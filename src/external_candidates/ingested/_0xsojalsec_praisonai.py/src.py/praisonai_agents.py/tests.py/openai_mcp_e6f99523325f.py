# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\openai-mcp.py
from praisonaiagents import MCP, Agent

search_agent = Agent(
    instructions="""You help book apartments on Airbnb.""",
    tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"),
)

search_agent.start("Search apartment in Paris for 2 nights. 07/28 - 07/30 for 2 adults")
