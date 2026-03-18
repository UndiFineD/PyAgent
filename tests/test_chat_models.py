#!/usr/bin/env python
"""Tests for chat models."""

from chat.models import ChatRoom


def test_room_post_and_history() -> None:
    """Posting a message to a ChatRoom should make it appear in the history."""
    room = ChatRoom("project-x", ["alice", "agent-1"])
    assert room.history() == []
    room.post("alice", "hello")
    assert room.history()[0]["sender"] == "alice"
    assert room.history()[0]["text"] == "hello"
