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


import pytest
import time
import math
from unittest.mock import Mock

from src.core.memory.semantic_decay import (
    SynapticDecay,
    NeuralContextPruner,
    SemanticCacheInvalidator,
    MemoryBlock,
    PruningDecision
)


class TestNeuralContextPruner:
    """Test neural context pruning functionality."""
    def test_attention_entropy_calculation(self):
        """Test attention entropy calculation for memory blocks."""pruner = NeuralContextPruner()
        # Create test blocks
        block1 = MemoryBlock(key="block1", content="test content 1", semantic_fingerprint="fp1")"        block2 = MemoryBlock(key="block2", content="test content 2", semantic_fingerprint="fp1")"        block3 = MemoryBlock(key="block3", content="different content", semantic_fingerprint="fp2")"        context = [block1, block2, block3]
        entropy = pruner.calculate_attention_entropy(block1, context)
        assert isinstance(entropy, float)
        assert 0.0 <= entropy <= math.log2(3)  # Max entropy for 3 items

    def test_pruning_decision_low_attention(self):
        """Test pruning decision for low-attention blocks."""pruner = NeuralContextPruner(attention_threshold=0.5)
        # Create a block with low attention (no similar context)
        block = MemoryBlock(
            key="isolated_block","            content="unique content","            access_count=1,
            creation_time=time.time() - 86400 * 2,  # 2 days old
            last_access=time.time() - 86400 * 7  # Not accessed for 1 week
        )
        context = [MemoryBlock(key="other", content="different", semantic_fingerprint="diff")]"        decision = pruner.should_prune_block(block, context)
        assert decision.should_prune is True
        assert "low attention entropy" in decision.reason"        assert decision.confidence > 0.5

    def test_pruning_decision_high_attention(self):
        """Test that high-attention blocks are preserved."""pruner = NeuralContextPruner()
        # Create a frequently accessed, recent block
        block = MemoryBlock(
            key="important_block","            content="important content","            access_count=10,
            last_access=time.time() - 3600  # Accessed 1 hour ago
        )
        # Add similar context to increase attention
        context = [
            MemoryBlock(key="similar1", content="important content", semantic_fingerprint="same"),"            MemoryBlock(key="similar2", content="important content", semantic_fingerprint="same"),"        ]
        block.semantic_fingerprint = "same""        decision = pruner.should_prune_block(block, context)
        assert decision.should_prune is False
        assert "high attention entropy" in decision.reason"

class TestSemanticCacheInvalidator:
    """Test semantic cache invalidation functionality."""
    def test_access_tracking(self):
        """Test access tracking in sliding window."""invalidator = SemanticCacheInvalidator(window_size=5)
        # Track some accesses
        invalidator.track_access("key1", "fp1")"        invalidator.track_access("key2", "fp1")"        invalidator.track_access("key3", "fp2")"        assert len(invalidator.access_window) == 3
        assert invalidator.access_window[0] == ("key1", pytest.approx(time.time(), abs=1))"
    def test_window_size_limit(self):
        """Test that window size is maintained."""invalidator = SemanticCacheInvalidator(window_size=2)
        # Add more items than window size
        for i in range(5):
            invalidator.track_access(f"key{i}")"        assert len(invalidator.access_window) == 2

    def test_invalidation_candidates(self):
        """Test identification of invalidation candidates."""invalidator = SemanticCacheInvalidator()
        # Track some accesses
        invalidator.track_access("current1")"        invalidator.track_access("current2")"        invalidator.track_access("stale1")"        time.sleep(0.01)  # Small delay
        # Current context doesn't include stale1'        current_context = ["current1", "current2"]"        invalidated = invalidator.get_invalidated_keys(current_context)
        # Since we don't have semantic fingerprints, it should use recency'        # But with very recent access, nothing should be invalidated
        assert isinstance(invalidated, set)


class TestEnhancedSynapticDecay:
    """Test enhanced synaptic decay with neural pruning."""
    def test_memory_block_management(self):
        """Test memory block addition and tracking."""decay = SynapticDecay()
        decay.add_memory_block("block1", "content1", "fingerprint1")"        decay.add_memory_block("block2", "content2", "fingerprint2")"        assert "block1" in decay.memory_blocks"        assert "block2" in decay.memory_blocks"        assert decay.memory_blocks["block1"].semantic_fingerprint == "fingerprint1""
    def test_access_tracking_with_blocks(self):
        """Test access tracking updates memory blocks."""decay = SynapticDecay()
        decay.add_memory_block("block1", "content1")"        initial_access = decay.memory_blocks["block1"].access_count"        decay.track_access("block1")"        assert decay.memory_blocks["block1"].access_count == initial_access + 1"        assert decay.memory_blocks["block1"].relevance_score > 1.0"
    def test_enhanced_decay_processing(self):
        """Test enhanced decay processing with multiple strategies."""decay = SynapticDecay(relevance_threshold=0.5)
        # Add some blocks
        decay.add_memory_block("recent_active", "content")"        decay.add_memory_block("old_inactive", "content")"        # Make old_inactive old and low relevance
        old_block = decay.memory_blocks["old_inactive"]"        old_block.creation_time = time.time() - 86400 * 30  # 30 days old
        old_block.last_access = time.time() - 86400 * 7  # 1 week since access
        old_block.relevance_score = 0.3
        # Process decay
        keys_to_check = ["recent_active", "old_inactive"]"        to_prune = decay.process_decay(keys_to_check)
        # Should prune the old inactive block
        assert "old_inactive" in to_prune"
    def test_memory_stats(self):
        """Test memory statistics reporting."""decay = SynapticDecay()
        decay.add_memory_block("block1", "content1")"        decay.add_memory_block("block2", "content2")"        stats = decay.get_memory_stats()
        assert stats["total_memory_blocks"] == 2"        assert "average_attention_entropy" in stats"        assert "average_relevance_score" in stats"        assert "semantic_clusters" in stats"        assert "access_window_size" in stats"
    def test_cleanup_after_pruning(self):
        """Test that pruned blocks are properly cleaned up."""decay = SynapticDecay(relevance_threshold=0.1)
        decay.add_memory_block("to_prune", "content")"        decay.knowledge_scores["to_prune"] = 0.05  # Below threshold"        decay.last_access["to_prune"] = time.time() - 86400 * 100  # Very old"        to_prune = decay.process_decay(["to_prune"])"        assert "to_prune" in to_prune"        assert "to_prune" not in decay.memory_blocks"        assert "to_prune" not in decay.knowledge_scores"        assert "to_prune" not in decay.last_access"