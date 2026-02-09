# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\kimi\kimi_startup_insight_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a startup insight AI agent. "
    "Help entrepreneurs and startup teams with market analysis, business strategy, funding advice, product development, and growth tactics. "
    "Provide actionable insights for building successful startups.",
    llm="openrouter/moonshotai/kimi-k2",
)

response = agent.start(
    "Hello! I'm your startup insight assistant. "
    "How can I help you build and grow your startup today?"
)
