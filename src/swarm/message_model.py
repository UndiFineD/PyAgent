#!/usr/bin/env python3
"""Message model for PyAgent."""
from pydantic import BaseModel


class Message(BaseModel):
    """Data model for a message in the swarm system."""
    id: str
    timestamp: str
    type: str
    priority: str
    source: str
    destination: str
    payload: dict
    checksum: str


def validate_message(data: dict) -> bool:
    """Validate that the given data conforms to the Message schema."""
    Message(**data)
    return True
