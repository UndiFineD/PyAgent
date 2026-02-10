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
# Phase 40: Pooling Engine Tests

"""
Tests for PoolingEngine - embedding pooling strategies.
"""

import pytest
import numpy as np

from src.infrastructure.engine.pooling.pooling_engine import (
    PoolingTask,
    PoolingStrategy,
    PoolingConfig,
    EmbeddingOutput,
    MeanPooler,
    CLSPooler,
    LastTokenPooler,
    MaxPooler,
    AttentionPooler,
    WeightedMeanPooler,
    MatryoshkaPooler,
    MultiVectorPooler,
    StepPooler,
    PoolingEngine,
    create_pooling_engine,
)

# Helper to create a default PoolingConfig
def default_config(strategy=PoolingStrategy.MEAN, normalize=True, truncate_dim=None):
    return PoolingConfig(strategy=strategy, normalize=normalize, truncate_dim=truncate_dim)


class TestEnums:
    """Test enum values."""

    def test_pooling_task_values(self):
        """Test PoolingTask enum."""
        assert PoolingTask.EMBED is not None
        assert PoolingTask.CLASSIFY is not None
        assert PoolingTask.SCORE is not None
        assert PoolingTask.RERANK is not None

    def test_pooling_strategy_values(self):
        """Test PoolingStrategy enum."""
        assert PoolingStrategy.MEAN is not None
        assert PoolingStrategy.CLS is not None
        assert PoolingStrategy.LAST is not None
        assert PoolingStrategy.MAX is not None
        assert PoolingStrategy.ATTENTION is not None


class TestPoolingConfig:
    """Test PoolingConfig dataclass."""

    def test_create_config(self):
        """Test creating PoolingConfig."""
        config = PoolingConfig(
            task=PoolingTask.EMBED,
            strategy=PoolingStrategy.MEAN,
        )
        assert config.task == PoolingTask.EMBED
        assert config.strategy == PoolingStrategy.MEAN

    def test_config_with_normalize(self):
        """Test config with normalize flag."""
        config = PoolingConfig(
            task=PoolingTask.EMBED,
            strategy=PoolingStrategy.CLS,
            normalize=True,
        )
        assert config.normalize is True


class TestEmbeddingOutput:
    """Test EmbeddingOutput dataclass."""

    def test_create_embedding_output(self):
        """Test creating EmbeddingOutput."""
        emb = np.array([0.1, 0.2, 0.3])
        output = EmbeddingOutput(embedding=emb, tokens_used=3)

        assert output.embedding is not None
        assert len(output.embedding) == 3

    def test_embedding_to_list(self):
        """Test embedding to_list method."""
        emb = np.array([0.1, 0.2])

        output = EmbeddingOutput(
            embedding=emb,
            tokens_used=2,
        )
        assert output.to_list() == [0.1, 0.2]


class TestMeanPooler:
    """Test mean pooling."""

    def test_mean_pool(self):
        """Test mean pooling computation."""
        config = PoolingConfig(strategy=PoolingStrategy.MEAN)
        pooler = MeanPooler(config)

        # Need 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.array([[
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
        ]])
        mask = np.array([[1.0, 1.0]])

        result = pooler.pool(embeddings, mask)

        expected = np.array([[2.5, 3.5, 4.5]])
        np.testing.assert_array_almost_equal(result, expected)

    def test_mean_pool_with_mask(self):
        """Test mean pooling with attention mask."""
        config = PoolingConfig(strategy=PoolingStrategy.MEAN)
        pooler = MeanPooler(config)

        # Need 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.array([[
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
        ]])
        mask = np.array([[1.0, 1.0, 0.0]])  # Last token masked

        result = pooler.pool(embeddings, mask)

        expected = np.array([[2.0, 3.0]])
        np.testing.assert_array_almost_equal(result, expected)


class TestCLSPooler:
    """Test CLS token pooling."""

    def test_cls_pool(self):
        """Test CLS pooling extracts first token."""
        config = PoolingConfig(strategy=PoolingStrategy.CLS)
        pooler = CLSPooler(config)

        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.array([[
            [1.0, 2.0, 3.0],  # CLS token
            [4.0, 5.0, 6.0],
        ]])

        result = pooler.pool(embeddings)

        expected = np.array([[1.0, 2.0, 3.0]])
        np.testing.assert_array_almost_equal(result, expected)


class TestLastTokenPooler:
    """Test last token pooling."""

    def test_last_token_pool(self):
        """Test last token pooling."""
        config = PoolingConfig(strategy=PoolingStrategy.LAST)
        pooler = LastTokenPooler(config)

        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.array([[
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],  # Last token
        ]])
        mask = np.array([[1.0, 1.0, 1.0]])

        result = pooler.pool(embeddings, mask)

        expected = np.array([[5.0, 6.0]])
        np.testing.assert_array_almost_equal(result, expected)

    def test_last_token_with_mask(self):
        """Test last token pooling with padded sequence."""
        config = PoolingConfig(strategy=PoolingStrategy.LAST)
        pooler = LastTokenPooler(config)

        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.array([[
            [1.0, 2.0],
            [3.0, 4.0],  # Actual last token
            [0.0, 0.0],  # Padding
        ]])
        mask = np.array([[1.0, 1.0, 0.0]])

        result = pooler.pool(embeddings, mask)

        expected = np.array([[3.0, 4.0]])
        np.testing.assert_array_almost_equal(result, expected)


class TestMaxPooler:
    """Test max pooling."""

    def test_max_pool(self):
        """Test max pooling."""
        config = PoolingConfig(strategy=PoolingStrategy.MAX)
        pooler = MaxPooler(config)

        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.array([[
            [1.0, 5.0],
            [3.0, 2.0],
            [2.0, 4.0],
        ]])

        result = pooler.pool(embeddings)

        expected = np.array([[3.0, 5.0]])
        np.testing.assert_array_almost_equal(result, expected)


class TestAttentionPooler:
    """Test attention-weighted pooling."""

    def test_attention_pool(self):
        """Test attention pooling."""
        config = PoolingConfig(strategy=PoolingStrategy.ATTENTION)
        pooler = AttentionPooler(config, hidden_dim=2)

        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.array([[
            [1.0, 2.0],
            [3.0, 4.0],
        ]])
        attention_mask = np.array([[1.0, 1.0]])

        result = pooler.pool(embeddings, attention_mask)

        # Should be weighted sum
        assert result is not None
        assert result.shape == (1, 2)


class TestWeightedMeanPooler:
    """Test weighted mean pooling."""

    def test_weighted_mean_pool(self):
        """Test weighted mean pooling."""
        config = PoolingConfig(strategy=PoolingStrategy.WEIGHTED_MEAN)
        pooler = WeightedMeanPooler(config)

        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.array([[
            [1.0, 2.0],
            [3.0, 4.0],
        ]])
        # attention_mask serves as weights
        attention_mask = np.array([[0.25, 0.75]])

        result = pooler.pool(embeddings, attention_mask)

        # Result should be weighted mean
        assert result is not None
        assert result.shape == (1, 2)


class TestMatryoshkaPooler:
    """Test Matryoshka dimensionality reduction."""

    def test_matryoshka_truncation(self):
        """Test Matryoshka embedding truncation."""
        config = PoolingConfig(strategy=PoolingStrategy.MEAN, truncate_dim=128)
        pooler = MatryoshkaPooler(config, supported_dims=[64, 128, 256, 512])

        # BasePooler.truncate works on embeddings
        embedding = np.random.randn(512)

        result = pooler.truncate(embedding, 128)

        assert len(result) == 128

    def test_matryoshka_with_normalize(self):
        """Test Matryoshka with normalization."""
        config = PoolingConfig(strategy=PoolingStrategy.MEAN, normalize=True, truncate_dim=2)
        pooler = MatryoshkaPooler(config)

        # 3D input for pool method: (batch, seq_len, hidden_dim)
        hidden_states = np.array([[[3.0, 4.0, 0.0, 0.0]]])

        result = pooler.pool_and_process(hidden_states)

        # Should be normalized and truncated to 2 dims
        assert result.shape[-1] == 2
        norm = np.linalg.norm(result[0])
        np.testing.assert_almost_equal(norm, 1.0)


class TestMultiVectorPooler:
    """Test ColBERT-style multi-vector pooling."""

    def test_multi_vector_pool(self):
        """Test multi-vector pooling."""
        config = PoolingConfig(strategy=PoolingStrategy.MEAN)
        pooler = MultiVectorPooler(config, compression_dim=64)

        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.random.randn(1, 10, 768)
        mask = np.ones((1, 10))

        result = pooler.pool(embeddings, mask)

        assert result.shape[1] == 10  # seq_len preserved
        assert result.shape[2] == 64  # compressed dim

    def test_multi_vector_maxsim_score(self):
        """Test MaxSim scoring."""
        config = PoolingConfig(strategy=PoolingStrategy.MEAN)
        pooler = MultiVectorPooler(config, compression_dim=64)

        query_vectors = np.random.randn(5, 64)
        doc_vectors = np.random.randn(10, 64)

        score = pooler.maxsim_score(query_vectors, doc_vectors)

        assert isinstance(score, float)


class TestStepPooler:
    """Test step-based pooling."""

    def test_step_pool(self):
        """Test step pooling."""
        config = PoolingConfig(strategy=PoolingStrategy.MEAN)
        step_token_ids = [2]  # Token ID 2 is a step marker
        pooler = StepPooler(config, step_token_ids=step_token_ids)

        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.array([[
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],  # step token position (token_id=2)
            [7.0, 8.0],
        ]])
        # Token IDs with step marker at position 2
        token_ids = np.array([[0, 1, 2, 3]])

        result = pooler.pool(embeddings, token_ids=token_ids)

        # Should pool at step token positions
        assert result.shape[0] == 1  # batch size


class TestPoolingEngine:
    """Test unified pooling engine."""

    def test_create_engine(self):
        """Test creating pooling engine."""
        engine = PoolingEngine(hidden_dim=768)
        assert engine is not None

    def test_engine_with_config(self):
        """Test engine with config."""
        config = PoolingConfig(
            task=PoolingTask.EMBED,
            strategy=PoolingStrategy.MEAN,
        )
        engine = PoolingEngine(config=config, hidden_dim=768)
        assert engine is not None

    def test_pool_embeddings(self):
        """Test pooling through engine."""
        engine = create_pooling_engine(
            strategy=PoolingStrategy.MEAN,
            hidden_dim=768,
        )

        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.random.randn(1, 10, 768)
        mask = np.ones((1, 10))

        result = engine.pool(embeddings, mask)

        assert result.embeddings is not None
        assert result.embeddings.shape[-1] == 768

    def test_pool_with_different_strategies(self):
        """Test pooling with different strategies."""
        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.random.randn(1, 10, 768)
        mask = np.ones((1, 10))

        for strategy in [PoolingStrategy.MEAN, PoolingStrategy.CLS, PoolingStrategy.LAST]:
            engine = create_pooling_engine(strategy=strategy, hidden_dim=768)
            result = engine.pool(embeddings, mask)
            assert result.embeddings is not None

    def test_classification_output(self):
        """Test classification pooling."""
        engine = create_pooling_engine(
            strategy=PoolingStrategy.CLS,
            hidden_dim=768,
            task=PoolingTask.CLASSIFY,
        )

        # 3D input: (batch, seq_len, hidden_dim)
        embeddings = np.random.randn(1, 10, 768)

        result = engine.pool(embeddings)
        assert result is not None
        assert result is not None


class TestFactoryFunction:
    """Test factory function."""

    def test_create_mean_engine(self):
        """Test creating mean pooling engine."""
        engine = create_pooling_engine(strategy=PoolingStrategy.MEAN)
        assert engine is not None

    def test_create_cls_engine(self):
        """Test creating CLS pooling engine."""
        engine = create_pooling_engine(strategy=PoolingStrategy.CLS)
        assert engine is not None

    def test_create_with_truncate_dim(self):
        """Test creating engine with Matryoshka dimension truncation."""
        engine = create_pooling_engine(
            strategy=PoolingStrategy.MEAN,
            truncate_dim=128,
        )
        assert engine is not None


# Run pytest if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
