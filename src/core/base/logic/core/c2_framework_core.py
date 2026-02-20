#!/usr/bin/env python3
from __future__ import annotations
"""
Minimal C2 framework core used by tests.

Provides lightweight enums and dataclasses matching test imports.
"""




from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class CommunicationProtocol(Enum):
    HTTP = "http"
    HTTPS = "https"
    SMB = "smb"
    TCP = "tcp"
    MTLS = "mtls"
    DNS = "dns"
    ICMP = "icmp"


class AgentStatus(Enum):
    ACTIVE = "active"
    SLEEPING = "sleeping"
    DEAD = "dead"
    CHECKING_IN = "checking_in"
    EXECUTING = "executing"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ListenerType(Enum):
    BEACON = "beacon"
    GOPHER = "gopher"
    REVERSE_TCP = "reverse_tcp"
    BIND_TCP = "bind_tcp"


@dataclass
class C2Profile:
    name: str
    port: int
    endpoint: str
    password_hash: str
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    extenders: List[str] = field(default_factory=list)
    server_response: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class C2Agent:
    agent_id: str
    name: str
    hostname: str
    username: str
    domain: str
    os: str
    architecture: str
    internal_ip: str
    external_ip: str
    listener_id: str
    protocol: CommunicationProtocol
    status: AgentStatus = AgentStatus.ACTIVE


@dataclass
class C2Listener:
    listener_id: str
    name: str
    listener_type: ListenerType
    protocol: CommunicationProtocol
    host: str
    port: int
    endpoint: str
    status: str = "stopped"
    agents_connected: int = 0


@dataclass
class C2Task:
    task_id: str
    agent_id: str
    command: str
    args: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING


@dataclass
class C2Extender:
    name: str
    extender_type: str
    path: str
    config: Dict[str, Any] = field(default_factory=dict)
    loaded: bool = False


@dataclass
class C2Session:
    session_id: str
    username: str
    connected_at: datetime = field(default_factory=datetime.now)


@dataclass
class C2Tunnel:
    tunnel_id: str
    agent_id: str
    tunnel_type: str
    local_host: str
    local_port: int
    remote_host: str
    remote_port: int
    status: str = "active"


@dataclass
class C2Framework:
    profile: C2Profile
    agents: Dict[str, C2Agent] = field(default_factory=dict)
    listeners: Dict[str, C2Listener] = field(default_factory=dict)
    tasks: Dict[str, C2Task] = field(default_factory=dict)


class C2FrameworkCore:
    ""
Minimal core with basic async lifecycle methods.""
def __init__(self) -> None:
        self.framework: Optional[C2Framework] = None
        self.running = False

    async def initialize(self, profile_config: Dict[str, Any]) -> bool:
        try:
            profile = C2Profile(
                name=profile_config.get("name", "default"),
                port=profile_config.get("port", 8080),
                endpoint=profile_config.get("endpoint", "/"),
                password_hash=profile_config.get("password", ""),
            )
            self.framework = C2Framework(profile=profile)
            return True
        except Exception:
            return False

    async def start_framework(self) -> bool:
        if not self.framework:
            return False
        self.running = True
        return True

    async def stop_framework(self) -> None:
        self.running = False


__all__ = [
    "CommunicationProtocol",
    "AgentStatus",
    "TaskStatus",
    "ListenerType",
    "C2Profile",
    "C2Agent",
    "C2Listener",
    "C2Task",
    "C2Extender",
    "C2Session",
    "C2Tunnel",
    "C2Framework",
    "C2FrameworkCore",
]
