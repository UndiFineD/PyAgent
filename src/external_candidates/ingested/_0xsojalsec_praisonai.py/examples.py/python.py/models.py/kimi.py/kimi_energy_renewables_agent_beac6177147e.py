# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\kimi\kimi_energy_renewables_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are an energy and renewables AI agent. "
    "Help users understand renewable energy technologies, "
    "energy systems, and sustainability. Provide guidance on "
    "solar power, wind energy, energy storage, "
    "and green technology solutions.",
    llm="openrouter/moonshotai/kimi-k2",
)

response = agent.start(
    "Hello! I'm your energy and renewables assistant. "
    "How can I help you with renewable energy "
    "and sustainability today?"
)
