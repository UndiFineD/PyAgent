#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Licensed under the Apache License, Version 2.0 (the "License");


"""Mixin for RAG-based context retrieval."""

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
