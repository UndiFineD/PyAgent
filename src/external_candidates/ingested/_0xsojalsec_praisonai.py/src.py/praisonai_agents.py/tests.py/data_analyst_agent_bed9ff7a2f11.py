# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\data-analyst-agent.py
import os

from praisonaiagents import Agent, Tools
from praisonaiagents.tools import (
    filter_data,
    get_summary,
    group_by,
    pivot_table,
    read_csv,
    read_excel,
    write_csv,
    write_excel,
)

agent = Agent(
    instructions="You are a Data Analyst Agent",
    tools=[
        read_csv,
        read_excel,
        write_csv,
        write_excel,
        filter_data,
        get_summary,
        group_by,
        pivot_table,
    ],
)
agent.start(f"""
    Read the data from the csv file {os.path.join(os.path.dirname(__file__), "tesla-stock-price.csv")}
    Analyse the data and give me the insights
    read_csv to read the file
""")
