# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\simple-api-mcp.py
from praisonaiagents import MCP, Agent

search_agent = Agent(
    instructions="""You are a Tweet.""",
    llm="openai/gpt-5-nano",
    tools=MCP("http://localhost:8080/sse"),
)
search_agent.launch(path="/tweet", port=3030)
