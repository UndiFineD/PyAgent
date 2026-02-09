# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\mcp\whatapp-groq-mcp.py
from praisonaiagents import MCP, Agent

whatsapp_agent = Agent(
    instructions="Whatsapp Agent",
    llm="groq/llama-3.2-90b-vision-preview",
    tools=MCP("python /Users/praison/whatsapp-mcp/whatsapp-mcp-server/main.py"),
)

whatsapp_agent.start("Send Hello to Mervin Praison")
