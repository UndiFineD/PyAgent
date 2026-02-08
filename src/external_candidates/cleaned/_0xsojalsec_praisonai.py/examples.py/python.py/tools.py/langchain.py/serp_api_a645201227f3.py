# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\tools\langchain\serp-api.py
# pip install langchain-community google-search-results
# export SERPAPI_API_KEY=your_api_key_here
# export OPENAI_API_KEY=your_api_key_here

from langchain_community.utilities import SerpAPIWrapper
from praisonaiagents import Agent, PraisonAIAgents

data_agent = Agent(instructions="Search about AI job trends in 2025", tools=[SerpAPIWrapper])
editor_agent = Agent(instructions="Write a blog article")

agents = PraisonAIAgents(agents=[data_agent, editor_agent])
agents.start()
