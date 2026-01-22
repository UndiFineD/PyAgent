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

import pytest
import torch
from src.infrastructure.engine.kv_cache.v2.block_table import BlockTableV2
from src.infrastructure.engine.kv_cache.v2.kv_cache_interface import KVCacheInterfaceV2
from src.infrastructure.engine.kv_cache.v2.block_hash_manager import BlockHashManager

def test_block_table_allocation_v2():
    """Test v2 block table allocation and hybrid support."""
    bt = BlockTableV2(num_blocks=100, block_size=16)
    blocks = bt.allocate(seq_id=42, num_required_blocks=5)
    assert len(blocks) == 5
    assert bt.get_utilization() == 5.0
    
    # Test hybrid size update
    bt.update_hybrid_mapping(blocks[0], new_size=32)
    assert bt.block_size_map[blocks[0]] == 32

def test_kv_cache_interface_storage():
    """Test v2 interface storage allocation."""
    interface = KVCacheInterfaceV2(num_layers=2, num_heads=8, head_size=64, num_blocks=10)
    # Note: On CI might want to use 'cpu' instead of 'cuda'
    device = "cuda" if torch.cuda.is_available() else "cpu"
    interface.initialize_storage(device=device)
    
    assert interface.k_cache is not None
    assert interface.k_cache.shape == (10, 2, 8, 16, 64)
    assert interface.k_cache.device.type in ["cuda", "cpu"]

def test_block_hash_manager():
    """Test prefix caching via block hashing."""
    manager = BlockHashManager()
    tokens = [1, 2, 3, 4, 5]
    
    # Register a block
    manager.register_block(block_id=7, tokens=tokens)
    
    # Precise lookup
    found_id = manager.find_block_by_tokens(tokens)
    assert found_id == 7
    
    # Miss lookup
    assert manager.find_block_by_tokens([1, 2, 3]) is None

def test_context_parallel_mask():
    """Test CP mask generation in block table."""
    bt = BlockTableV2(num_blocks=100)
    blocks = bt.allocate(seq_id=1, num_required_blocks=10)
    
    # Rank 0 of 2
    mask0 = bt.get_context_parallel_mask(seq_id=1, rank=0, world_size=2)
    assert len(mask0) == 5
    assert mask0 == blocks[:5]
    
    # Rank 1 of 2
    mask1 = bt.get_context_parallel_mask(seq_id=1, rank=1, world_size=2)
    assert len(mask1) == 5
    assert mask1 == blocks[5:]
