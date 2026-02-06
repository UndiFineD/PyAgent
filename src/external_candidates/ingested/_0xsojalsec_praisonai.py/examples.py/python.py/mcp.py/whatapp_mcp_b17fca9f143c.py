# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\mcp\whatapp-mcp.py
from praisonaiagents import MCP, Agent

whatsapp_agent = Agent(
    instructions="Whatsapp Agent",
    llm="gpt-5-nano",
    tools=MCP("python /Users/praison/whatsapp-mcp/whatsapp-mcp-server/main.py"),
)

whatsapp_agent.start("Send Hello to Mervin Praison")
