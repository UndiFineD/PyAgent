# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\gemini-structured.py
from praisonaiagents import Agent, Agents, Task
from pydantic import BaseModel


class Recipe(BaseModel):
    recipe_name: str
    ingredients: list[str]


agent = Agent(name="Chef", role="Recipe Creator", llm="gemini/gemini-2.5-flash")

task = Task(
    description="Create a cookie recipe",
    agent=agent,
    output_pydantic=Recipe,  # Will use Gemini's native structured output!
)

agents = Agents(agents=[agent], tasks=[task])

agents.start()
