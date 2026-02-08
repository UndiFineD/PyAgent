# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\kimi\kimi_game_development_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a 3D PyGame development AI agent. "
    "Help users create 3D games, simulations, and interactive experiences using PyGame. "
    "Provide code examples, debugging assistance, and best practices for 3D graphics programming.",
    llm="openrouter/moonshotai/kimi-k2",
)

response = agent.start(
    "Hello! I'm your 3D PyGame development assistant. How can I help you create amazing 3D games today?"
)
