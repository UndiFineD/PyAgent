# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_multimodal_coding_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a multimodal coding AI agent. "
    "Help users with code generation, review, and debugging "
    "by analyzing both text and visual inputs like screenshots and diagrams.",
    llm="xai/grok-4",
)

response = agent.start(
    "I have a screenshot of a UI design and need to generate the corresponding HTML/CSS code. "
    "Can you help me create the frontend code?"
)
