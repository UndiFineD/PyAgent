# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\models\anthropic\async_basic_stream.py
"""
Basic streaming async example using Claude.
"""

import asyncio

from agno.agent import Agent
from agno.models.anthropic import Claude

agent = Agent(
    model=Claude(id="claude-3-5-sonnet-20240620"),
    markdown=True,
)

asyncio.run(agent.aprint_response("Share a 2 sentence horror story", stream=True))
