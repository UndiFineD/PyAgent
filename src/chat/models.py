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

from __future__ import annotations

from typing import Any, Dict, List, Optional


class ChatRoom:
    """Lightweight in-memory chat room for humans and agents.

    The class is intentionally simple during initial development; persistence,
    permissions and agent hooks will be added later according to the
    implementation plan.
    """

    def __init__(self, name: str, participants: Optional[List[str]] = None) -> None:
        self.name = name
        # participants may include human user ids and agent identifiers
        self.participants = participants or []
        # internal message history list; each entry is a dict with sender/text
        self._messages: List[Dict[str, Any]] = []

    def post(self, sender: str, text: str) -> None:
        """Append a message from *sender* with the given *text* to history."""
        # In the simplest form we don't validate sender membership yet
        self._messages.append({"sender": sender, "text": text})

    def history(self) -> List[Dict[str, Any]]:
        """Return a copy of the chat history."""
        # return a shallow copy so callers can't mutate internal list
        return list(self._messages)
