"""
Parser-safe ErrorMappingCore stub.

Provides a minimal ErrorMappingCore class as a safe import target while
the complete implementation is being restored.
"""
from __future__ import annotations




from typing import Any, Dict


class ErrorMappingCore:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.mappings: Dict[str, str] = {}

    def register_mapping(self, key: str, description: str) -> None:
        self.mappings[key] = description

    def lookup(self, key: str) -> str | None:
        return self.mappings.get(key)


__all__ = ["ErrorMappingCore"]