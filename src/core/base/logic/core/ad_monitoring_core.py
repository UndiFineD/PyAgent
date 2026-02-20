#!/usr/bin/env python3
"""Minimal AD monitoring core for tests."""

try:
    from __future__ import annotations
except ImportError:
    from __future__ import annotations


try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum
except ImportError:
    from enum import Enum

try:
    from typing import List, Dict, Any
except ImportError:
    from typing import List, Dict, Any



class ChangeType(Enum):
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"


class AttributeChangeType(Enum):
    ADDED = "added"
    MODIFIED = "modified"
    REMOVED = "removed"


class SecurityEventType(Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    ALERT = "alert"


@dataclass
class ADObjectChange:
    dn: str
    change_type: ChangeType


@dataclass
class AttributeChange:
    attribute: str
    change_type: AttributeChangeType


@dataclass
class MonitoringSession:
    session_id: str


@dataclass
class MonitoringConfig:
    polling_interval: int = 60


class ADConnectionProvider:
    pass


class AlertProvider:
    pass


class ADMonitoringCore:
    async def monitor(self) -> List[ADObjectChange]:
        return []
