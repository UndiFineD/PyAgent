# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\models\llama\llama_data_science_agent.py
from praisonaiagents import Agent

agent = Agent(
    instructions="You are a data science AI agent. "
    "Help users with data analysis, machine learning model development, "
    "statistical analysis, and data visualization. Provide guidance on "
    "data preprocessing, feature engineering, model selection, and evaluation.",
    llm="meta-llama/Llama-3.1-8B-Instruct",
)

response = agent.start(
    "Hello! I'm your data science assistant. "
    "How can I help you with your data analysis and machine learning projects today?"
)
