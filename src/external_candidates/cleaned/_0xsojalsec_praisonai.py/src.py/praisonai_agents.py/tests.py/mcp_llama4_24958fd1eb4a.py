# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\mcp-llama4.py
import os

from praisonaiagents import MCP, Agent

brave_api_key = os.getenv("BRAVE_API_KEY")

research_agent = Agent(
    instructions="Research Agent",
    llm="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    tools=MCP(
        "npx -y @modelcontextprotocol/server-brave-search",
        env={"BRAVE_API_KEY": brave_api_key},
    ),
)

research_agent.start("What is the latest research on the topic of AI and its impact on society?")
