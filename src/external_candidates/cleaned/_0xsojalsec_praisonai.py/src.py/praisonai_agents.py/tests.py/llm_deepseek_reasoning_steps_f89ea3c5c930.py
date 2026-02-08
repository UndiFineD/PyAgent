# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\llm-deepseek-reasoning-steps.py
from praisonaiagents import Agent, PraisonAIAgents, Task

reasoning_agent = Agent(role="Helpful Assistant", reasoning_steps=True, llm="deepseek/deepseek-reasoner")
small_agent = Agent(role="Helpful Assistant", llm="openai/gpt-3.5-turbo")

reasoning_task = Task(description="How many r's in the word 'Strawberry'?", agent=reasoning_agent)
small_task = Task(
    description="With the provided reasoning tell me how many r's in the word 'Strawberry'?",
    agent=small_agent,
)

agents = PraisonAIAgents(agents=[reasoning_agent, small_agent], tasks=[reasoning_task, small_task])

agents.start()
