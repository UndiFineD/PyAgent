# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\mcp\mcp-sse-weather.py
from praisonaiagents import MCP, Agent

search_agent = Agent(
    instructions="""You are a weather agent that can provide weather information for a given city.""",
    llm="openai/gpt-5-nano",
    tools=MCP("http://localhost:8080/sse"),
)

search_agent.start("What is the weather in London?")
