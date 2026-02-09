# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\tools\langchain\azure-code-interpreter.py
import getpass

from langchain_azure_dynamic_sessions import SessionsPythonREPLTool
from praisonaiagents import Agent, PraisonAIAgents

POOL_MANAGEMENT_ENDPOINT = getpass.getpass()

coder_agent = Agent(
    instructions="""word = "strawberry"
                                    count = word.count("r")
                                    print(f"There are {count}'R's in the word 'Strawberry'")""",
    tools=[SessionsPythonREPLTool],
)

agents = PraisonAIAgents(agents=[coder_agent])
agents.start()
