# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\mcp\redis-mcp.py
import os

from praisonaiagents import MCP, Agent

# Redis connection string
redis_url = "redis://localhost:6379"

# Use a single string command with Redis configuration
redis_agent = Agent(
    instructions="""You are a helpful assistant that can interact with Redis.
    Use the available tools when relevant to manage Redis operations.""",
    llm="gpt-5-nano",
    tools=MCP("npx -y @modelcontextprotocol/server-redis", args=[redis_url]),
)

redis_agent.start("Set a key-value pair in Redis")
