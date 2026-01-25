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

"""
Events.py module.
"""

import logging
from typing import Any, Callable, Dict, List, Optional

from src.core.base.common.models import ConversationMessage, EventType

logger = logging.getLogger(__name__)


class EventCore:
    """Core logic for event handling and history formatting."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def trigger_event(
        self, event: EventType, data: dict[str, Any], hooks: list[Callable[[dict[str, Any]], None]]
    ) -> None:
        """Trigger an event and invoke provided hooks."""
        for callback in hooks:
            try:
                callback(data)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning(f"Hook error for {event.value}: {e}")

    def filter_events(self, events: List[Dict[str, Any]], event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Filter events based on type."""
        if not event_type:
            return events
        return [e for e in events if e.get("type") == event_type]

    def format_history_for_prompt(self, history: list[ConversationMessage]) -> list[dict[str, str]]:
        """Converts internal history objects to dicts for backend consumption."""
        return [{"role": m.role.value, "content": m.content} for m in history]

    def build_prompt_with_history(self, prompt: str, history: list[ConversationMessage], system_prompt: str) -> str:
        """Logic to assemble the full prompt string."""
        full_prompt = f"System: {system_prompt}\n\n"
        for msg in history:
            full_prompt += f"{msg.role.name}: {msg.content}\n"
        full_prompt += f"User: {prompt}\n"
        return full_prompt
