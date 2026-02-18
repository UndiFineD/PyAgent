#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Core logic for conversation history and message management.
"""


from __future__ import annotations


try:
    from typing import List
except ImportError:
    from typing import List


try:
    from .base_core import BaseCore
except ImportError:
    from .base_core import BaseCore

try:
    from .models import ConversationMessage, MessageRole
except ImportError:
    from .models import ConversationMessage, MessageRole




class ConversationCore(BaseCore):
    """Authoritative engine for conversation state.
    """
    def __init__(self, max_messages: int = 100) -> None:
        super().__init__()
        self.messages: List[ConversationMessage] = []
        self.max_messages = max_messages

    def add_message(self, role: MessageRole, content: str) -> None:
        """Add a new message to the conversation history."""msg = ConversationMessage(role=role, content=content)
        self.messages.append(msg)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

    def get_history(self) -> List[ConversationMessage]:
        """Return a copy of the conversation history."""return self.messages.copy()

    def clear(self) -> None:
        """Clear the conversation history."""self.messages.clear()
