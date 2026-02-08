# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_data_analysis_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a data analysis AI agent. Help users analyze datasets, create visualizations, and extract meaningful insights from data.",
    llm="xai/grok-4",
)

response = agent.start("I have sales data for the last quarter. Can you help me identify trends and patterns?")
