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

"""
Semantic hashing.py module.
"""

import logging
from typing import Dict, List, Set

import numpy as np

logger = logging.getLogger(__name__)


class SemanticHasher:
    """
    Implements Locality Sensitive Hashing (LSH) for swarm contexts (Phase 88).
    Allows O(1) or O(log N) lookup of semantically related context shards across ranks.
    """

    def __init__(self, dimension: int = 384, num_bits: int = 16) -> None:
        self.dimension = dimension
        self.num_bits = num_bits
        # Random projection matrix
        np.random.seed(42)  # Deterministic projections across the swarm nodes
        self.projections = np.random.randn(num_bits, dimension)

        # The hash table: bucket_id -> set(shard_identifiers)
        self.buckets: Dict[int, Set[str]] = {}

    def compute_hash(self, embedding: np.ndarray) -> int:
        """Converts an embedding into a bitstring hash via random projections."""
        if len(embedding) != self.dimension:
            # Simple padding/truncation for flex
            temp = np.zeros(self.dimension)
            temp[: min(len(embedding), self.dimension)] = embedding[: min(len(embedding), self.dimension)]
            embedding = temp

        projections = np.dot(self.projections, embedding)
        # Convert signs to bits
        bits = (projections > 0).astype(int)

        # Convert bit array to integer
        hash_val = 0
        for bit in bits:
            hash_val = (hash_val << 1) | bit
        return hash_val

    def index_shard(self, shard_id: str, embedding: np.ndarray):
        """Adds a shard to the semantic hash table."""
        h = self.compute_hash(embedding)
        if h not in self.buckets:
            self.buckets[h] = set()
        self.buckets[h].add(shard_id)
        logger.debug(f"[Phase 88] SemanticHashing: Indexed {shard_id} in bucket {h:016b}")

    def find_nearest_shards(self, query_emb: np.ndarray) -> List[str]:
        """Finds shards in the same semantic bucket."""
        h = self.compute_hash(query_emb)
        shards = list(self.buckets.get(h, set()))
        if shards:
            logger.info(f"[Phase 88] SemanticHashing: Found {len(shards)} candidates in bucket {h:016b}")
        return shards

    def remove_shard(self, shard_id: str):
        """Removes a shard from all buckets."""
        for bucket in self.buckets.values():
            if shard_id in bucket:
                bucket.remove(shard_id)
