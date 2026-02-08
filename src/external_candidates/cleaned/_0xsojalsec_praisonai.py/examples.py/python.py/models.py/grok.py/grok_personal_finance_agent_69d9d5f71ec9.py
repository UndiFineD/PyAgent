# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_personal_finance_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a personal finance AI agent. Help users with budgeting, saving strategies, debt management, and financial planning advice.",
    llm="xai/grok-4",
)

response = agent.start("I want to save $10,000 in the next year. What's the best strategy for me?")
