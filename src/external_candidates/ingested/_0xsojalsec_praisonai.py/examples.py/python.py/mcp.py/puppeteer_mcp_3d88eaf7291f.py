# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\mcp\puppeteer-mcp.py
import os

from praisonaiagents import MCP, Agent

# Use a single string command with Puppeteer configuration
puppeteer_agent = Agent(
    instructions="""You are a helpful assistant that can automate web browser interactions.
    Use the available tools when relevant to perform web automation tasks.""",
    llm="gpt-5-nano",
    tools=MCP("npx -y @modelcontextprotocol/server-puppeteer"),
)

puppeteer_agent.start("Navigate to example.com and take a screenshot")
