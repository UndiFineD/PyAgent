# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import json
from typing import TYPE_CHECKING
from src.core.base.BaseUtilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.cognitive.HierarchicalMemoryAgent import HierarchicalMemoryAgent

class MemoryQueryMixin:
    """Mixin for hierarchical memory querying in HierarchicalMemoryAgent."""

    @as_tool
    def hierarchical_query(self: HierarchicalMemoryAgent, query: str, deep_search: bool = False) -> str:
        """Searches across memory tiers starting from short-term."""
        search_tiers = ["short", "mid"]
        if deep_search:
            search_tiers += ["long", "archival"]

        # Collect all memory files
        all_data = []  # (tier, content, tags)
        for tier in search_tiers:
            tier_dir = self.memory_root / tier
            for mem_file in tier_dir.glob("*.json"):
                try:
                    with open(mem_file) as f:
                        data = json.load(f)
                    all_data.append((tier, data.get("content", ""), data.get("tags", [])))
                except Exception:
                    continue

        if not all_data:
            return "No matching memories found."

        # Rust-accelerated search
        try:
            from rust_core import search_with_tags_rust
            contents = [d[1] for d in all_data]
            tags_list = [d[2] for d in all_data]
            matches = search_with_tags_rust(query, contents, tags_list)

            results = []
            for idx, score in matches:
                tier, content, _ = all_data[idx]
                results.append(f"[{tier.upper()}] {content[:100]}...")

            if not results:
                return "No matching memories found."
            return "### Memory Search Results\\n\\n" + "\\n".join(results)
        except (ImportError, Exception):
            pass  # Fall back to Python

        # Python fallback
        results = []
        for tier, content, tags in all_data:
            if query.lower() in content.lower() or any(
                query.lower() in t.lower() for t in tags
            ):
                results.append(f"[{tier.upper()}] {content[:100]}...")

        if not results:
            return "No matching memories found."

        return "### Memory Search Results\\n\\n" + "\\n".join(results)
