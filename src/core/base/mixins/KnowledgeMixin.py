#!/usr/bin/env python3
# Knowledge Mixin for BaseAgent
from typing import Any, Optional
from pathlib import Path
from src.core.base.ShardedKnowledgeCore import ShardedKnowledgeCore

class KnowledgeMixin:
    """Handles knowledge engines, memory, and sharded storage."""
    
    def __init__(self, agent_name: str, workspace_root: Path, **kwargs: Any) -> None:
        # Knowledge Trinity initialization
        try:
            from src.core.knowledge.knowledge_engine import KnowledgeEngine
            self.knowledge = KnowledgeEngine(
                agent_id=agent_name, base_path=Path("data/agents")
            )
        except (ImportError, ModuleNotFoundError):
            self.knowledge = None

        # Memory
        try:
            from src.logic.agents.cognitive.LongTermMemory import LongTermMemory
            self.memory = LongTermMemory(agent_name=agent_name)
        except (ImportError, ModuleNotFoundError):
            self.memory = None

        self.sharded_knowledge = ShardedKnowledgeCore(base_path=Path("data/agents"))
        self._local_global_context: Any = None
        self._workspace_root = workspace_root

    @property
    def global_context(self) -> Any:
        if (
            hasattr(self, "fleet")
            and self.fleet
            and hasattr(self.fleet, "global_context")
        ):
            return self.fleet.global_context
        if self._local_global_context is None:
            try:
                from src.logic.agents.cognitive.context.engines.GlobalContextEngine import (
                    GlobalContextEngine,
                )
                self._local_global_context = GlobalContextEngine(self._workspace_root)
            except (ImportError, ValueError):
                pass
        return self._local_global_context

    @global_context.setter
    def global_context(self, value: Any) -> None:
        self._local_global_context = value
