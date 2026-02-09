# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\mistral\async_basic_stream.py
"""
Basic streaming async example using Mistral.
"""

import asyncio

from agno.agent import Agent
from agno.models.mistral.mistral import MistralChat

agent = Agent(
    model=MistralChat(id="mistral-large-latest"),
    markdown=True,
)

asyncio.run(agent.aprint_response("Share a 2 sentence horror story", stream=True))
