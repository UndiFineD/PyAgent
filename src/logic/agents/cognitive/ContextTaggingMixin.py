#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
from src.logic.agents.cognitive.context.models.ContextTag import ContextTag


class ContextTaggingMixin:
    """Tagging methods for ContextAgent."""

    def add_tag(self, tag: ContextTag) -> None:
        """Add a tag."""
        if not hasattr(self, "_tags"):
            self._tags: dict[str, ContextTag] = {}
        self._tags[tag.name] = tag

    def remove_tag(self, tag_name: str) -> bool:
        """Remove a tag."""
        if hasattr(self, "_tags") and tag_name in self._tags:
            del self._tags[tag_name]
            return True
        return False

    def get_tags(self) -> list[ContextTag]:
        """Get all tags."""
        return list(getattr(self, "_tags", {}).values())

    def has_tag(self, tag_name: str) -> bool:
        """Check if a tag exists."""
        return tag_name in getattr(self, "_tags", {})

    def get_tags_by_parent(self, parent_name: str) -> list[ContextTag]:
        """Get all tags with a specific parent."""
        return [t for t in getattr(self, "_tags", {}).values() if t.parent == parent_name]
