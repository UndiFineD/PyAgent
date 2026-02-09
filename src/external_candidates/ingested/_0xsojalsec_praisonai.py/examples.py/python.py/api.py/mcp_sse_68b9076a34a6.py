# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\api\mcp-sse.py
from praisonaiagents import MCP, Agent

qa_agent = Agent(
    instructions="""You are a Question Answering Agent.""",
    llm="openai/gpt-5-nano",
    tools=MCP("http://localhost:8080/agents/sse"),
)

qa_agent.start("AI in 2025")
