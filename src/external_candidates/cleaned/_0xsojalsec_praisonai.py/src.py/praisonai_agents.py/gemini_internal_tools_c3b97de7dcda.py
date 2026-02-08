# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\gemini-internal-tools.py
from praisonaiagents import Agent

agent = Agent(
    instructions="Research assistant with web search",
    llm="gemini/gemini-2.5-flash",
    tools=[
        {"googleSearch": {}},
    ],
)

response = agent.start("Who is Mervin Praison?")
