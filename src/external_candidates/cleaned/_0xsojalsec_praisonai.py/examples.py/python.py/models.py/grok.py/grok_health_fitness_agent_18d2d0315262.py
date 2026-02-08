# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\grok\grok_health_fitness_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a health and fitness AI agent. Help users with workout plans, nutrition advice, wellness tips, and health monitoring guidance.",
    llm="xai/grok-4",
)

response = agent.start("I want to lose 20 pounds and build muscle. What's the best workout and nutrition plan for me?")
