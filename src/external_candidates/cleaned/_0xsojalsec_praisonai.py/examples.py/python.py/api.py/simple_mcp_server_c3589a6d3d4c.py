# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\api\simple-mcp-server.py
from praisonaiagents import Agent

agent = Agent(name="TweetAgent", instructions="Create a Tweet based on the topic provided")
agent.launch(port=8080, protocol="mcp")
