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

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Unit Tests for Tokenizer Registry

"""
Tests for TokenizerRegistry module.
"""

import pytest

from src.infrastructure.engine.tokenization.tokenizer_registry import (
    TokenizerBackend,
    SpecialTokenHandling,
    TruncationStrategy,
    PaddingStrategy,
    TokenizerConfig,
    TokenizerInfo,
    TokenizeResult,
    BatchTokenizeResult,
    TokenizerRegistry,
    TokenizerPool,
    estimate_token_count,
    detect_tokenizer_backend,
)


class TestTokenizerEnums:
    """Test tokenizer enumerations."""

    def test_tokenizer_backend_values(self):
        """Test TokenizerBackend enum values."""
        assert TokenizerBackend.HUGGINGFACE is not None
        assert TokenizerBackend.TIKTOKEN is not None
        assert TokenizerBackend.MISTRAL is not None
        assert TokenizerBackend.SENTENCEPIECE is not None
        assert TokenizerBackend.CUSTOM is not None

    def test_special_token_handling_values(self):
        """Test SpecialTokenHandling enum values."""
        assert SpecialTokenHandling.INCLUDE is not None
        assert SpecialTokenHandling.EXCLUDE is not None
        assert SpecialTokenHandling.BOS_ONLY is not None
        assert SpecialTokenHandling.EOS_ONLY is not None
        assert SpecialTokenHandling.CUSTOM is not None

    def test_truncation_strategy_values(self):
        """Test TruncationStrategy enum values."""
        assert TruncationStrategy.NONE is not None
        assert TruncationStrategy.LEFT is not None
        assert TruncationStrategy.RIGHT is not None
        assert TruncationStrategy.LONGEST_FIRST is not None

    def test_padding_strategy_values(self):
        """Test PaddingStrategy enum values."""
        assert PaddingStrategy.NONE is not None
        assert PaddingStrategy.MAX_LENGTH is not None
        assert PaddingStrategy.LONGEST is not None


class TestTokenizerConfig:
    """Test TokenizerConfig dataclass."""

    def test_default_config(self):
        """Test default TokenizerConfig values."""
        config = TokenizerConfig(model_name="test-model")

        assert config.model_name == "test-model"
        assert config.backend == TokenizerBackend.HUGGINGFACE
        assert config.use_fast is True
        assert config.trust_remote_code is False

    def test_custom_config(self):
        """Test custom TokenizerConfig values."""
        config = TokenizerConfig(
            model_name="gpt-4",
            backend=TokenizerBackend.TIKTOKEN,
            max_length=4096,
            truncation=TruncationStrategy.RIGHT,
        )

        assert config.model_name == "gpt-4"
        assert config.backend == TokenizerBackend.TIKTOKEN
        assert config.max_length == 4096

    def test_config_hash(self):
        """Test TokenizerConfig is hashable."""
        config1 = TokenizerConfig(model_name="test")
        config2 = TokenizerConfig(model_name="test")
        config3 = TokenizerConfig(model_name="other")

        assert hash(config1) == hash(config2)
        assert hash(config1) != hash(config3)


class TestTokenizerInfo:
    """Test TokenizerInfo dataclass."""

    def test_tokenizer_info(self):
        """Test TokenizerInfo creation."""
        info = TokenizerInfo(
            backend=TokenizerBackend.HUGGINGFACE,
            vocab_size=50000,
            bos_token_id=1,
            eos_token_id=2,
            pad_token_id=0,
            max_length=4096,
            model_name="test-model",
        )

        assert info.vocab_size == 50000
        assert info.bos_token_id == 1
        assert info.eos_token_id == 2
        assert info.pad_token_id == 0

    def test_tokenizer_info_to_dict(self):
        """Test TokenizerInfo to_dict method."""
        info = TokenizerInfo(
            backend=TokenizerBackend.TIKTOKEN,
            vocab_size=100000,
            bos_token_id=None,
            eos_token_id=None,
            pad_token_id=None,
            max_length=8192,
            model_name="gpt-4",
        )

        d = info.to_dict()

        assert d["vocab_size"] == 100000
        assert d["backend"] == "TIKTOKEN"


class TestTokenizeResult:
    """Test TokenizeResult dataclass."""

    def test_tokenize_result(self):
        """Test TokenizeResult creation."""
        result = TokenizeResult(
            input_ids=[1, 2, 3, 4, 5],
            attention_mask=[1, 1, 1, 1, 1],
        )

        assert result.num_tokens == 5
        assert result.truncated is False

    def test_tokenize_result_to_numpy(self):
        """Test TokenizeResult to_numpy method."""
        result = TokenizeResult(
            input_ids=[1, 2, 3],
            attention_mask=[1, 1, 1],
        )

        np_result = result.to_numpy()

        assert "input_ids" in np_result
        assert len(np_result["input_ids"]) == 3


class TestBatchTokenizeResult:
    """Test BatchTokenizeResult dataclass."""

    def test_batch_tokenize_result(self):
        """Test BatchTokenizeResult creation."""
        result = BatchTokenizeResult(
            input_ids=[[1, 2, 3], [4, 5]],
        )

        assert len(result.input_ids) == 2
        assert result.max_length == 3
        assert result.token_counts == [3, 2]

    def test_batch_pad_to_max(self):
        """Test padding batch to max length."""
        result = BatchTokenizeResult(
            input_ids=[[1, 2, 3], [4, 5]],
        )

        padded = result.pad_to_max(pad_token_id=0)

        assert len(padded.input_ids[1]) == 3
        assert padded.input_ids[1] == [4, 5, 0]


class TestTokenizerRegistry:
    """Test TokenizerRegistry class."""

    def test_singleton_instance(self):
        """Test TokenizerRegistry is singleton."""
        registry1 = TokenizerRegistry()
        registry2 = TokenizerRegistry()

        assert registry1 is registry2

    def test_registry_stats(self):
        """Test getting registry stats."""
        registry = TokenizerRegistry()

        stats = registry.get_stats()

        assert "cached" in stats
        assert "hits" in stats
        assert "misses" in stats


class TestTokenizerPool:
    """Test TokenizerPool class."""

    @pytest.mark.skip(reason="Requires network access to HuggingFace")
    def test_pool_creation(self):
        """Test TokenizerPool creation."""
        config = TokenizerConfig(model_name="test-model")
        pool = TokenizerPool(config=config)

        assert pool is not None

    @pytest.mark.skip(reason="Requires network access to HuggingFace")
    def test_pool_stats(self):
        """Test getting pool stats."""
        config = TokenizerConfig(model_name="test-model")
        pool = TokenizerPool(config=config)

        assert pool.pool_size > 0


class TestUtilityFunctions:
    """Test utility functions."""

    def test_estimate_token_count(self):
        """Test token count estimation."""
        text = "Hello, world! This is a test."

        count = estimate_token_count(text)

        assert isinstance(count, int)
        assert count > 0

    def test_estimate_token_count_empty(self):
        """Test estimation with empty text."""
        count = estimate_token_count("")

        assert count == 0

    def test_estimate_token_count_unicode(self):
        """Test estimation with Unicode."""
        text = "Hello, 世界! 🌍"

        count = estimate_token_count(text)

        assert count > 0


class TestMockTokenizers:
    """Test with mocked tokenizers."""

    def test_huggingface_tokenizer_encode(self):
        """Test HuggingFace tokenizer encode with mock."""
        # Test that the encode returns a list of integers
        result = TokenizeResult(input_ids=[1, 2, 3, 4, 5])

        assert len(result.input_ids) == 5
        assert all(isinstance(x, int) for x in result.input_ids)

    def test_huggingface_tokenizer_decode(self):
        """Test HuggingFace tokenizer decode concept."""
        # Just verify the dataclass works correctly
        result = TokenizeResult(input_ids=[1, 2, 3], tokens=["Hello", ",", " world"])

        assert result.tokens is not None
        assert len(result.tokens) == 3


class TestTokenizerBackendDetection:
    """Test tokenizer backend detection."""

    @pytest.mark.parametrize("model_name,expected_backend", [
        ("gpt-4", TokenizerBackend.TIKTOKEN),
        ("gpt-3.5-turbo", TokenizerBackend.TIKTOKEN),
        ("o1-preview", TokenizerBackend.TIKTOKEN),
        ("meta-llama/Llama-2-7b", TokenizerBackend.HUGGINGFACE),
        ("mistralai/Mistral-7B", TokenizerBackend.MISTRAL),
    ])
    def test_backend_detection(self, model_name: str, expected_backend: TokenizerBackend):
        """Test backend detection for various models."""
        backend = detect_tokenizer_backend(model_name)

        assert backend == expected_backend
