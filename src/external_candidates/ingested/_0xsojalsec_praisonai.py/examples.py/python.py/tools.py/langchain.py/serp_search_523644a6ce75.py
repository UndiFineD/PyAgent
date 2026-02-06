# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\tools\langchain\serp-search.py
from langchain_community.utilities import SerpAPIWrapper
from praisonaiagents import Agent, PraisonAIAgents

data_agent = Agent(
    instructions="Search about decline of recruitment across various industries with the rise of AI",
    tools=[SerpAPIWrapper],
)
editor_agent = Agent(
    instructions="Write a blog article pointing out the jobs most at rish due to the rise of AI"
)
agents = PraisonAIAgents(agents=[data_agent, editor_agent])
agents.start()
