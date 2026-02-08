# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\kimi\kimi_quantum_ai_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a quantum AI agent. "
    "Help users understand quantum artificial intelligence, "
    "quantum machine learning, and quantum neural networks. "
    "Provide guidance on quantum algorithms for AI, "
    "quantum optimization, and hybrid quantum-classical systems.",
    llm="openrouter/moonshotai/kimi-k2",
)

response = agent.start(
    "Hello! I'm your quantum AI assistant. How can I help you explore quantum artificial intelligence today?"
)
