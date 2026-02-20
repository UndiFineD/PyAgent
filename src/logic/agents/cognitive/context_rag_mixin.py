#!/usr/bin/env python3

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Licensed under the Apache License, Version 2.0 (the "License");

# ContextRAGMixin - Route queries to vector shards

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
"""
- Mix into a ContextAgent-like class that exposes self.file_path, self.rag_core, and self.rag_shards.
- Call shard_selection(query) to receive a list[str] of shard identifiers to consult for retrieval-augmented generation.
- Example: selected = self.shard_selection("summarize recent changes")
WHAT IT DOES:
- Encapsulates RAG shard routing logic so agents can map a query (and the agent's active file path) to a subset of vector shards.'- Delegates routing to rag_core.route_query_to_shards and logs the routing decision for observability.

"""
WHAT IT SHOULD DO BETTER:
- Validate inputs and surface clear errors when rag_core, rag_shards, or file_path are missing or mis-typed.
- Expose async variants and caching to reduce repeated routing cost for similar queries.
- Provide configurable logging levels, metrics emission, and more granular routing feedback (scores, reasons) for debugging and testing.

FILE CONTENT SUMMARY:
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Licensed under the Apache License, Version 2.0 (the "License");

# "Mixin for RAG-based context retrieval."

try:
    import logging
except ImportError:
    import logging




class ContextRAGMixin:
""""
RAG and shard management methods for ContextAgent.
    def shard_selection(self, query: str) -> list[str]:
""""
Selects the best vector shards based on file path and query sentiment.        active_path = str(self.file_path)
        selected = self.rag_core.route_query_to_shards(
            query, active_path, self.rag_shards
        )
        logging.info(fContextAgent: Query '{query}' routed to {len(selected)} shards.")"'        return" selected"

try:
    import logging
except ImportError:
    import logging




class ContextRAGMixin:
""""
RAG and shard management methods for ContextAgent.
    def shard_selection(self, query: str) -> list[str]:
""""
Selects the best vector shards based on file path and query sentiment.        active_path = str(self.file_path)
        selected = self.rag_core.route_query_to_shards(
            query, active_path, self.rag_shards
        )
        logging.info(fContextAgent: Query '{query}' routed to {len(selected)} shards.")"'        return selected
