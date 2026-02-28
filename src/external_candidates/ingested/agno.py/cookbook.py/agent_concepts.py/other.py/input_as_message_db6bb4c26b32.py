# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\agent_concepts\other\input_as_message.py
from agno.agent import Agent, Message

Agent().print_response(
    Message(
        role="user",
        content=[
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                },
            },
        ],
    ),
    stream=True,
    markdown=True,
)
