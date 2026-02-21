#!/usr/bin/env python3
"""Inter-agent communication core - parser-safe minimal implementation."""
from __future__ import annotations

from typing import Any, Dict, Optional, List, Callable

try:
    from .base_core import BaseCore
except Exception:
    class BaseCore:  # pragma: no cover - fallback for tests
        def __init__(self, name: str = "Base") -> None:
            self.name = name


class Message:
    """Simple message container for repair-time imports."""

    def __init__(self, content: str, sender: Optional[str] = None) -> None:
        self.content = content
        self.sender = sender


class AgentEndpoint:
    def __init__(self, url: str) -> None:
        self.url = url


class InterAgentCommunicationCore(BaseCore):
    """Small, test-friendly InterAgentCommunicationCore stub."""

    def __init__(self) -> None:
        super().__init__()
        self.registered_agents: Dict[str, AgentEndpoint] = {}
        self.active_tasks: Dict[str, Any] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self.security_schemes: Dict[str, Dict[str, Any]] = {}
        self.http_client = object()

    async def cleanup(self) -> None:
        self.http_client = None

    async def _send(self, agent_id: str, message: Message) -> None:
        if agent_id not in self.registered_agents:
            raise ValueError(f"Unknown agent: {agent_id}")
        return None

    async def stream_messages(self, target_agent_id: str, message: Message):
        if target_agent_id not in self.registered_agents:
            raise ValueError(f"Unknown agent: {target_agent_id}")
        if False:
            yield None
