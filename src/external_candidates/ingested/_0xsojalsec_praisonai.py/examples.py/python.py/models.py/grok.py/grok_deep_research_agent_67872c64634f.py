# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_deep_research_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a deep research AI agent. Conduct comprehensive research, analyze complex topics, and provide detailed insights on various subjects.",
    llm="xai/grok-4",
)

response = agent.start(
    "I need to research the impact of artificial intelligence on job markets. Can you provide a comprehensive analysis?"
)
