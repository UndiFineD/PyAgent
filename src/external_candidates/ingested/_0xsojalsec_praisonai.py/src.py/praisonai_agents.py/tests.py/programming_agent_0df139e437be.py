# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\programming-agent.py
from praisonaiagents import Agent, Tools
from praisonaiagents.tools import duckduckgo  # Web Search Tool
from praisonaiagents.tools import (  # Code Tools; Shell Tools
    analyze_code,
    disassemble_code,
    execute_code,
    execute_command,
    format_code,
    get_system_info,
    kill_process,
    lint_code,
    list_processes,
)

agent = Agent(
    instructions="You are a Programming Agent",
    self_reflect=True,
    min_reflect=5,
    max_reflect=10,
    tools=[
        execute_code,
        analyze_code,
        format_code,
        lint_code,
        disassemble_code,
        execute_command,
        list_processes,
        kill_process,
        get_system_info,
        duckduckgo,
    ],
)
agent.start(
    "Write a python script using yfinance to find the stock price of Tesla"
    "First check if required packages are installed"
    "Run it using execute_code"
    "execute_command if you want to run any terminal command"
    "search internet using duckduckgo if you want to know update python package information"
    "Analyse the output using analyze_code and fix error if required"
    "if no package is installed, install it"
    "then run the code"
)
