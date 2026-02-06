# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\mcp\whatapp-ollama-mcp.py
from praisonaiagents import MCP, Agent

whatsapp_agent = Agent(
    instructions="Whatsapp Agent",
    llm="ollama/llama3.2",
    tools=MCP("python /Users/praison/whatsapp-mcp/whatsapp-mcp-server/main.py"),
)

whatsapp_agent.start(
    "Send Hello to Mervin Praison. Use send_message tool, recipient and message are the required parameters."
)
