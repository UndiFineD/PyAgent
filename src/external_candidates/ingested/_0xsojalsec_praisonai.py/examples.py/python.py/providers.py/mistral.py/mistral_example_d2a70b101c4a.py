# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\examples\python\providers\mistral\mistral_example.py
"""
Basic example of using Mistral with PraisonAI
"""

from praisonaiagents import Agent

# Initialize Agent with Mistral
agent = Agent(
    instructions="You are a helpful assistant",
    llm="mistral/mistral-large-latest",
)

# Example conversation
response = agent.start("Why sky is Blue?")

# Example with language translation
translation_task = """
Translate the following text to French and explain any cultural nuances:
"The early bird catches the worm, but the second mouse gets the cheese."
"""

response = agent.start(translation_task)

# Example with creative content generation
creative_task = """
Write a haiku about artificial intelligence and its impact on society.
Then explain the symbolism in your haiku.
"""

response = agent.start(creative_task)
