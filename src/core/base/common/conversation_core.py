#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

<<<<<<< HEAD

from __future__ import annotations
from src.core.base.version import VERSION
from typing import List
from src.core.base.models import MessageRole, ConversationMessage

__version__ = VERSION

class ConversationHistory:
    """Manages a conversation history with message storage and retrieval."""

    def __init__(self, max_messages: int = 100) -> None:
        self.messages: list[ConversationMessage] = []
        self.max_messages = max_messages

    def add(self, role: MessageRole, content: str) -> None:
=======
"""
Core logic for conversation history and message management.
"""

from __future__ import annotations
from typing import List, Optional
from .base_core import BaseCore
from .models import MessageRole, ConversationMessage

class ConversationCore(BaseCore):
    """
    Authoritative engine for conversation state.
    """
    def __init__(self, max_messages: int = 100) -> None:
        super().__init__()
        self.messages: List[ConversationMessage] = []
        self.max_messages = max_messages

    def add_message(self, role: MessageRole, content: str) -> None:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        msg = ConversationMessage(role=role, content=content)
        self.messages.append(msg)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

<<<<<<< HEAD
    def get_context(self) -> list[ConversationMessage]:
=======
    def get_history(self) -> List[ConversationMessage]:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return self.messages.copy()

    def clear(self) -> None:
        self.messages.clear()
