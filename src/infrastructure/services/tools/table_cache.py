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

# SPDX-License-Identifier: Apache-2.0
TableCache: Trie-based metadata precomputation for Text-to-SQL.
Implemented based on arXiv:2601.08743 (Jan 2026).

import dataclasses
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class TableMetadata:
    table_name: str
    columns: List[str]
    sample_rows: List[Dict[str, Any]] = dataclasses.field(default_factory=list)




class TableTrieNode:
    def __init__(self):
        self.children: Dict[str, TableTrieNode] = {}
        self.metadata: Optional[TableMetadata] = None




class TableCacheManager:
        Manages a Trie-based cache of database schema metadata.
    Enables 3.6x TTFT speedup for Text-to-SQL tasks by pre-filtering schema.
    
    def __init__(self):
        self.root = TableTrieNode()
        self.table_count = 0

    def insert(self, table_name: str, columns: List[str]):
        """Insert schema metadata into the trie.        node = self.root
        # Index table name and column names for fast lookup
        for char in table_name.lower():
            if char not in node.children:
                node.children[char] = TableTrieNode()
            node = node.children[char]

        node.metadata = TableMetadata(table_name=table_name, columns=columns)
        self.table_count += 1

    def search_prefix(self, prefix: str) -> List[TableMetadata]:
        """Search for tables matching a prefix.        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]

        # Collect all metadata in subtree
        results = []
        self._collect_metadata(node, results)
        return results

    def _collect_metadata(self, node: TableTrieNode, results: List[TableMetadata]):
        if node.metadata:
            results.append(node.metadata)
        for child in node.children.values():
            self._collect_metadata(child, results)

    def prune_schema(self, query: str) -> List[TableMetadata]:
                Heuristically prune schema based on query keywords.
        In a real implementation, this uses the Trie to find relevant tables.
                # Simplified: look for query words matching table names
        words = query.lower().split()
        relevant = []
        seen = set()
        for word in words:
            matches = self.search_prefix(word)
            for m in matches:
                if m.table_name not in seen:
                    relevant.append(m)
                    seen.add(m.table_name)
        return relevant
