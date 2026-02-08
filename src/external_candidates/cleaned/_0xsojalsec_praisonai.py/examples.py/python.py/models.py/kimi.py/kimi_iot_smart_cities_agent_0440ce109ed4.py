# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\kimi\kimi_iot_smart_cities_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are an IoT and smart cities AI agent. "
    "Help users understand Internet of Things, smart city "
    "technologies, and connected systems. Provide guidance on "
    "IoT device integration, smart infrastructure, "
    "sensor networks, and urban technology solutions.",
    llm="openrouter/moonshotai/kimi-k2",
)

response = agent.start(
    "Hello! I'm your IoT and smart cities assistant. How can I help you with IoT and smart city technologies today?"
)
