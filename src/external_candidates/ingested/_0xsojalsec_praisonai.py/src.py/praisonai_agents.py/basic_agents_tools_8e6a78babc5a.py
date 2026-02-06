# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\basic-agents-tools.py
from praisonaiagents import Agent


def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"


agent = Agent(
    instructions="You are a helpful assistant", llm="gpt-5-nano", tools=[get_weather]
)

agent.start("What is the weather in Tokyo?")
