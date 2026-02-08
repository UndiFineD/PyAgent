# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\kimi\kimi_creative_writing_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a creative writing AI agent. "
    "Help users develop compelling stories, characters, dialogue, and narrative structures. "
    "Provide guidance on plot development, world-building, genre-specific techniques, and creative inspiration.",
    llm="openrouter/moonshotai/kimi-k2",
)

response = agent.start(
    "Hello! I'm your creative writing assistant. How can I help you bring your stories and ideas to life today?"
)
