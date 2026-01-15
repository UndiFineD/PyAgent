#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Access control for stats.

from __future__ import annotations
import fnmatch




class StatsAccessController:
    """Controls access to stats."""
    def __init__(self) -> None:
        self.permissions: dict[str, dict[str, str]] = {}

    def grant(self, user: str, pattern: str, level: str = "read") -> None:
        self.permissions.setdefault(user, {})[pattern] = level

    def can_access(self, user: str, resource: str, required_level: str = "read") -> bool:
        if user not in self.permissions: return False
        req = required_level.lower()
        for pat, granted in self.permissions[user].items():
            if fnmatch.fnmatch(resource, pat):
                g = granted.lower()
                if req == "read" and g in ("read", "write"): return True
                if req == "write" and g == "write": return True
        return False
