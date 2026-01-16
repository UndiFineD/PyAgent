#!/usr/bin/env python3
# Persistence Mixin for BaseAgent
from typing import Any, List
from src.core.base.models import AgentState, EventType
from src.core.base.AgentHistory import AgentConversationHistory
from src.core.base.AgentScratchpad import AgentScratchpad

class PersistenceMixin:
    """Handles agent state, history, scratchpad, and events."""
    
    def __init__(self, **kwargs: Any) -> None:
        self._state: AgentState = AgentState.INITIALIZED
        self._history_manager = AgentConversationHistory()
        self._scratchpad_manager = AgentScratchpad()
        self._webhooks: List[str] = []
        self._event_hooks: dict[EventType, list[Any]] = {}

    @property
    def state(self) -> AgentState:
        return self._state

    def register_webhook(self, url: str) -> None:
        """Registers a webhook URL for notifications."""
        if url not in self._webhooks:
            self._webhooks.append(url)

    def _trigger_event(self, event_type: EventType, data: dict[str, Any]) -> None:
        """Triggers local events and hooks."""
        hooks = self._event_hooks.get(event_type, [])
        for hook in hooks:
            try:
                hook(data)
            except Exception:
                pass
