# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\mcp-sse.py
from praisonaiagents import MCP, Agent

tweet_agent = Agent(
    instructions="""You are a Tweet Formatter Agent.""",
    tools=MCP("http://localhost:8080/sse"),
)

tweet_agent.start("AI in Healthcare")
