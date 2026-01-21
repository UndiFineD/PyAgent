# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from typing import Any
from datetime import datetime

class CoreResolutionMixin:
    """Methods for conflict resolution and fact preparation."""

    def prepare_fact(self, key: str, value: Any) -> dict[str, Any]:
        """Prepares a fact entry with timestamp."""
        return {"value": value, "updated_at": datetime.now().isoformat()}

    def prepare_insight(self, insight: str, source_agent: str) -> dict[str, Any]:
        """Prepares an insight entry."""
        return {
            "text": insight,
            "source": source_agent,
            "timestamp": datetime.now().isoformat(),
        }

    def merge_entity_info(
        self, existing: dict[str, Any], new_attributes: dict[str, Any]
    ) -> dict[str, Any]:
        """Merges new attributes into an entity record."""
        updated = existing.copy()
        updated.update(new_attributes)
        updated["last_modified"] = datetime.now().isoformat()
        return updated

    def resolve_conflict(
        self, existing: Any, incoming: Any, strategy: str = "latest"
    ) -> Any:
        """Logic to resolve conflicts when multiple agents update the same key."""
        if strategy == "latest":
            if isinstance(existing, dict) and isinstance(incoming, dict):
                e_ts = existing.get("updated_at", "")
                i_ts = incoming.get("updated_at", "")
                return incoming if i_ts >= e_ts else existing
            return incoming

        if strategy == "merge":
            if isinstance(existing, dict) and isinstance(incoming, dict):
                merged = existing.copy()
                merged.update(incoming)
                return merged
            if isinstance(existing, list) and isinstance(incoming, list):
                return list(set(existing + incoming))
            return incoming

        if strategy == "accumulate":
            if isinstance(existing, (int, float)) and isinstance(
                incoming, (int, float)
            ):
                return existing + incoming
            return incoming

        return incoming
