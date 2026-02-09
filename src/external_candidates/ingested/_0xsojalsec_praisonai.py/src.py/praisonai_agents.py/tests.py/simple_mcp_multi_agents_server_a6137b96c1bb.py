# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\simple-mcp-multi-agents-server.py
from duckduckgo_search import DDGS
from praisonaiagents import Agent, Agents


def internet_search_tool(query: str):
    results = []
    ddgs = DDGS()
    for result in ddgs.text(keywords=query, max_results=5):
        results.append(
            {
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", ""),
            }
        )
    return results


agent = Agent(
    name="SearchAgent",
    instructions="You Search the internet for information",
    tools=[internet_search_tool],
)
agent2 = Agent(name="SummariseAgent", instructions="You Summarise the information")

agents = Agents(name="MultiAgents", agents=[agent, agent2])
agents.launch(port=8080, protocol="mcp")
