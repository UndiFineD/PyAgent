#!/usr/bin/env python
"""Tests for the MCP tools."""
import importlib
from typing import Callable, cast, get_type_hints


def _load_send_message_tool() -> Callable[..., object]:
    """Load send_message_tool dynamically to avoid requiring import stubs for chat.mcp_tools."""
    mcp_module = importlib.import_module("chat.mcp_tools")
    return cast(Callable[..., object], mcp_module.send_message_tool)


def test_mcp_tool_signature() -> None:
    """The send_message_tool should have the correct name and type hints."""
    send_message_tool = _load_send_message_tool()
    assert send_message_tool.__name__ == "send_chat_message"
    hints = get_type_hints(send_message_tool)
    assert "room" in hints
    assert hints["room"] is str
