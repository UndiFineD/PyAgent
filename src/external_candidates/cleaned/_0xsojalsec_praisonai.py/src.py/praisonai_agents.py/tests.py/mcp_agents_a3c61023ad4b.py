# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\mcp-agents.py
from praisonaiagents import MCP, Agent

agent = Agent(
    instructions="""You are a helpful assistant that can check stock prices and perform other tasks.
    Use the available tools when relevant to answer user questions.""",
    llm="gpt-5-nano",
    tools=MCP("/Users/praison/miniconda3/envs/mcp/bin/python /Users/praison/stockprice/app.py"),
)

agent.start("What is the stock price of Tesla?")
