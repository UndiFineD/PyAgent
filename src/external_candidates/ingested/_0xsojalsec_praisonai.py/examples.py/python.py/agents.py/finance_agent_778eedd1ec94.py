# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\agents\finance-agent.py
from praisonaiagents import Agent, Tools
from praisonaiagents.tools import get_historical_data, get_stock_info, get_stock_price

agent = Agent(
    instructions="You are a Research Agent",
    tools=[get_stock_price, get_stock_info, get_historical_data],
)
agent.start(
    "Understand current stock price and historical data of Apple and Google. Tell me if I can invest in them"
)
