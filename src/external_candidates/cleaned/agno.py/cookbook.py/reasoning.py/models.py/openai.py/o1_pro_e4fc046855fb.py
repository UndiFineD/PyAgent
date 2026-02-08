# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\reasoning\models\openai\o1_pro.py
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

agent = Agent(model=OpenAIResponses(id="o1-pro"))
agent.print_response(
    "Solve the trolley problem. Evaluate multiple ethical frameworks. Include an ASCII diagram of your solution.",
    stream=True,
)
