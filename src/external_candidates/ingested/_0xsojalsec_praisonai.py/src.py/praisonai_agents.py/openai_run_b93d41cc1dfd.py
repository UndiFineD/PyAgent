# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\openai-run.py
import asyncio

from praisonaiagents import Agent

agent = Agent(instructions="You are a helpful assistant", llm="gpt-5-nano")
agent.run("Why sea is Blue?")


async def main():
    await agent.arun("Why sky is Blue?")
    await agent.arun("What was my previous question?")


asyncio.run(main())
