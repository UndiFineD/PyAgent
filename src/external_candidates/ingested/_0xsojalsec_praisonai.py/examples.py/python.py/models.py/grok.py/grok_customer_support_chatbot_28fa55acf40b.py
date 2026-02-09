# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_customer_support_chatbot.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a customer support AI agent for TechGadgets.com, an online electronics store. Answer customer queries helpfully.",
    llm="xai/grok-4",
)

response = agent.start("How to return an item?")
