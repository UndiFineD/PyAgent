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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Conversation turn tracking logic.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from .models import ContextConfig, ConversationTurn, TokenMetrics, TurnType


class TurnTracker:
    """Track conversation turns and token usage."""

    def __init__(self, config: Optional[ContextConfig] = None):
        self.config = config or ContextConfig()
        self._turns: List[ConversationTurn] = []
        self._total_tokens = TokenMetrics()
        self._turn_index: Dict[str, ConversationTurn] = {}

    @property
    def turns(self) -> List[ConversationTurn]:
        """Return the list of conversation turns."""
        return self._turns

    @property
    def turn_count(self) -> int:
        """Return the total number of turns."""
        return len(self._turns)

    @property
    def total_tokens(self) -> TokenMetrics:
        """Return the total token metrics for all turns."""
        return self._total_tokens

    def add_turn(
        self,
        turn_type: TurnType,
        content: Any,
        tokens: Optional[TokenMetrics] = None,
        parent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversationTurn:
        """Add a turn to the conversation."""
        turn_id = f"turn_{uuid.uuid4().hex[:12]}"

        turn = ConversationTurn(
            id=turn_id,
            type=turn_type,
            content=content,
            tokens=tokens,
            parent_id=parent_id,
            metadata=metadata or {},
        )

        self.append_turn(turn)

        return turn

    def append_turn(self, turn: ConversationTurn) -> None:
        """Append an existing turn to the conversation."""
        self._turns.append(turn)
        self._turn_index[turn.id] = turn

        if turn.tokens:
            self._total_tokens = self._total_tokens.add(turn.tokens)

        # Link to parent
        if turn.parent_id and turn.parent_id in self._turn_index:
            self._turn_index[turn.parent_id].child_ids.append(turn.id)

    def get_turn(self, turn_id: str) -> Optional[ConversationTurn]:
        """Get turn by ID."""
        return self._turn_index.get(turn_id)

    def get_messages(
        self,
        include_system: bool = True,
        include_reasoning: bool = False,
    ) -> List[Dict[str, Any]]:
        """Get turns as messages."""
        messages = []
        for turn in self._turns:
            if turn.type == TurnType.SYSTEM and not include_system:
                continue
            if turn.type == TurnType.REASONING and not include_reasoning:
                continue
            messages.append(turn.to_message())
        return messages

    def get_recent(self, n: int) -> List[ConversationTurn]:
        """Get n most recent turns."""
        return self._turns[-n:]

    def clear(self) -> None:
        """Clear all turns."""
        self._turns.clear()
        self._turn_index.clear()
        self._total_tokens = TokenMetrics()

    def truncate(self, max_turns: Optional[int] = None) -> int:
        """Truncate old turns."""
        limit = max_turns or self.config.max_turns
        if len(self._turns) <= limit:
            return 0

        removed = len(self._turns) - limit
        old_turns = self._turns[:removed]
        self._turns = self._turns[removed:]

        # Update index
        for turn in old_turns:
            self._turn_index.pop(turn.id, None)

        return removed
