"""
Phase 44: Advanced Sampling & Speculative Decoding Tests
Tests for Rust-accelerated sampling and speculative decoding functions.
"""

import pytest
import random
import math

# Try to import rust_core
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False
    rust_core = None


pytestmark = pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")


class TestRejectionSampling:
    """Test rejection sampling verification."""

    def test_all_tokens_accepted(self):
        """Test when all draft tokens are accepted."""
        draft_tokens = [1, 2, 0]
        # Draft and target have same probabilities - accept_prob = 1.0
        draft_probs = [[0.1, 0.8, 0.1], [0.1, 0.1, 0.8], [0.8, 0.1, 0.1]]
        target_probs = [[0.1, 0.8, 0.1], [0.1, 0.1, 0.8], [0.8, 0.1, 0.1]]
        random_nums = [0.1, 0.1, 0.1]  # All below 1.0 accept threshold

        accepted, recovered, all_accepted = rust_core.rejection_sample_verify_rust(
            draft_tokens, draft_probs, target_probs, random_nums
        )

        # When p_target == p_draft, accept_prob = 1.0
        assert accepted == 3
        assert all_accepted is True

    def test_first_token_rejected(self):
        """Test when first token is rejected."""
        draft_tokens = [0]
        draft_probs = [[0.9, 0.1]]  # Draft confident
        target_probs = [[0.1, 0.9]]  # Target disagrees
        random_nums = [0.5]  # Above accept_prob = 0.1/0.9 ≈ 0.11

        accepted, recovered, all_accepted = rust_core.rejection_sample_verify_rust(
            draft_tokens, draft_probs, target_probs, random_nums
        )

        assert all_accepted is False
        assert accepted == 0
        assert recovered is not None

    def test_partial_acceptance(self):
        """Test partial token acceptance."""
        draft_tokens = [0, 1]
        draft_probs = [
            [0.5, 0.5],  # Token 0: accept prob = 1.0 (same)
            [0.9, 0.1],  # Token 1: draft confident, target disagrees
        ]
        target_probs = [
            [0.5, 0.5],  # Same as draft - accept
            [0.1, 0.9],  # Target disagrees - may reject
        ]
        random_nums = [0.1, 0.5]  # First accepts, second likely rejects

        accepted, recovered, all_accepted = rust_core.rejection_sample_verify_rust(
            draft_tokens, draft_probs, target_probs, random_nums
        )

        # First token should be accepted, second may or may not be
        assert accepted >= 1  # At least first token accepted

    def test_empty_input(self):
        """Test with empty input."""
        accepted, recovered, all_accepted = rust_core.rejection_sample_verify_rust(
            [], [], [], []
        )

        assert accepted == 0
        assert recovered is None
        assert all_accepted is False


class TestTopKSampling:
    """Test top-k filtering."""

    def test_top_k_basic(self):
        """Test basic top-k filtering."""
        logits = [[1.0, 2.0, 3.0, 4.0, 5.0]]
        k = 2

        result = rust_core.apply_top_k_rust(logits, k)

        # Top 2 values (5.0, 4.0) should remain
        assert result[0][4] == 5.0
        assert result[0][3] == 4.0
        # Others should be -inf
        assert result[0][0] == float('-inf')
        assert result[0][1] == float('-inf')
        assert result[0][2] == float('-inf')

    def test_top_k_zero_passthrough(self):
        """Test k=0 passes through unchanged."""
        logits = [[1.0, 2.0, 3.0]]

        result = rust_core.apply_top_k_rust(logits, 0)

        assert result == logits

    def test_top_k_larger_than_vocab(self):
        """Test k larger than vocab size."""
        logits = [[1.0, 2.0, 3.0]]

        result = rust_core.apply_top_k_rust(logits, 10)

        assert result == logits


class TestTopPSampling:
    """Test top-p (nucleus) filtering."""

    def test_top_p_basic(self):
        """Test basic top-p filtering."""
        # Large difference so softmax gives clear probabilities
        logits = [[0.0, 0.0, 10.0]]  # Token 2 has very high prob

        result = rust_core.apply_top_p_rust(logits, 0.5)

        # Token 2 should remain (has majority of probability mass)
        assert result[0][2] == 10.0

    def test_top_p_one_passthrough(self):
        """Test p=1.0 passes through unchanged."""
        logits = [[1.0, 2.0, 3.0]]

        result = rust_core.apply_top_p_rust(logits, 1.0)

        assert result == logits

    def test_top_p_cumulative(self):
        """Test cumulative probability cutoff."""
        # Uniform logits
        logits = [[0.0, 0.0, 0.0, 0.0]]

        result = rust_core.apply_top_p_rust(logits, 0.5)

        # Should keep roughly half (due to cumulative)
        valid_count = sum(1 for v in result[0] if v > float('-inf'))
        assert valid_count >= 1


class TestBatchTopKTopPSampling:
    """Test batch top-k/top-p sampling."""

    def test_batch_sample_basic(self):
        """Test basic batch sampling."""
        logits = [
            [0.0, 0.0, 10.0],  # Token 2 dominant
            [10.0, 0.0, 0.0],  # Token 0 dominant
        ]
        temperatures = [1.0, 1.0]
        top_ks = [2, 2]
        top_ps = [0.9, 0.9]

        result = rust_core.batch_topk_topp_sample_rust(logits, temperatures, top_ks, top_ps)

        assert len(result) == 2
        # Dominant tokens should be selected
        assert result[0] == 2
        assert result[1] == 0

    def test_batch_sample_temperature(self):
        """Test temperature scaling."""
        logits = [
            [0.0, 1.0, 2.0],
        ]
        temperatures = [0.01]  # Very low temp = argmax
        top_ks = [0]
        top_ps = [1.0]

        result = rust_core.batch_topk_topp_sample_rust(logits, temperatures, top_ks, top_ps)

        assert result[0] == 2  # Argmax

    def test_batch_sample_empty(self):
        """Test empty batch."""
        result = rust_core.batch_topk_topp_sample_rust([], [], [], [])

        assert result == []


class TestBatchApplyPenalties:
    """Test penalty application."""

    def test_repetition_penalty(self):
        """Test repetition penalty application."""
        logits = [[1.0, 2.0, 3.0]]
        rep_penalties = [2.0]  # Divide positive logits by 2
        freq_penalties = [0.0]
        pres_penalties = [0.0]
        prompt_tokens = [[0, 1]]  # Tokens 0, 1 in prompt
        output_tokens = [[]]

        result = rust_core.batch_apply_penalties_rust(
            logits, rep_penalties, freq_penalties, pres_penalties,
            prompt_tokens, output_tokens
        )

        # Tokens 0, 1 should be penalized
        assert result[0][0] < 1.0  # Was 1.0, divided by 2
        assert result[0][1] < 2.0  # Was 2.0, divided by 2
        assert result[0][2] == 3.0  # Unchanged

    def test_frequency_penalty(self):
        """Test frequency penalty."""
        logits = [[5.0, 5.0, 5.0]]
        rep_penalties = [1.0]
        freq_penalties = [1.0]  # Subtract count
        pres_penalties = [0.0]
        prompt_tokens = [[]]
        output_tokens = [[0, 0, 1]]  # Token 0 appears twice, 1 once

        result = rust_core.batch_apply_penalties_rust(
            logits, rep_penalties, freq_penalties, pres_penalties,
            prompt_tokens, output_tokens
        )

        assert result[0][0] == 3.0  # 5.0 - 2*1.0
        assert result[0][1] == 4.0  # 5.0 - 1*1.0
        assert result[0][2] == 5.0  # Unchanged

    def test_presence_penalty(self):
        """Test presence penalty."""
        logits = [[5.0, 5.0, 5.0]]
        rep_penalties = [1.0]
        freq_penalties = [0.0]
        pres_penalties = [2.0]  # Subtract 2 if present
        prompt_tokens = [[0]]
        output_tokens = [[1]]

        result = rust_core.batch_apply_penalties_rust(
            logits, rep_penalties, freq_penalties, pres_penalties,
            prompt_tokens, output_tokens
        )

        assert result[0][0] == 3.0  # Present in prompt
        assert result[0][1] == 3.0  # Present in output
        assert result[0][2] == 5.0  # Not present


class TestNgramProposal:
    """Test n-gram based token proposal."""

    def test_ngram_propose_match(self):
        """Test n-gram proposal with matching suffix."""
        tokens = [1, 2, 3, 1, 2]  # Suffix [1, 2] matches earlier
        min_n = 2
        max_n = 3
        k = 2

        result = rust_core.advanced_ngram_propose_rust(tokens, min_n, max_n, k)

        # Should propose continuation after [1, 2] which is [3]
        assert len(result) > 0
        assert result[0] == 3

    def test_ngram_propose_no_match(self):
        """Test n-gram proposal with no match."""
        tokens = [1, 2, 3, 4, 5]  # No repeated patterns
        min_n = 2
        max_n = 3
        k = 2

        result = rust_core.advanced_ngram_propose_rust(tokens, min_n, max_n, k)

        assert result == []

    def test_ngram_propose_empty(self):
        """Test n-gram proposal with empty input."""
        result = rust_core.advanced_ngram_propose_rust([], 2, 3, 2)

        assert result == []


class TestEncoderCacheHash:
    """Test encoder content hashing."""

    def test_content_hash_basic(self):
        """Test basic content hashing."""
        data = b"test content"

        result = rust_core.encoder_content_hash_rust(list(data))

        assert isinstance(result, str)
        assert len(result) == 16  # 16 hex chars

    def test_content_hash_deterministic(self):
        """Test hash is deterministic."""
        data = list(b"same content")

        result1 = rust_core.encoder_content_hash_rust(data)
        result2 = rust_core.encoder_content_hash_rust(data)

        assert result1 == result2

    def test_content_hash_different(self):
        """Test different content gives different hash."""
        result1 = rust_core.encoder_content_hash_rust(list(b"content a"))
        result2 = rust_core.encoder_content_hash_rust(list(b"content b"))

        assert result1 != result2


class TestEncoderCacheLRUEvict:
    """Test LRU eviction for encoder cache."""

    def test_lru_evict_basic(self):
        """Test basic LRU eviction."""
        keys = ["a", "b", "c", "d"]
        last_access = [1.0, 3.0, 2.0, 4.0]  # a oldest, d newest
        ref_counts = [0, 0, 0, 0]
        num_to_evict = 2

        result = rust_core.encoder_cache_lru_evict_rust(
            keys, last_access, ref_counts, num_to_evict
        )

        assert len(result) == 2
        assert "a" in result  # Oldest
        assert "c" in result  # Second oldest

    def test_lru_evict_prefer_unreferenced(self):
        """Test eviction prefers unreferenced entries."""
        keys = ["a", "b", "c"]
        last_access = [1.0, 2.0, 3.0]
        ref_counts = [1, 0, 0]  # a is referenced
        num_to_evict = 2

        result = rust_core.encoder_cache_lru_evict_rust(
            keys, last_access, ref_counts, num_to_evict
        )

        assert len(result) == 2
        # Should evict unreferenced first
        assert "b" in result
        assert "c" in result

    def test_lru_evict_empty(self):
        """Test eviction with empty input."""
        result = rust_core.encoder_cache_lru_evict_rust([], [], [], 2)

        assert result == []


class TestKVCacheMetricsAggregate:
    """Test KV cache metrics aggregation."""

    def test_metrics_aggregate_basic(self):
        """Test basic metrics aggregation."""
        lifetimes = [1.0, 2.0, 3.0, 4.0, 5.0]
        idle_times = [0.1, 0.2, 0.3, 0.4, 0.5]
        access_counts = [1, 2, 0, 3, 1]

        result = rust_core.kv_cache_metrics_aggregate_rust(
            lifetimes, idle_times, access_counts
        )

        assert "mean_lifetime" in result
        assert "p50_lifetime" in result
        assert "p95_lifetime" in result
        assert "mean_idle" in result
        assert "mean_access_count" in result
        assert "zero_access_rate" in result

        assert result["mean_lifetime"] == 3.0
        assert result["zero_access_rate"] == 0.2  # 1/5

    def test_metrics_aggregate_empty(self):
        """Test with empty input."""
        result = rust_core.kv_cache_metrics_aggregate_rust([], [], [])

        assert result == {}


class TestTypicalSampling:
    """Test typical sampling (entropy-based)."""

    def test_typical_sampling_basic(self):
        """Test basic typical sampling."""
        logits = [[0.0, 0.0, 10.0]]  # Token 2 dominant

        result = rust_core.apply_typical_sampling_rust(logits, 0.9)

        # Token 2 should remain (closest to entropy)
        assert result[0][2] == 10.0

    def test_typical_sampling_uniform(self):
        """Test typical sampling on uniform distribution."""
        logits = [[0.0, 0.0, 0.0, 0.0]]

        result = rust_core.apply_typical_sampling_rust(logits, 0.5)

        # Should keep some tokens
        valid_count = sum(1 for v in result[0] if v > float('-inf'))
        assert valid_count >= 1


class TestMinPSampling:
    """Test min-P sampling."""

    def test_min_p_basic(self):
        """Test basic min-P sampling."""
        logits = [[0.0, 0.0, 10.0]]  # Token 2 has ~1.0 prob after softmax

        result = rust_core.apply_min_p_rust(logits, 0.5)

        # Token 2 should remain, others masked
        assert result[0][2] == 10.0

    def test_min_p_zero_passthrough(self):
        """Test min_p=0 passes through unchanged."""
        logits = [[1.0, 2.0, 3.0]]

        result = rust_core.apply_min_p_rust(logits, 0.0)

        assert result == logits


class TestGumbelNoise:
    """Test Gumbel noise generation."""

    def test_gumbel_noise_shape(self):
        """Test Gumbel noise shape."""
        result = rust_core.gumbel_noise_rust((3, 5), 42)

        assert len(result) == 3
        assert len(result[0]) == 5

    def test_gumbel_noise_deterministic(self):
        """Test Gumbel noise is deterministic with same seed."""
        result1 = rust_core.gumbel_noise_rust((2, 3), 42)
        result2 = rust_core.gumbel_noise_rust((2, 3), 42)

        assert result1 == result2

    def test_gumbel_noise_different_seeds(self):
        """Test different seeds give different noise."""
        result1 = rust_core.gumbel_noise_rust((2, 3), 42)
        result2 = rust_core.gumbel_noise_rust((2, 3), 43)

        assert result1 != result2


class TestIntegration:
    """Integration tests combining multiple Phase 44 functions."""

    def test_sampling_pipeline(self):
        """Test complete sampling pipeline."""
        batch_size = 2
        vocab_size = 100

        # Generate random logits
        random.seed(42)
        logits = [
            [random.gauss(0, 1) for _ in range(vocab_size)]
            for _ in range(batch_size)
        ]

        # Apply penalties
        penalized = rust_core.batch_apply_penalties_rust(
            logits,
            [1.2, 1.1],  # repetition
            [0.1, 0.2],  # frequency
            [0.1, 0.1],  # presence
            [[0, 1, 2], [3, 4]],  # prompt
            [[5, 5, 6], [7]],  # output
        )

        # Apply top-k
        top_k_filtered = rust_core.apply_top_k_rust(penalized, 50)

        # Apply top-p
        top_p_filtered = rust_core.apply_top_p_rust(top_k_filtered, 0.9)

        # Sample
        tokens = rust_core.batch_topk_topp_sample_rust(
            top_p_filtered,
            [0.8, 0.7],  # temperatures
            [0, 0],  # k already applied
            [1.0, 1.0],  # p already applied
        )

        assert len(tokens) == batch_size
        assert all(0 <= t < vocab_size for t in tokens)

    def test_speculative_decoding_pipeline(self):
        """Test speculative decoding verification pipeline."""
        vocab_size = 10
        num_drafts = 3

        # Generate draft and target distributions
        random.seed(42)
        draft_tokens = [random.randint(0, vocab_size - 1) for _ in range(num_drafts)]

        def make_probs():
            raw = [random.random() for _ in range(vocab_size)]
            total = sum(raw)
            return [p / total for p in raw]

        draft_probs = [make_probs() for _ in range(num_drafts)]
        target_probs = [make_probs() for _ in range(num_drafts)]
        random_nums = [random.random() for _ in range(num_drafts)]

        accepted, recovered, all_accepted = rust_core.rejection_sample_verify_rust(
            draft_tokens, draft_probs, target_probs, random_nums
        )

        assert 0 <= accepted <= num_drafts
        assert isinstance(all_accepted, bool)
        if not all_accepted:
            assert recovered is not None or accepted == num_drafts

    def test_cache_management_pipeline(self):
        """Test cache management pipeline."""
        # Generate cache entries
        entries = ["entry_a", "entry_b", "entry_c", "entry_d", "entry_e"]
        access_times = [1.0, 5.0, 3.0, 2.0, 4.0]
        ref_counts = [0, 1, 0, 0, 1]

        # Evict 2 entries
        to_evict = rust_core.encoder_cache_lru_evict_rust(
            entries, access_times, ref_counts, 2
        )

        assert len(to_evict) == 2

        # Compute content hash
        content = list(b"sample image data")
        hash_key = rust_core.encoder_content_hash_rust(content)
        assert len(hash_key) == 16

    def test_metrics_collection(self):
        """Test metrics collection pipeline."""
        # Simulate block lifetimes
        lifetimes = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        idle_times = [0.1, 0.2, 0.1, 0.3, 0.2, 0.1]
        access_counts = [5, 3, 0, 2, 1, 4]

        metrics = rust_core.kv_cache_metrics_aggregate_rust(
            lifetimes, idle_times, access_counts
        )

        assert metrics["mean_lifetime"] == sum(lifetimes) / len(lifetimes)
        assert 0 <= metrics["zero_access_rate"] <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
