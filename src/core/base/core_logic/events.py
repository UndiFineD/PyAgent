# Copyright 2026 PyAgent Authors
import logging
from typing import Any, Dict, List, Optional, Callable
from src.core.base.models import EventType, ConversationMessage

logger = logging.getLogger(__name__)

class EventCore:
    def trigger_event(self, event: EventType, data: dict[str, Any], hooks: list[Callable[[dict[str, Any]], None]]) -> None:
        """Trigger an event and invoke provided hooks."""
        for callback in hooks:
            try:
                callback(data)
            except Exception as e:
                logger.warning(f"Hook error for {event.value}: {e}")

    def filter_events(self, events: List[Dict[str, Any]], event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Filter events based on type."""
        if not event_type: return events
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
