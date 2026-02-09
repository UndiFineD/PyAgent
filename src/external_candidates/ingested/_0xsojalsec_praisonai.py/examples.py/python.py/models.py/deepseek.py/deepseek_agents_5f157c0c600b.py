# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\deepseek\deepseek-agents.py
# pip install praisonaiagents
# export OPENAI_BASE_URL=http://localhost:11434/v1
# ollama pull deepseek-r1

from praisonaiagents import Agent

agent = Agent(instructions="You are helpful Assisant", llm="deepseek-r1")

agent.start("Why sky is Blue?")
