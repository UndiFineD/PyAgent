#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

from __future__ import annotations
from typing import Any, List
from ..models import MessageRole, ConversationMessage

class ConversationHistory:
    """Manages a conversation history with message storage and retrieval."""

    def __init__(self, max_messages: int = 100) -> None:
        self.messages: List[ConversationMessage] = []
        self.max_messages = max_messages

    def add(self, role: MessageRole, content: str) -> None:
        msg = ConversationMessage(role=role, content=content)
        self.messages.append(msg)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self) -> List[ConversationMessage]:
        return self.messages.copy()

    def clear(self) -> None:
        self.messages.clear()


