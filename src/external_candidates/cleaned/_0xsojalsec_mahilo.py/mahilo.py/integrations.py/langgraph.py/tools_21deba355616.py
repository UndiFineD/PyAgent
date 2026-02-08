# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mahilo\mahilo\integrations\langgraph\tools.py
from typing import Callable

from langchain_core.tools import tool
from mahilo.message_protocol import MessageType
from mahilo.registry import GlobalRegistry
from mahilo.tools import get_chat_with_agent_tool


def get_chat_with_agent_tool_langgraph() -> Callable:
    """Get the chat_with_agent tool that can be bound to LLMs."""

    # Create a synchronous version of the chat_with_agent tool for LangGraph
    def chat_with_agent_sync(agent_name: str, your_name: str, question: str) -> str:
        """Chat with another agent (synchronous version for LangGraph).

        Args:
            agent_name: Name of the agent to chat with
            your_name: Your agent's name
            question: The message to send

        Returns:
            A confirmation message
        """
        registry = GlobalRegistry.get_agent_registry()
        agent = registry.get_agent(agent_name)

        if not agent:
            return f"Error: Agent '{agent_name}' not found"

        # if agent is not active, activate it
        if not agent.is_active():
            agent.activate()

        # Use the synchronous version of send_message_to_agent
        registry.send_message_to_agent_sync(
            sender=your_name,
            recipient=agent_name,
            message=question,
            message_type=MessageType.DIRECT,
        )

        return f"Message sent to {agent_name}. They will process it and respond when ready."

    # Return the synchronous tool
    return tool(chat_with_agent_sync)
