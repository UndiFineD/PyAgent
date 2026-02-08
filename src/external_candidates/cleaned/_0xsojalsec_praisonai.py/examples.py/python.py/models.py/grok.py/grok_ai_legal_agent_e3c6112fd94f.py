# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_ai_legal_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a legal AI agent. "
    "Help users with legal document analysis, contract review, "
    "and legal advice while ensuring compliance and risk assessment.",
    llm="xai/grok-4",
)

response = agent.start(
    "I need to review a software licensing agreement. Can you help me identify potential risks and key terms?"
)
