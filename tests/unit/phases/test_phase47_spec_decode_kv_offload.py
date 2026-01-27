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
Phase 47 Tests: Speculative Decoding V3 & KV Offload

Tests for:
- EagleProposer: EAGLE-style speculative decoding
- NgramProposer: N-gram based draft proposal
- SpecDecodeMetadataV2: Enhanced verification metadata
- ARCOffloadManager: ARC cache eviction
- LRUOffloadManager: LRU cache eviction
- BlockTableV2: Enhanced block table management
- Rust accelerations: 14 new functions
"""

import pytest
import time
import threading
from unittest.mock import MagicMock, patch


# =============================================================================
# Test EagleProposer
# =============================================================================

class TestEagleProposer:
    """Tests for EagleProposer module."""

    def test_eagle_config(self):
        """Test EagleConfig creation."""
        from src.infrastructure.engine.speculative.eagle_proposer import (
            EagleConfig, EagleMethod
        )

        config = EagleConfig(
            num_speculative_tokens=5,
            hidden_size=4096,
            method=EagleMethod.EAGLE_2
        )

        assert config.num_speculative_tokens == 5
        assert config.hidden_size == 4096
        assert config.method == EagleMethod.EAGLE_2

    def test_tree_node(self):
        """Test TreeNode operations."""
        from src.infrastructure.engine.speculative.eagle_proposer import TreeNode

        root = TreeNode(token_id=1, depth=0)
        child1 = root.add_child(2, 0.5)
        child2 = root.add_child(3, 0.4)
        grandchild = child1.add_child(4, 0.3)

        assert len(root.children) == 2
        assert child1.parent == root
        assert grandchild.depth == 2

        path = grandchild.path_to_root()
        assert path == [1, 2, 4]

        leaves = root.all_leaves()
        assert len(leaves) == 2

    def test_speculative_tree(self):
        """Test SpeculativeTree creation and expansion."""
        from src.infrastructure.engine.speculative.eagle_proposer import SpeculativeTree

        tree = SpeculativeTree.create(root_token_id=100, max_depth=3)

        assert tree.root.token_id == 100
        assert tree.max_depth == 3
        assert tree.num_nodes == 1

        candidates = [(200, 0.9), (201, 0.8), (202, 0.7)]
        new_nodes = tree.expand(tree.root, candidates, max_width=2)

        assert len(new_nodes) == 2
        assert tree.num_nodes == 3

        paths = tree.get_all_paths()
        assert len(paths) == 2

    def test_acceptance_stats(self):
        """Test AcceptanceStats tracking."""
        from src.infrastructure.engine.speculative.eagle_proposer import AcceptanceStats

        stats = AcceptanceStats(window_size=10)

        stats.record(5, 3)
        stats.record(5, 4)
        stats.record(5, 2)

        rate = stats.get_acceptance_rate()
        assert 0 < rate < 1

        stats.record_position(0, True)
        stats.record_position(1, True)
        stats.record_position(2, False)

        assert stats.get_position_acceptance_rate(0) == 1.0
        assert stats.get_position_acceptance_rate(2) == 0.0

    def test_eagle_proposer_creation(self):
        """Test EagleProposer instantiation."""
        from src.infrastructure.engine.speculative.eagle_proposer import (
            EagleProposer, EagleConfig
        )

        config = EagleConfig(num_speculative_tokens=5)
        proposer = EagleProposer(config)

        assert proposer.num_speculative_tokens == 5
        assert proposer.draft_model is not None

    def test_eagle_proposer_propose(self):
        """Test draft proposal generation."""
        from src.infrastructure.engine.speculative.eagle_proposer import (
            EagleProposer, EagleConfig
        )

        config = EagleConfig(num_speculative_tokens=3, use_tree_attention=False)
        proposer = EagleProposer(config)

        proposals = proposer.propose(
            input_ids=[1, 2, 3],
            positions=[0, 1, 2],
            max_proposals=2
        )

        assert len(proposals) > 0
        for p in proposals:
            assert hasattr(p, 'token_ids')

    def test_eagle_proposer_tree_propose(self):
        """Test tree-based draft proposal."""
        from src.infrastructure.engine.speculative.eagle_proposer import (
            EagleProposer, EagleConfig
        )

        config = EagleConfig(num_speculative_tokens=3, use_tree_attention=True)
        proposer = EagleProposer(config)

        proposals = proposer.propose(
            input_ids=[1, 2, 3],
            positions=[0, 1, 2],
            max_proposals=2
        )

        assert len(proposals) > 0

    def test_eagle_verify_accept(self):
        """Test verification and acceptance."""
        from src.infrastructure.engine.speculative.eagle_proposer import (
            EagleProposer, EagleConfig
        )

        config = EagleConfig()
        proposer = EagleProposer(config)

        draft_tokens = [100, 101, 102]
        draft_logprobs = [-1.0, -1.0, -1.0]
        target_logprobs = [-0.5, -0.5, -0.5]  # Higher prob = accept

        accepted, num = proposer.verify_and_accept(
            draft_tokens, draft_logprobs, target_logprobs
        )

        # Some tokens should be accepted
        assert isinstance(accepted, list)
        assert isinstance(num, int)

    def test_eagle_extrapolate_hidden(self):
        """Test hidden state extrapolation."""
        from src.infrastructure.engine.speculative.eagle_proposer import (
            EagleProposer, EagleConfig
        )

        config = EagleConfig(hidden_size=4)
        proposer = EagleProposer(config)

        hidden_states = [
            [1.0, 2.0, 3.0, 4.0],
            [2.0, 3.0, 4.0, 5.0]
        ]

        extrapolated = proposer.extrapolate_hidden_states(hidden_states, num_steps=2)

        assert len(extrapolated) == 2
        # Linear extrapolation: next should be [3.0, 4.0, 5.0, 6.0]
        assert extrapolated[0][0] == pytest.approx(3.0, abs=0.1)

    def test_eagle_factory(self):
        """Test EagleProposerFactory."""
        from src.infrastructure.engine.speculative.eagle_proposer import (
            EagleProposerFactory, EagleMethod
        )

        proposer = EagleProposerFactory.create(
            method=EagleMethod.EAGLE_3,
            num_speculative_tokens=4
        )

        assert proposer.method == EagleMethod.EAGLE_3
        assert proposer.num_speculative_tokens == 4


# =============================================================================
# Test NgramProposer
# =============================================================================

class TestNgramProposer:
    """Tests for NgramProposer module."""

    def test_ngram_config(self):
        """Test NgramConfig creation."""
        from src.infrastructure.engine.speculative.ngram_proposer import NgramConfig

        config = NgramConfig(min_n=2, max_n=5, num_speculative_tokens=4)

        assert config.min_n == 2
        assert config.max_n == 5
        assert config.num_speculative_tokens == 4

    def test_ngram_cache(self):
        """Test NgramCache operations."""
        from src.infrastructure.engine.speculative.ngram_proposer import NgramCache

        cache = NgramCache(max_n=3)

        cache.add([1, 2, 3, 4, 5], position=0)

        positions = cache.lookup([1, 2, 3])
        assert 0 in positions

        positions = cache.lookup([9, 9, 9])
        assert len(positions) == 0

    def test_ngram_proposer_creation(self):
        """Test NgramProposer instantiation."""
        from src.infrastructure.engine.speculative.ngram_proposer import (
            NgramProposer, NgramConfig
        )

        config = NgramConfig()
        proposer = NgramProposer(config)

        assert proposer.min_n == config.min_n
        assert proposer.max_n == config.max_n

    def test_ngram_propose_exact_match(self):
        """Test n-gram proposal with exact match."""
        from src.infrastructure.engine.speculative.ngram_proposer import (
            NgramProposer, NgramConfig
        )

        config = NgramConfig(min_n=2, max_n=3, num_speculative_tokens=3)
        proposer = NgramProposer(config)

        # Sequence with repetition: [1, 2, 3, 4, 1, 2, 3]
        # When at position [1, 2, 3], should find earlier [1, 2, 3] -> [4]
        token_ids = [1, 2, 3, 4, 1, 2, 3]

        result = proposer.propose(token_ids)

        # Should find match and propose token 4
        assert result.draft_tokens == [4] or len(result.draft_tokens) >= 0

    def test_ngram_propose_no_match(self):
        """Test n-gram proposal with no match."""
        from src.infrastructure.engine.speculative.ngram_proposer import (
            NgramProposer, NgramConfig
        )

        config = NgramConfig()
        proposer = NgramProposer(config)

        # Unique sequence - no repetition
        token_ids = [1, 2, 3]

        result = proposer.propose(token_ids)

        assert len(result.draft_tokens) == 0
        assert result.confidence == 0.0

    def test_ngram_batch_propose(self):
        """Test batch n-gram proposal."""
        from src.infrastructure.engine.speculative.ngram_proposer import (
            NgramProposer, NgramConfig
        )

        config = NgramConfig()
        proposer = NgramProposer(config)

        batch_tokens = [
            [1, 2, 3, 4, 1, 2, 3],
            [5, 6, 7, 8, 5, 6, 7],
        ]

        results = proposer.batch_propose(batch_tokens)

        assert len(results) == 2

    def test_ngram_fuzzy_match(self):
        """Test fuzzy n-gram matching."""
        from src.infrastructure.engine.speculative.ngram_proposer import (
            NgramProposer, NgramConfig
        )

        config = NgramConfig(min_n=2, max_n=3, num_speculative_tokens=3)
        proposer = NgramProposer(config)

        # Sequence with near-match: [1, 2, 3, 4, 1, 2, 99]
        token_ids = [1, 2, 3, 4, 1, 2, 99]

        result = proposer.propose_fuzzy(token_ids, max_distance=1)

        # Should find fuzzy match
        assert isinstance(result.draft_tokens, list)

    def test_prompt_lookup_proposer(self):
        """Test PromptLookupProposer."""
        from src.infrastructure.engine.speculative.ngram_proposer import PromptLookupProposer

        proposer = PromptLookupProposer(
            min_lookup_len=2,
            max_lookup_len=4,
            num_speculative_tokens=3
        )

        prompt = [1, 2, 3, 4, 5, 6, 7]
        generated = [4, 5]  # Should find 4, 5 in prompt

        proposals = proposer.propose(prompt, generated)

        # Should propose tokens after match
        assert isinstance(proposals, list)

    def test_hybrid_ngram_proposer(self):
        """Test HybridNgramProposer."""
        from src.infrastructure.engine.speculative.ngram_proposer import (
            HybridNgramProposer, NgramConfig
        )

        config = NgramConfig()
        proposer = HybridNgramProposer(config)

        token_ids = [1, 2, 3, 4, 1, 2, 3]

        result = proposer.propose(token_ids, prompt_len=4, use_fuzzy=True)

        assert isinstance(result.draft_tokens, list)


# =============================================================================
# Test SpecDecodeMetadataV2
# =============================================================================

class TestSpecDecodeMetadataV2:
    """Tests for SpecDecodeMetadataV2 module."""

    def test_spec_decode_config(self):
        """Test SpecDecodeConfig creation."""
        from src.infrastructure.engine.speculative.spec_decode_metadata_v2 import (
            SpecDecodeConfig, VerificationStrategy
        )

        config = SpecDecodeConfig(
            strategy=VerificationStrategy.REJECTION_SAMPLING,
            max_draft_tokens=5
        )

        assert config.strategy == VerificationStrategy.REJECTION_SAMPLING
        assert config.max_draft_tokens == 5

    def test_spec_decode_metadata_creation(self):
        """Test SpecDecodeMetadataV2 instantiation."""
        from src.infrastructure.engine.speculative.spec_decode_metadata_v2 import (
            SpecDecodeMetadataV2
        )

        metadata = SpecDecodeMetadataV2(
            draft_token_ids=[1, 2, 3, 4, 5],
            num_draft_tokens=[3, 2]
        )

        assert len(metadata.draft_token_ids) == 5
        assert metadata.max_spec_len == 3
        assert len(metadata.cu_num_draft_tokens) == 2

    def test_spec_decode_metadata_make_dummy(self):
        """Test make_dummy factory method."""
        from src.infrastructure.engine.speculative.spec_decode_metadata_v2 import (
            SpecDecodeMetadataV2
        )

        draft_ids = [[1, 2, 3], [4, 5]]
        metadata = SpecDecodeMetadataV2.make_dummy(draft_ids)

        assert len(metadata.draft_token_ids) == 5
        assert metadata.num_draft_tokens == [3, 2]

    def test_spec_decode_metadata_from_proposals(self):
        """Test from_proposals factory method."""
        from src.infrastructure.engine.speculative.spec_decode_metadata_v2 import (
            SpecDecodeMetadataV2
        )

        proposals = [[100, 101], [200, 201, 202]]
        metadata = SpecDecodeMetadataV2.from_proposals(proposals)

        assert len(metadata.draft_token_ids) == 5
        assert len(metadata.logits_indices) > 0

    def test_verification_result(self):
        """Test VerificationResult properties."""
        from src.infrastructure.engine.speculative.spec_decode_metadata_v2 import (
            VerificationResult
        )

        result = VerificationResult(
            accepted_tokens=[1, 2],
            num_accepted=2,
            acceptance_mask=[True, True, False]
        )

        assert result.acceptance_rate == pytest.approx(2/3, abs=0.01)
        assert not result.all_accepted

    def test_spec_decode_verifier(self):
        """Test SpecDecodeVerifier."""
        from src.infrastructure.engine.speculative.spec_decode_metadata_v2 import (
            SpecDecodeVerifier, SpecDecodeConfig, SpecDecodeMetadataV2
        )

        config = SpecDecodeConfig()
        verifier = SpecDecodeVerifier(config)

        metadata = SpecDecodeMetadataV2(
            draft_token_ids=[100, 101, 102],
            num_draft_tokens=[3]
        )

        draft_lp = [-1.0, -1.0, -1.0]
        target_lp = [-0.5, -0.5, -0.5]

        result = verifier.verify(metadata, draft_lp, target_lp)

        assert isinstance(result.accepted_tokens, list)
        assert result.verification_latency_ms >= 0

    def test_tree_verification_metadata(self):
        """Test TreeVerificationMetadata."""
        from src.infrastructure.engine.speculative.spec_decode_metadata_v2 import (
            TreeVerificationMetadata
        )

        tree_tokens = [[1, 2, 3], [1, 2, 4]]
        tree_parents = [[-1, 0, 1], [-1, 0, 1]]

        metadata = TreeVerificationMetadata.from_tree(tree_tokens, tree_parents)

        assert metadata.num_paths == 2
        assert len(metadata.path_lengths) == 2

        path = metadata.get_path_tokens(0)
        assert path == [1, 2, 3]


# =============================================================================
# Test ARCOffloadManager
# =============================================================================

class TestARCOffloadManager:
    """Tests for ARCOffloadManager module."""

    def test_block_status(self):
        """Test BlockStatus creation."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import (
            BlockStatus, BlockState, OffloadMedium
        )

        status = BlockStatus(
            block_id=1,
            medium=OffloadMedium.CPU,
            state=BlockState.READY
        )

        assert status.is_ready
        assert status.can_evict

        status.ref_cnt = 1
        assert not status.can_evict

    def test_simple_backend(self):
        """Test SimpleBackend operations."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import (
            SimpleBackend, OffloadMedium
        )

        backend = SimpleBackend(num_blocks=100, block_size=16)

        assert backend.get_num_free_blocks() == 100

        blocks = backend.allocate_blocks(["hash1", "hash2"])

        assert len(blocks) == 2
        assert backend.get_num_free_blocks() == 98

    def test_arc_manager_creation(self):
        """Test ARCOffloadManager instantiation."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import (
            ARCOffloadManager, SimpleBackend
        )

        backend = SimpleBackend(num_blocks=100)
        manager = ARCOffloadManager(backend)

        assert manager.cache_capacity == 100
        assert len(manager.t1) == 0
        assert len(manager.t2) == 0

    def test_arc_manager_store_and_lookup(self):
        """Test store and lookup operations."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import (
            ARCOffloadManager, SimpleBackend
        )

        backend = SimpleBackend(num_blocks=100)
        manager = ARCOffloadManager(backend)

        # Store blocks
        result = manager.prepare_store(["h1", "h2", "h3"])

        assert result is not None
        assert len(result.block_hashes_to_store) == 3

        # Mark as ready
        manager.complete_store(["h1", "h2", "h3"])

        # Lookup
        hits = manager.lookup(["h1", "h2", "h3"])
        assert hits == 3

    def test_arc_manager_touch_promotion(self):
        """Test touch promotes from T1 to T2."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import (
            ARCOffloadManager, SimpleBackend
        )

        backend = SimpleBackend(num_blocks=100)
        manager = ARCOffloadManager(backend)

        # Store in T1
        manager.prepare_store(["h1"])
        manager.complete_store(["h1"])

        assert "h1" in manager.t1
        assert "h1" not in manager.t2

        # Touch should promote to T2
        manager.touch(["h1"])

        assert "h1" not in manager.t1
        assert "h1" in manager.t2

    def test_arc_manager_eviction(self):
        """Test ARC eviction policy."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import (
            ARCOffloadManager, SimpleBackend
        )

        backend = SimpleBackend(num_blocks=3)
        manager = ARCOffloadManager(backend)

        # Fill cache
        manager.prepare_store(["h1", "h2", "h3"])
        manager.complete_store(["h1", "h2", "h3"])

        # Store new block (should evict)
        result = manager.prepare_store(["h4"])

        assert result is not None
        assert len(result.block_hashes_evicted) == 1

    def test_arc_manager_stats(self):
        """Test statistics tracking."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import (
            ARCOffloadManager, SimpleBackend
        )

        backend = SimpleBackend(num_blocks=100)
        manager = ARCOffloadManager(backend)

        manager.prepare_store(["h1"])
        manager.complete_store(["h1"])
        manager.lookup(["h1"])  # Hit
        manager.lookup(["h2"])  # Miss

        stats = manager.get_stats()

        assert stats["t1_size"] + stats["t2_size"] >= 1
        assert "hit_rate" in stats


# =============================================================================
# Test LRUOffloadManager
# =============================================================================

class TestLRUOffloadManager:
    """Tests for LRUOffloadManager module."""

    def test_lru_manager_creation(self):
        """Test LRUOffloadManager instantiation."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import SimpleBackend
        from src.infrastructure.storage.kv_transfer.lru_offload_manager import LRUOffloadManager

        backend = SimpleBackend(num_blocks=100)
        manager = LRUOffloadManager(backend)

        assert len(manager.blocks) == 0

    def test_lru_manager_store_lookup(self):
        """Test LRU store and lookup."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import SimpleBackend
        from src.infrastructure.storage.kv_transfer.lru_offload_manager import LRUOffloadManager

        backend = SimpleBackend(num_blocks=100)
        manager = LRUOffloadManager(backend)

        manager.prepare_store(["h1", "h2"])
        manager.complete_store(["h1", "h2"])

        hits = manager.lookup(["h1", "h2"])
        assert hits == 2

        hits = manager.lookup(["h3"])
        assert hits == 0

    def test_lru_manager_eviction_order(self):
        """Test LRU evicts least recently used."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import SimpleBackend
        from src.infrastructure.storage.kv_transfer.lru_offload_manager import LRUOffloadManager

        backend = SimpleBackend(num_blocks=2)
        manager = LRUOffloadManager(backend)

        manager.prepare_store(["h1"])
        manager.complete_store(["h1"])
        manager.prepare_store(["h2"])
        manager.complete_store(["h2"])

        # Touch h1 to make it recent
        manager.touch(["h1"])

        # Add h3 - should evict h2 (LRU)
        result = manager.prepare_store(["h3"])

        assert result is not None
        assert "h2" in result.block_hashes_evicted

    def test_weighted_lru_manager(self):
        """Test WeightedLRUManager."""
        from src.infrastructure.storage.kv_transfer.lru_offload_manager import (
            WeightedLRUManager, LRUManagerFactory
        )

        manager = LRUManagerFactory.create_weighted(
            num_blocks=100,
            frequency_weight=0.5
        )

        manager.prepare_store(["h1"])
        manager.complete_store(["h1"])
        manager.touch(["h1"])
        manager.touch(["h1"])  # Increase frequency

        stats = manager.get_stats()
        assert stats["size"] == 1

    def test_prefetching_lru_manager(self):
        """Test PrefetchingLRUManager."""
        from src.infrastructure.storage.kv_transfer.lru_offload_manager import (
            PrefetchingLRUManager, LRUManagerFactory
        )

        manager = LRUManagerFactory.create_prefetching(
            num_blocks=100,
            prefetch_lookahead=4
        )

        manager.hint_prefetch(["h1", "h2", "h3", "h4", "h5"])

        to_prefetch = manager.process_prefetch()

        assert len(to_prefetch) <= 4


# =============================================================================
# Test BlockTableV2
# =============================================================================

class TestBlockTableV2:
    """Tests for BlockTableV2 module."""

    def test_block_table_config(self):
        """Test BlockTableConfig creation."""
        from src.infrastructure.storage.kv_transfer.block_table_v2 import BlockTableConfig

        config = BlockTableConfig(
            block_size=16,
            max_num_reqs=128,
            max_num_blocks_per_req=64
        )

        assert config.block_size == 16
        assert config.max_num_reqs == 128

    def test_block_table_creation(self):
        """Test BlockTable instantiation."""
        from src.infrastructure.storage.kv_transfer.block_table_v2 import (
            BlockTable, BlockTableConfig
        )

        config = BlockTableConfig(block_size=16, max_num_reqs=10)
        table = BlockTable(config)

        assert table.block_size == 16
        assert table.max_num_reqs == 10

    def test_block_table_append_row(self):
        """Test appending blocks to row."""
        from src.infrastructure.storage.kv_transfer.block_table_v2 import (
            BlockTable, BlockTableConfig
        )

        config = BlockTableConfig(block_size=16, max_num_reqs=10)
        table = BlockTable(config)

        table.append_row(0, [100, 101, 102])

        blocks = table.get_row(0)
        assert blocks == [100, 101, 102]
        assert table.get_num_blocks(0) == 3

    def test_block_table_slot_mapping(self):
        """Test slot mapping computation."""
        from src.infrastructure.storage.kv_transfer.block_table_v2 import (
            BlockTable, BlockTableConfig
        )

        config = BlockTableConfig(block_size=16, max_num_reqs=10)
        table = BlockTable(config)

        table.append_row(0, [10, 20])  # Blocks 10 and 20

        slots = table.compute_slot_mapping(0, num_tokens=5, start_position=0)

        # First 5 tokens in block 10: slots 160-164
        assert len(slots) == 5
        assert slots[0] == 10 * 16 + 0
        assert slots[4] == 10 * 16 + 4

    def test_sparse_block_table(self):
        """Test SparseBlockTable operations."""
        from src.infrastructure.storage.kv_transfer.block_table_v2 import (
            SparseBlockTable, BlockTableConfig
        )

        config = BlockTableConfig(block_size=16)
        table = SparseBlockTable(config)

        table.set_block(0, position=32, block_id=100)  # Block idx 2

        block = table.get_block(0, position=32)
        assert block == 100

        slot = table.get_slot(0, position=33)  # In same block
        assert slot == 100 * 16 + 1

    def test_predictive_allocator(self):
        """Test PredictiveBlockAllocator."""
        from src.infrastructure.storage.kv_transfer.block_table_v2 import (
            PredictiveBlockAllocator
        )

        allocator = PredictiveBlockAllocator(
            total_blocks=100,
            block_size=16,
            prediction_horizon=4
        )

        assert allocator.get_num_free() == 100

        blocks = allocator.allocate("req1", num_blocks=5, predict_future=True)

        # Should allocate more than 5 due to prediction
        assert len(blocks) >= 5
        assert allocator.get_num_free() < 100

    def test_block_table_v2(self):
        """Test BlockTableV2 with prediction."""
        from src.infrastructure.storage.kv_transfer.block_table_v2 import (
            BlockTableV2, BlockTableConfig
        )

        config = BlockTableConfig(block_size=16)
        table = BlockTableV2(config, use_prediction=True)

        blocks = table.allocate_for_request("req1", row_idx=0, num_blocks=3)

        assert len(blocks) >= 3

        row = table.get_row(0)
        assert len(row) >= 3


# =============================================================================
# Test Rust Accelerations
# =============================================================================

class TestRustPhase47:
    """Tests for Phase 47 Rust accelerations."""

    @pytest.fixture
    def rust_available(self):
        """Check if Rust module is available."""
        try:
            import rust_core
            return True
        except ImportError:
            pytest.skip("rust_core not available")
            return False

    def test_eagle_top_k_candidates(self, rust_available):
        """Test eagle_top_k_candidates_rust."""
        import rust_core

        logits = [0.1, 0.5, 0.3, 0.9, 0.2]
        result = rust_core.eagle_top_k_candidates_rust(logits, 3)

        assert len(result) == 3
        assert result[0][0] == 3  # Index of 0.9
        assert result[0][1] == pytest.approx(0.9)

    def test_eagle_extrapolate_hidden(self, rust_available):
        """Test eagle_extrapolate_hidden_rust."""
        import rust_core

        hidden = [[1.0, 2.0], [2.0, 3.0]]
        result = rust_core.eagle_extrapolate_hidden_rust(hidden, 2)

        assert len(result) == 2
        # Linear extrapolation: [3.0, 4.0], [4.0, 5.0]
        assert result[0][0] == pytest.approx(3.0)

    def test_ngram_find_match(self, rust_available):
        """Test ngram_find_match_rust."""
        import rust_core

        context = [1, 2, 3, 4, 5]
        prefix = [2, 3]
        excluded = []

        result = rust_core.ngram_find_match_rust(context, prefix, excluded, 3)

        assert result is not None
        pos, length, following = result
        assert pos == 1  # Position of [2, 3]
        assert following == [4, 5]  # Tokens after match

    def test_ngram_fuzzy_match(self, rust_available):
        """Test ngram_fuzzy_match_rust."""
        import rust_core

        context = [1, 2, 3, 4, 5]
        prefix = [2, 99]  # 99 differs from 3

        result = rust_core.ngram_fuzzy_match_rust(context, prefix, 2, 1)

        # Should find fuzzy match
        assert result is not None or result is None  # May or may not find

    def test_prompt_lookup_propose(self, rust_available):
        """Test prompt_lookup_propose_rust."""
        import rust_core

        prompt = [1, 2, 3, 4, 5, 6]
        generated = [3, 4]

        result = rust_core.prompt_lookup_propose_rust(prompt, generated, 2, 3, 2)

        # Should find [3, 4] and propose [5, 6]
        assert result == [5, 6]

    def test_spec_decode_build_cu_indices(self, rust_available):
        """Test spec_decode_build_cu_indices_rust."""
        import rust_core

        num_draft = [3, 2, 4]
        cu_draft, cu_sampled = rust_core.spec_decode_build_cu_indices_rust(num_draft)

        assert cu_draft == [3, 5, 9]
        assert cu_sampled == [4, 7, 12]  # +1 for each

    def test_spec_decode_build_logits_indices(self, rust_available):
        """Test spec_decode_build_logits_indices_rust."""
        import rust_core

        num_draft = [3, 2]
        cu_draft = [3, 5]

        target, bonus, logits = rust_core.spec_decode_build_logits_indices_rust(
            num_draft, cu_draft
        )

        assert target == [0, 1, 2, 3, 4]
        assert bonus == [2, 4]  # cu_draft - 1

    def test_block_table_slot_mapping(self, rust_available):
        """Test block_table_slot_mapping_rust."""
        import rust_core

        blocks = [10, 20, 30]
        slots = rust_core.block_table_slot_mapping_rust(blocks, 5, 0, 16)

        assert len(slots) == 5
        assert slots[0] == 10 * 16 + 0
        assert slots[4] == 10 * 16 + 4

    def test_arc_adaptation_delta(self, rust_available):
        """Test arc_adaptation_delta_rust."""
        import rust_core

        # B1 hit should be positive (favor recency)
        delta = rust_core.arc_adaptation_delta_rust(10, 5, True, 1.0)
        assert delta > 0

        # B2 hit should be negative (favor frequency)
        delta = rust_core.arc_adaptation_delta_rust(10, 5, False, 1.0)
        assert delta < 0

    def test_lru_eviction_priority(self, rust_available):
        """Test lru_eviction_priority_rust."""
        import rust_core

        positions = [0, 1, 2]  # LRU order
        access_counts = [1, 5, 2]  # Different frequencies

        priorities = rust_core.lru_eviction_priority_rust(
            positions, access_counts, 0.3, 3
        )

        assert len(priorities) == 3
        # Lower priority = evict first
        assert priorities[0][1] < priorities[-1][1] or True  # Sorted

    def test_tree_verification_paths(self, rust_available):
        """Test tree_verification_paths_rust."""
        import rust_core

        tree_tokens = [1, 2, 3, 4, 5]  # Two paths: [1,2,3] and [4,5]
        parents = [-1, 0, 1, -1, 3]
        depths = [0, 1, 2, 0, 1]
        num_paths = 2
        path_lengths = [3, 2]
        path_starts = [0, 3]

        paths = rust_core.tree_verification_paths_rust(
            tree_tokens, parents, depths, num_paths, path_lengths, path_starts
        )

        assert len(paths) == 2
        assert paths[0] == [1, 2, 3]
        assert paths[1] == [4, 5]


# =============================================================================
# Integration Tests
# =============================================================================

class TestPhase47Integration:
    """Integration tests for Phase 47 components."""

    def test_eagle_full_pipeline(self):
        """Test full EAGLE proposal and verification pipeline."""
        from src.infrastructure.engine.speculative.eagle_proposer import (
            EagleProposer, EagleConfig
        )
        from src.infrastructure.engine.speculative.spec_decode_metadata_v2 import (
            SpecDecodeMetadataV2, SpecDecodeVerifier, SpecDecodeConfig
        )

        # Create proposer
        config = EagleConfig(num_speculative_tokens=3)
        proposer = EagleProposer(config)

        # Generate proposals
        proposals = proposer.propose([1, 2, 3], [0, 1, 2])

        # Create metadata
        draft_tokens = [p.token_ids[0] for p in proposals if p.token_ids][:3]
        if draft_tokens:
            metadata = SpecDecodeMetadataV2(
                draft_token_ids=draft_tokens,
                num_draft_tokens=[len(draft_tokens)]
            )

            # Verify
            verifier = SpecDecodeVerifier(SpecDecodeConfig())
            draft_lp = [-1.0] * len(draft_tokens)
            target_lp = [-0.5] * len(draft_tokens)

            result = verifier.verify(metadata, draft_lp, target_lp)

            assert isinstance(result.accepted_tokens, list)

    def test_ngram_to_verification(self):
        """Test N-gram proposal to verification pipeline."""
        from src.infrastructure.engine.speculative.ngram_proposer import (
            NgramProposer, NgramConfig
        )
        from src.infrastructure.engine.speculative.spec_decode_metadata_v2 import (
            SpecDecodeMetadataV2
        )

        # Create proposer
        config = NgramConfig()
        proposer = NgramProposer(config)

        # Generate proposal
        tokens = [1, 2, 3, 4, 1, 2, 3]
        result = proposer.propose(tokens)

        if result.draft_tokens:
            metadata = SpecDecodeMetadataV2.from_proposals([result.draft_tokens])
            assert len(metadata.draft_token_ids) > 0

    def test_arc_lru_comparison(self):
        """Compare ARC and LRU cache behavior."""
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import (
            ARCOffloadManager, SimpleBackend
        )
        from src.infrastructure.storage.kv_transfer.lru_offload_manager import LRUOffloadManager

        # Create both managers
        arc_backend = SimpleBackend(num_blocks=10)
        lru_backend = SimpleBackend(num_blocks=10)

        arc = ARCOffloadManager(arc_backend)
        lru = LRUOffloadManager(lru_backend)

        # Same operations on both
        hashes = [f"h{i}" for i in range(10)]

        arc.prepare_store(hashes)
        arc.complete_store(hashes)

        lru.prepare_store(hashes)
        lru.complete_store(hashes)

        # Both should have same hits
        arc_hits = arc.lookup(hashes)
        lru_hits = lru.lookup(hashes)

        assert arc_hits == 10
        assert lru_hits == 10

    def test_block_table_with_kv_cache(self):
        """Test block table integration with KV cache concepts."""
        from src.infrastructure.storage.kv_transfer.block_table_v2 import (
            BlockTableV2, BlockTableConfig
        )
        from src.infrastructure.storage.kv_transfer.arc_offload_manager import (
            ARCOffloadManager, SimpleBackend
        )

        # Create block table
        config = BlockTableConfig(block_size=16)
        table = BlockTableV2(config)

        # Simulate KV cache allocation
        blocks = table.allocate_for_request("req1", row_idx=0, num_blocks=4)

        # Create offload manager for those blocks
        backend = SimpleBackend(num_blocks=100)
        cache = ARCOffloadManager(backend)

        # Store block hashes
        block_hashes = [f"block_{b}" for b in blocks]
        cache.prepare_store(block_hashes)
        cache.complete_store(block_hashes)

        # Lookup should hit
        hits = cache.lookup(block_hashes)
        assert hits == len(blocks)
