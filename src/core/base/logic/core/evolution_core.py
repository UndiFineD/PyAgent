from __future__ import annotations
"""
Parser-safe EvolutionCore stub.

Provides a lightweight EvolutionCore and AgentMetadata dataclass so
other modules can import and run basic tests during repair.
"""




from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class AgentMetadata:
    name: str
    usage_count: int = 0
    success_rate: float = 0.0
    last_used: float = field(default_factory=time.time)
    tier: str = "specialized"
    parent_agents: List[str] = field(default_factory=list)
    sop_name: Optional[str] = None


class EvolutionCore:
    def __init__(self, sop_core: Optional[Any] = None) -> None:
        self.agent_pool: Dict[str, AgentMetadata] = {}
        self.sop_core = sop_core

    def record_usage(self, agent_name: str, success: bool) -> None:
        if agent_name not in self.agent_pool:
            self.agent_pool[agent_name] = AgentMetadata(name=agent_name)
        meta = self.agent_pool[agent_name]
        meta.usage_count += 1
        meta.last_used = time.time()

    def propose_integration(self, agent_a_name: str, agent_b_name: str) -> Optional[str]:
        a = self.agent_pool.get(agent_a_name)
        b = self.agent_pool.get(agent_b_name)
        if not a or not b:
            return None
        new_name = f"integrated_{agent_a_name}_{agent_b_name}"
        if new_name not in self.agent_pool:
            self.agent_pool[new_name] = AgentMetadata(name=new_name, parent_agents=[agent_a_name, agent_b_name])
        return new_name


__all__ = ["EvolutionCore", "AgentMetadata"]
