# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_lead_generation_assistant.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a lead generation AI agent for RealEstatePro.com. Help identify and qualify potential real estate leads.",
    llm="xai/grok-4",
)

response = agent.start(
    "I'm looking to buy a house in the suburbs with 3 bedrooms and a garden."
)
