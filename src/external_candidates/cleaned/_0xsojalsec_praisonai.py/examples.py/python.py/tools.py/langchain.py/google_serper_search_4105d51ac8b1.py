# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\tools\langchain\google-serper-search.py
import os

from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
from praisonaiagents import Agent, PraisonAIAgents

load_dotenv()

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

search = GoogleSerperAPIWrapper()

data_agent = Agent(
    instructions="Suggest me top 5 most visited websites for Dosa Recipe",
    tools=[search],
)
editor_agent = Agent(instructions="List out the websites with their url and a short description")
agents = PraisonAIAgents(agents=[data_agent, editor_agent])
agents.start()
