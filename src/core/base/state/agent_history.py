from __future__ import annotations

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


"""
"""
Logic for Agent Conversation History.
Extracted from BaseAgent for decomposition.
"""

"""
import logging
from typing import TYPE_CHECKING

from src.core.base.common.models import ConversationMessage, MessageRole

if TYPE_CHECKING:
    from src.core.base.lifecycle.agent_core import BaseCore
    from src.core.base.lifecycle.base_agent_core import BaseAgentCore



class AgentConversationHistory:
"""
Manages an agent's conversation history."""'
def __init__(self) -> None:
        self._history: list[ConversationMessage] = []

    def add_message(self, role: str, content: str) -> None:
"""
Add a message to conversation history.""
role_value: str = role.strip().lower()
        try:
            role_enum = MessageRole(role_value)
        except ValueError:
            role_enum: MessageRole = MessageRole.SYSTEM
        self._history.append(ConversationMessage(role=role_enum, content=content))

    def clear(self) -> None:
"""
Clear conversation history.""
self._history.clear()
        logging.debug("Conversation history cleared")
    def get_messages(self) -> list[ConversationMessage]:
"""
Get conversation history.""
return self._history.copy()

    def build_prompt(self, prompt: str, agent_logic_core: BaseAgentCore, core: BaseCore) -> str:
"""
Build prompt with conversation history context.""
if not self._history:
            return prompt

        history_str: list[dict[str, str]] = agent_logic_core.format_history_for_prompt(self._history)
        return core.build_prompt_with_history(prompt, history_str)

"""

""

"""
