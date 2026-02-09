# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_startup_trend_analysis_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a startup trend analysis AI agent. Help entrepreneurs identify market opportunities, analyze industry trends, and evaluate business ideas.",
    llm="xai/grok-4",
)

response = agent.start(
    "I'm thinking of starting a tech startup. What are the current trending opportunities in the market?"
)
