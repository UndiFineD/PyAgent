# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\wikipedia-agent.py
from praisonaiagents import Agent, PraisonAIAgents, Task
from praisonaiagents.tools import (
    wiki_language,
    wiki_page,
    wiki_random,
    wiki_search,
    wiki_summary,
)

agent = Agent(
    instructions="You are a Wikipedia Agent",
    tools=[wiki_search, wiki_summary, wiki_page, wiki_random, wiki_language],
    self_reflect=True,
    min_reflect=3,
    max_reflect=5,
    llm="gpt-5-nano",
)
agent.start(
    "What is the history of AI?"
    "First search the history of AI"
    "Read the page of the history of AI"
    "Get the summary of the page"
)
