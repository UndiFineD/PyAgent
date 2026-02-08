# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\guardrail_agent_example.py
from praisonaiagents import Agent


def validate_content(data):
    if len(str(data)) < 50:
        return False, "Content too short"
    return True, data


agent = Agent(instructions="You are a writer", guardrail=validate_content, max_guardrail_retries=1)

agent.start("Write a welcome message with 5 words")
