from typing import get_type_hints

from chat.mcp_tools import send_message_tool


def test_mcp_tool_signature():
    """The send_message_tool should have the correct name and type hints."""
    assert send_message_tool.__name__ == "send_chat_message"
    hints = get_type_hints(send_message_tool)
    assert "room" in hints
    assert hints["room"] == str
