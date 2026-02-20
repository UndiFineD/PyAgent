#!/usr/bin/env python3
""
Minimal, parser-safe Swarm Orchestrator Core used for tests.""
from dataclasses import dataclass, field
from typing import Dict, Any, List


class DelegationMode:
    ROUND_ROBIN = "round_robin"
    BROADCAST = "broadcast"


@dataclass
class SwarmMember:
    member_id: str
    status: str = "idle"
    metadata: Dict[str, Any] = field(default_factory=dict)


class SwarmOrchestratorCore:
    def __init__(self):
        self.members: Dict[str, SwarmMember] = {}

    def register_member(self, member: SwarmMember) -> None:
        self.members[member.member_id] = member

    def delegate(self, mode: str, task: Any) -> List[str]:
        if mode == DelegationMode.BROADCAST:
            return list(self.members.keys())
        return []
