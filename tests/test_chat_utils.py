#!/usr/bin/env python
"""Tests for chat utilities."""
import importlib
from collections.abc import Callable, Sequence
from typing import Protocol, cast


class ChatRoomLike(Protocol):
    """Protocol for room objects returned by create_personal_room."""

    name: str
    participants: Sequence[str]


def _load_chat_symbols() -> tuple[type[object], Callable[[str], ChatRoomLike]]:
    """Dynamically load chat symbols without requiring mypy stubs for chat package modules."""
    utils_module = importlib.import_module("chat.utils")
    models_module = importlib.import_module("chat.models")
    room_type = cast(type[object], models_module.ChatRoom)
    create_room = cast(Callable[[str], ChatRoomLike], utils_module.create_personal_room)
    return room_type, create_room


def test_personal_room_creation() -> None:
    """create_personal_room should create a ChatRoom with the correct name and participants."""
    chat_room_type, create_personal_room = _load_chat_symbols()
    room = create_personal_room("alice")
    assert isinstance(room, chat_room_type)
    assert room.name == "personal-alice"
    # should include the user and an agent identifier
    assert "alice" in room.participants
    assert any(p.startswith("agent-") for p in room.participants)
