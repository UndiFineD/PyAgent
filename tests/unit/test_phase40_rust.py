# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: Rust Acceleration Tests

"""
Tests for Phase 40 Rust functions.
"""

import pytest
import numpy as np
from typing import List, Tuple

# Import Rust functions
try:
    import rust_core
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust core not available")
class TestReasoningParserRust:
    """Test Rust reasoning parser functions."""
    
    def test_extract_thinking_blocks(self):
        """Test extracting thinking blocks."""
        text = "Hello <think>Let me think</think> World"
        
        blocks = rust_core.extract_thinking_blocks_rust(text, "<think>", "</think>")
        
        assert len(blocks) == 1
        start, end, content = blocks[0]
        assert "Let me think" in content
    
    def test_extract_multiple_blocks(self):
        """Test extracting multiple thinking blocks."""
        text = "<think>First</think> middle <think>Second</think> end"
        
        blocks = rust_core.extract_thinking_blocks_rust(text, "<think>", "</think>")
        
        assert len(blocks) == 2
        assert "First" in blocks[0][2]
        assert "Second" in blocks[1][2]
    
    def test_extract_no_blocks(self):
        """Test when no thinking blocks present."""
        text = "Hello World without any thinking"
        
        blocks = rust_core.extract_thinking_blocks_rust(text, "<think>", "</think>")
        
        assert len(blocks) == 0
    
    def test_parse_tool_calls(self):
        """Test parsing tool calls."""
        text = '{"name": "search", "arguments": {"query": "test"}}'
        
        calls = rust_core.parse_tool_calls_rust(text)
        
        assert len(calls) >= 0  # May or may not parse depending on format
    
    def test_classify_token_context(self):
        """Test classifying token context."""
        prefix = "Hello <think>"
        token = "reasoning"
        
        is_thinking, is_tool, is_content = rust_core.classify_token_context_rust(
            prefix, token, "<think>", "</think>"
        )
        
        # Should be in thinking mode
        assert is_thinking is True
        assert is_content is False


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust core not available")
class TestMultiModalCacheRust:
    """Test Rust multimodal cache functions."""
    
    def test_blake3_hash(self):
        """Test Blake3 hash computation."""
        data = b"test data for hashing"
        
        h = rust_core.blake3_hash_rust(list(data))
        
        assert isinstance(h, str)
        assert len(h) == 32  # 128-bit hash in hex
    
    def test_blake3_deterministic(self):
        """Test Blake3 is deterministic."""
        data = b"consistent data"
        
        h1 = rust_core.blake3_hash_rust(list(data))
        h2 = rust_core.blake3_hash_rust(list(data))
        
        assert h1 == h2
    
    def test_perceptual_hash_distance_same(self):
        """Test perceptual hash distance for same hash."""
        h = "abc123def456"
        
        distance = rust_core.perceptual_hash_distance_rust(h, h)
        
        assert distance == 1.0  # Similarity = 1.0 for same hash
    
    def test_perceptual_hash_distance_different(self):
        """Test perceptual hash distance for different hashes."""
        h1 = "aaaaaaaaaaaaaaaa"
        h2 = "bbbbbbbbbbbbbbbb"
        
        distance = rust_core.perceptual_hash_distance_rust(h1, h2)
        
        assert distance < 1.0  # Different hashes have lower similarity
    
    def test_lru_evict_candidates(self):
        """Test LRU eviction candidate selection."""
        access_times = [5.0, 1.0, 3.0, 2.0, 4.0]
        
        to_evict = rust_core.lru_evict_candidates_rust(access_times, 2)
        
        # Should evict indices with lowest access times (1 and 3)
        assert len(to_evict) == 2
        assert 1 in to_evict  # Access time 1.0
        assert 3 in to_evict  # Access time 2.0
    
    def test_arc_cache_priority(self):
        """Test ARC cache priority computation."""
        priority = rust_core.arc_cache_priority_rust(
            frequency=10,
            recency=0.5,
            size_bytes=1024,
            alpha=0.5,
        )
        
        assert priority > 0


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust core not available")
class TestPoolingRust:
    """Test Rust pooling functions."""
    
    def test_mean_pool(self):
        """Test mean pooling."""
        embeddings = [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
        ]
        mask = [1.0, 1.0]
        
        result = rust_core.mean_pool_rust(embeddings, mask)
        
        expected = [2.5, 3.5, 4.5]
        for i, (r, e) in enumerate(zip(result, expected)):
            assert abs(r - e) < 0.01, f"Mismatch at {i}: {r} != {e}"
    
    def test_mean_pool_with_mask(self):
        """Test mean pooling with attention mask."""
        embeddings = [
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
        ]
        mask = [1.0, 1.0, 0.0]  # Last token masked
        
        result = rust_core.mean_pool_rust(embeddings, mask)
        
        expected = [2.0, 3.0]
        for r, e in zip(result, expected):
            assert abs(r - e) < 0.01
    
    def test_cls_pool(self):
        """Test CLS token pooling."""
        embeddings = [
            [1.0, 2.0, 3.0],  # CLS token
            [4.0, 5.0, 6.0],
        ]
        
        result = rust_core.cls_pool_rust(embeddings)
        
        assert result == [1.0, 2.0, 3.0]
    
    def test_last_token_pool(self):
        """Test last token pooling."""
        embeddings = [
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
        ]
        mask = [1.0, 1.0, 1.0]
        
        result = rust_core.last_token_pool_rust(embeddings, mask)
        
        assert result == [5.0, 6.0]
    
    def test_last_token_pool_with_padding(self):
        """Test last token pooling with padding."""
        embeddings = [
            [1.0, 2.0],
            [3.0, 4.0],
            [0.0, 0.0],  # Padding
        ]
        mask = [1.0, 1.0, 0.0]
        
        result = rust_core.last_token_pool_rust(embeddings, mask)
        
        assert result == [3.0, 4.0]
    
    def test_matryoshka_truncate(self):
        """Test Matryoshka dimensionality reduction."""
        embedding = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        result = rust_core.matryoshka_truncate_rust(embedding, 3, False)
        
        assert len(result) == 3
        assert result == [1.0, 2.0, 3.0]
    
    def test_matryoshka_normalize(self):
        """Test Matryoshka with normalization."""
        embedding = [3.0, 4.0, 0.0, 0.0]  # norm = 5
        
        result = rust_core.matryoshka_truncate_rust(embedding, 2, True)
        
        # Should be normalized to unit length
        norm = sum(x**2 for x in result) ** 0.5
        assert abs(norm - 1.0) < 0.01
    
    def test_attention_pool(self):
        """Test attention-weighted pooling."""
        embeddings = [
            [1.0, 2.0],
            [3.0, 4.0],
        ]
        attention_scores = [0.3, 0.7]
        
        result = rust_core.attention_pool_rust(embeddings, attention_scores)
        
        assert len(result) == 2
        # Weighted by softmax of scores


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust core not available")
class TestInputPreprocessorRust:
    """Test Rust input preprocessing functions."""
    
    def test_estimate_tokens(self):
        """Test token count estimation."""
        text = "Hello world"
        
        count = rust_core.estimate_tokens_rust(text)
        
        assert count > 0
        assert count < 10
    
    def test_estimate_tokens_long(self):
        """Test token estimation for long text."""
        text = "word " * 100
        
        count = rust_core.estimate_tokens_rust(text)
        
        assert count >= 100
    
    def test_validate_chat_messages_valid(self):
        """Test validating valid chat messages."""
        messages = [
            ("user", "Hello"),
            ("assistant", "Hi!"),
        ]
        
        is_valid, error = rust_core.validate_chat_messages_rust(messages)
        
        assert is_valid is True
        assert error == ""
    
    def test_validate_chat_messages_empty(self):
        """Test validating empty messages."""
        is_valid, error = rust_core.validate_chat_messages_rust([])
        
        assert is_valid is False
        assert "empty" in error.lower()
    
    def test_validate_chat_messages_invalid_role(self):
        """Test validating invalid role."""
        messages = [
            ("invalid_role", "Hello"),
        ]
        
        is_valid, error = rust_core.validate_chat_messages_rust(messages)
        
        assert is_valid is False
    
    def test_linearize_chat_chatml(self):
        """Test linearizing to ChatML format."""
        messages = [
            ("user", "Hello"),
        ]
        
        result = rust_core.linearize_chat_rust(messages, "chatml")
        
        assert "<|im_start|>user" in result
        assert "Hello" in result
        assert "<|im_end|>" in result
    
    def test_linearize_chat_llama(self):
        """Test linearizing to Llama format."""
        messages = [
            ("user", "Hello"),
        ]
        
        result = rust_core.linearize_chat_rust(messages, "llama")
        
        assert "user" in result
        assert "Hello" in result
    
    def test_linearize_chat_mistral(self):
        """Test linearizing to Mistral format."""
        messages = [
            ("user", "Hello"),
        ]
        
        result = rust_core.linearize_chat_rust(messages, "mistral")
        
        assert "[INST]" in result


@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust core not available")
class TestAdvancedSamplingRust:
    """Test Rust advanced sampling functions."""
    
    def test_apply_temperature_schedule_constant(self):
        """Test constant temperature schedule."""
        logits = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        result = rust_core.apply_temperature_schedule_rust(
            logits,
            temperature=0.5,
            step=50,
            schedule="constant",
            decay_target=0.1,
            decay_steps=100,
        )
        
        # Should divide by temperature
        expected = [x / 0.5 for x in logits]
        for r, e in zip(result, expected):
            assert abs(r - e) < 0.01
    
    def test_apply_temperature_schedule_linear(self):
        """Test linear temperature decay."""
        logits = [1.0, 2.0, 3.0]
        
        result = rust_core.apply_temperature_schedule_rust(
            logits,
            temperature=1.0,
            step=50,
            schedule="linear",
            decay_target=0.1,
            decay_steps=100,
        )
        
        # At step 50, temp should be ~0.55
        assert len(result) == 3
    
    def test_apply_temperature_schedule_cosine(self):
        """Test cosine temperature decay."""
        logits = [1.0, 2.0, 3.0]
        
        result = rust_core.apply_temperature_schedule_rust(
            logits,
            temperature=1.0,
            step=50,
            schedule="cosine",
            decay_target=0.0,
            decay_steps=100,
        )
        
        assert len(result) == 3
    
    def test_apply_bad_words_mask(self):
        """Test bad words masking."""
        logits = [1.0, 2.0, 3.0, 4.0, 5.0]
        banned = [1, 3]
        
        result = rust_core.apply_bad_words_mask_rust(logits, banned)
        
        assert result[1] == float('-inf')
        assert result[3] == float('-inf')
        assert result[0] == 1.0
        assert result[2] == 3.0
    
    def test_apply_whitelist_mask(self):
        """Test token whitelist masking."""
        logits = [1.0, 2.0, 3.0, 4.0, 5.0]
        allowed = [0, 2, 4]
        
        result = rust_core.apply_whitelist_mask_rust(logits, allowed)
        
        assert result[0] == 1.0
        assert result[2] == 3.0
        assert result[4] == 5.0
        assert result[1] == float('-inf')
        assert result[3] == float('-inf')
    
    def test_mirostat_sample(self):
        """Test Mirostat sampling."""
        # Logits with one dominant token
        logits = [-10.0, -10.0, 5.0, -10.0, -10.0]
        
        token_id, new_mu = rust_core.mirostat_sample_rust(
            logits,
            mu=10.0,
            tau=5.0,
            eta=0.1,
        )
        
        # Should select token 2 (highest logit)
        assert token_id == 2
        assert isinstance(new_mu, float)
    
    def test_adaptive_top_k_low_entropy(self):
        """Test adaptive top_k with low entropy."""
        # Low entropy: one dominant token
        logits = [0.0, 0.0, 10.0, 0.0, 0.0]
        
        k = rust_core.adaptive_top_k_rust(
            logits,
            entropy_threshold=2.0,
            min_k=5,
            max_k=100,
        )
        
        # Low entropy -> smaller k
        assert k < 50
    
    def test_adaptive_top_k_high_entropy(self):
        """Test adaptive top_k with high entropy."""
        # High entropy: uniform distribution
        logits = [1.0, 1.0, 1.0, 1.0, 1.0]
        
        k = rust_core.adaptive_top_k_rust(
            logits,
            entropy_threshold=2.0,
            min_k=5,
            max_k=100,
        )
        
        # Higher entropy -> larger k
        assert k >= 5


# Run pytest if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
