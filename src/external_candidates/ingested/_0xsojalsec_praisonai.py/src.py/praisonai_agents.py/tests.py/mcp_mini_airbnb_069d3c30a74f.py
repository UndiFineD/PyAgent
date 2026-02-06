# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\mcp-mini-airbnb.py
from praisonaiagents import MCP, Agent

search_agent = Agent(
    instructions="""You help book apartments on Airbnb.""",
    llm="gpt-5-nano",
    tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"),
)

search_agent.start(
    "I want to book an apartment in Paris for 2 nights. 03/28 - 03/30 for 2 adults"
)
