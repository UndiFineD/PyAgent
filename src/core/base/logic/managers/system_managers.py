"""
System Managers for PyAgent.
(Facade for src.core.base.common.*_core)
"""

from __future__ import annotations
from src.core.base.common.priority_core import PriorityCore as FilePriorityManager
from src.core.base.common.cache_core import CacheCore as ResponseCache
from src.core.base.common.health_core import HealthCore as HealthChecker
from src.core.base.common.profile_core import ProfileCore as ProfileManager

from dataclasses import dataclass, field
from typing import Any, Callable
from src.core.base.common.models import AgentEvent, _empty_agent_event_handlers

@dataclass
class EventManager:
    """Manages agent events. (Facade)"""
    handlers: dict[AgentEvent, list[Callable[..., None]]] = field(
        default_factory=_empty_agent_event_handlers
    )

    def on(self, event: AgentEvent, handler: Callable[..., None]) -> None:
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)

    def emit(self, event: AgentEvent, data: Any = None) -> None:
        if event in self.handlers:
            for handler in self.handlers[event]:
                if data is not None:
                    handler(data)
                else:
                    handler()

@dataclass
class StatePersistence:
    """Persists agent state. (Facade)"""
    state_file: Any
    backup: bool = False
    backup_count: int = 0
    def save(self, state: dict[str, Any]) -> None: pass
    def load(self, default: dict[str, Any] | None = None) -> dict[str, Any]: return default or {}

