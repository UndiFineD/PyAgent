# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\cohere\async_basic_stream.py
"""
Basic streaming async example using Cohere.
"""

import asyncio

from agno.agent import Agent
from agno.models.cohere import Cohere

agent = Agent(
    model=Cohere(id="command-a-03-2025"),
    markdown=True,
)

asyncio.run(agent.aprint_response("Share a 2 sentence horror story", stream=True))
