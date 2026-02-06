# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\agent_concepts\other\input_as_messages_list.py
from agno.agent import Agent, Message

Agent().print_response(
    messages=[
        Message(
            role="user",
            content=[
                {"type": "text", "text": "Hi! My name is John."},
            ],
        ),
        Message(
            role="user",
            content=[
                {"type": "text", "text": "What are you capable of?"},
            ],
        ),
    ],
    stream=True,
    markdown=True,
)
