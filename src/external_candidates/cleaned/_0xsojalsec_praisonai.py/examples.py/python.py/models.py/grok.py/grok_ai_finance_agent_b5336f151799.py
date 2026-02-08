# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_ai_finance_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a finance AI agent. "
    "Help users with financial analysis, investment strategies, "
    "budget planning, and market trend analysis for informed decision making.",
    llm="xai/grok-4",
)

response = agent.start(
    "I need to analyze my investment portfolio and create a diversification strategy. "
    "Can you help me optimize my financial planning?"
)
