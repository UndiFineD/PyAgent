"""
Parser-safe AutonomyCore facade stub.

Minimal placeholder used while the real autonomy core is repaired.
"""
from __future__ import annotations




from typing import Any


class StandardAutonomyCore:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


class AutonomyCore(StandardAutonomyCore):
"""
Compatibility facade around the real Autonomy core.

    This stub exposes the same class name so imports succeed during tests.
"""
def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


__all__ = ["AutonomyCore", "StandardAutonomyCore"]