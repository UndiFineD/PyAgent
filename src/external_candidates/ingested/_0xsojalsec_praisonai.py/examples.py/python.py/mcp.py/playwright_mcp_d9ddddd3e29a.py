# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\mcp\playwright-mcp.py
from praisonaiagents import MCP, Agent

search_agent = Agent(
    instructions="""You help search the web.""",
    llm="gpt-5-nano",
    tools=MCP("http://localhost:8931/sse"),
)

search_agent.start("Find about Praison AI")
