# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\tools\langchain\bearly-code-interpreter.py
from langchain_community.tools import BearlyInterpreterTool
from praisonaiagents import Agent, PraisonAIAgents

coder_agent = Agent(
    instructions="""for i in range(0,10):
                                        print(f'The number is {i}')""",
    tools=[BearlyInterpreterTool],
)

agents = PraisonAIAgents(agents=[coder_agent])
agents.start()
