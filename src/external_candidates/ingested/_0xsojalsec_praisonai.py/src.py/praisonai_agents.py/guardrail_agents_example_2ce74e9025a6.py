# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\guardrail_agents_example.py
from typing import Any, Tuple

from praisonaiagents import Agent, PraisonAIAgents, Task, TaskOutput


def validate_content(task_output: TaskOutput) -> Tuple[bool, Any]:
    if len(task_output.raw) < 50:
        return False, "Content too short"
    return True, task_output


agent = Agent(
    instructions="You are a writer",
)

task = Task(
    description="Write a welcome message", guardrail=validate_content, agent=agent
)

praison_agents = PraisonAIAgents(agents=[agent], tasks=[task])

praison_agents.start()
