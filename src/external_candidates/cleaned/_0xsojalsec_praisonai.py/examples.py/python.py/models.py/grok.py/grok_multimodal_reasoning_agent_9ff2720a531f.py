# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_multimodal_reasoning_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a multimodal reasoning AI agent. Analyze images and text to provide comprehensive insights.",
    llm="xai/grok-4",
)

response = agent.start("Can you help me analyze a chart showing sales data for Q1 2024?")
