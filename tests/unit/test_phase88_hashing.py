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

import numpy as np
import pytest
from src.infrastructure.swarm.orchestration.swarm.semantic_hashing import SemanticHasher

def test_semantic_hashing_collision():
    hasher = SemanticHasher(dimension=384, num_bits=8)

    # Create two very similar embeddings
    emb1 = np.ones(384)
    emb2 = np.ones(384) + 0.01 * np.random.randn(384)

    # Create a very different embedding
    emb3 = -np.ones(384)

    h1 = hasher.compute_hash(emb1)
    h2 = hasher.compute_hash(emb2)
    h3 = hasher.compute_hash(emb3)

    # Close embeddings should likely share the same hash (LSH property)
    assert h1 == h2
    # Opposing embeddings should have different hashes
    assert h1 != h3

    print(f"\n[Phase 88] LSH successful: h1={h1}, h2={h2}, h3={h3}")

def test_hashing_index():
    hasher = SemanticHasher(dimension=384, num_bits=4)
    emb = np.random.randn(384)

    hasher.index_shard("shard_A", emb)
    candidates = hasher.find_nearest_shards(emb)

    assert "shard_A" in candidates
    print("[Phase 88] Semantic index correctly retrieved shard A from its bucket.")
