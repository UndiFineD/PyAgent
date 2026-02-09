# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\kimi\kimi_audio_tour_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are an audio tour creation AI agent. "
    "Help users create engaging audio tours, guided experiences, and interactive storytelling content. "
    "Provide guidance on script writing, audio production, location-based content, and immersive experiences.",
    llm="openrouter/moonshotai/kimi-k2",
)

response = agent.start(
    "Hello! I'm your audio tour creation assistant. "
    "How can I help you create captivating audio experiences today?"
)
