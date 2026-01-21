#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import logging


class ContextRAGMixin:
    """RAG and shard management methods for ContextAgent."""

    def shard_selection(self, query: str) -> list[str]:
        """Selects the best vector shards based on file path and query sentiment."""
        active_path = str(self.file_path)
        selected = self.rag_core.route_query_to_shards(
            query, active_path, self.rag_shards
        )
        logging.info(f"ContextAgent: Query '{query}' routed to {len(selected)} shards.")
        return selected
