# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\tools\langchain\jina-code-interpreter.py
from langchain_community.tools.riza.command import ExecPython
from praisonaiagents import Agent, PraisonAIAgents

coder_agent = Agent(
    instructions="""word = "strawberry"
                                    count = word.count("r")
                                    print(f"There are {count}'R's in the word 'Strawberry'")""",
    tools=[ExecPython],
)

agents = PraisonAIAgents(agents=[coder_agent])
agents.start()
