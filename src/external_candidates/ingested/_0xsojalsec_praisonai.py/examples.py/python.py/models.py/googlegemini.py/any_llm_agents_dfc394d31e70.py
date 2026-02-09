# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\googlegemini\any-llm-agents.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a helpful assistant",
    llm="gemini/gemini-1.5-flash-8b",
    self_reflect=True,
    verbose=True,
)

agent.start("Why sky is Blue?")
