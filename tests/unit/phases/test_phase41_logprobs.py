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
# Phase 41: Unit Tests for Logprobs Processing

"""
Tests for LogprobsProcessor module.
"""

import pytest
import numpy as np
import math
from unittest.mock import Mock, MagicMock

from src.infrastructure.engine.logprobs.logprobs_processor import (
    LogprobFormat,
    LogprobEntry,
    TopLogprob,
    PromptLogprobs,
    SampleLogprobs,
    FlatLogprobs,
    LogprobsResult,
    LogprobsProcessor,
    StreamingLogprobs,
    LogprobsAnalyzer,
    compute_perplexity,
    compute_entropy,
    normalize_logprobs,
)


class TestLogprobFormat:
    """Test LogprobFormat enum."""

    def test_format_values(self):
        """Test LogprobFormat enum values."""
        assert LogprobFormat.DICT is not None
        assert LogprobFormat.TUPLE is not None
        assert LogprobFormat.FLAT is not None
        assert LogprobFormat.STRUCTURED is not None


class TestTopLogprob:
    """Test TopLogprob dataclass."""

    def test_top_logprob_creation(self):
        """Test TopLogprob creation."""
        top = TopLogprob(
            token_id=100,
            token="hello",
            logprob=-0.5,
        )

        assert top.token_id == 100
        assert top.token == "hello"
        assert top.logprob == -0.5

    def test_top_logprob_probability(self):
        """Test probability property."""
        top = TopLogprob(token_id=100, token="test", logprob=-1.0)

        expected = math.exp(-1.0)
        assert top.probability == pytest.approx(expected)

    def test_top_logprob_comparison(self):
        """Test TopLogprob comparison."""
        top1 = TopLogprob(token_id=1, token="a", logprob=-0.5)
        top2 = TopLogprob(token_id=2, token="b", logprob=-1.0)

        assert top2 < top1  # top2 has lower logprob


class TestLogprobEntry:
    """Test LogprobEntry dataclass."""

    def test_logprob_entry_creation(self):
        """Test LogprobEntry creation."""
        entry = LogprobEntry(
            token_id=100,
            token="hello",
            logprob=-0.5,
            position=0,
        )

        assert entry.token_id == 100
        assert entry.token == "hello"
        assert entry.logprob == -0.5
        assert entry.position == 0

    def test_logprob_entry_probability(self):
        """Test probability property."""
        entry = LogprobEntry(token_id=100, token="test", logprob=-1.0)

        expected = math.exp(-1.0)
        assert entry.probability == pytest.approx(expected)

    def test_logprob_entry_entropy(self):
        """Test entropy calculation."""
        top_logprobs = (
            TopLogprob(token_id=1, token="a", logprob=-0.5),
            TopLogprob(token_id=2, token="b", logprob=-1.0),
            TopLogprob(token_id=3, token="c", logprob=-2.0),
        )

        entry = LogprobEntry(
            token_id=1,
            token="a",
            logprob=-0.5,
            top_logprobs=top_logprobs,
        )

        assert entry.entropy > 0

    def test_logprob_entry_entropy_empty(self):
        """Test entropy with no top logprobs."""
        entry = LogprobEntry(token_id=1, token="a", logprob=-0.5)

        assert entry.entropy == 0.0


class TestPromptLogprobs:
    """Test PromptLogprobs dataclass."""

    def test_prompt_logprobs_creation(self):
        """Test PromptLogprobs creation."""
        prompt_lp = PromptLogprobs(
            token_ids=[1, 2, 3],
            tokens=["a", "b", "c"],
            logprobs=[-0.5, -1.0, -0.8],
        )

        assert len(prompt_lp) == 3
        assert prompt_lp[0] == (1, "a", -0.5)

    def test_prompt_logprobs_mean(self):
        """Test mean logprob calculation."""
        prompt_lp = PromptLogprobs(
            token_ids=[1, 2, 3],
            tokens=["a", "b", "c"],
            logprobs=[-0.5, -1.0, -0.5],
        )

        assert prompt_lp.mean_logprob == pytest.approx(-0.667, rel=0.01)

    def test_prompt_logprobs_perplexity(self):
        """Test perplexity calculation."""
        prompt_lp = PromptLogprobs(
            token_ids=[1, 2],
            tokens=["a", "b"],
            logprobs=[-1.0, -1.0],
        )

        # PPL = exp(-mean_logprob) = exp(1.0) ≈ 2.718
        assert prompt_lp.perplexity == pytest.approx(math.e, rel=0.01)


class TestSampleLogprobs:
    """Test SampleLogprobs dataclass."""

    def test_sample_logprobs_creation(self):
        """Test SampleLogprobs creation."""
        sample_lp = SampleLogprobs()

        assert len(sample_lp) == 0

    def test_sample_logprobs_append(self):
        """Test appending entries."""
        sample_lp = SampleLogprobs()

        entry = LogprobEntry(token_id=1, token="a", logprob=-0.5)
        sample_lp.append(entry)

        assert len(sample_lp) == 1
        assert sample_lp[0] == entry

    def test_sample_logprobs_properties(self):
        """Test token_ids, tokens, logprobs properties."""
        entries = [
            LogprobEntry(token_id=1, token="a", logprob=-0.5),
            LogprobEntry(token_id=2, token="b", logprob=-1.0),
        ]
        sample_lp = SampleLogprobs(entries=entries)

        assert sample_lp.token_ids == [1, 2]
        assert sample_lp.tokens == ["a", "b"]
        assert sample_lp.logprobs == [-0.5, -1.0]


class TestFlatLogprobs:
    """Test FlatLogprobs dataclass."""

    def test_flat_logprobs_empty(self):
        """Test empty FlatLogprobs."""
        flat = FlatLogprobs.empty(top_k=5)

        assert flat.num_tokens == 0
        assert flat.top_k == 5

    def test_flat_logprobs_creation(self):
        """Test FlatLogprobs creation."""
        flat = FlatLogprobs(
            token_ids=np.array([1, 2, 3], dtype=np.int32),
            logprobs=np.array([-0.5, -1.0, -0.8], dtype=np.float32),
            top_k_token_ids=np.zeros((3, 5), dtype=np.int32),
            top_k_logprobs=np.full((3, 5), -float('inf'), dtype=np.float32),
        )

        assert flat.num_tokens == 3
        assert flat.top_k == 5

    def test_flat_logprobs_memory_bytes(self):
        """Test memory_bytes property."""
        flat = FlatLogprobs(
            token_ids=np.array([1, 2, 3], dtype=np.int32),
            logprobs=np.array([-0.5, -1.0, -0.8], dtype=np.float32),
            top_k_token_ids=np.zeros((3, 5), dtype=np.int32),
            top_k_logprobs=np.zeros((3, 5), dtype=np.float32),
        )

        assert flat.memory_bytes > 0

    def test_flat_logprobs_from_entries(self):
        """Test creating from LogprobEntry list."""
        entries = [
            LogprobEntry(
                token_id=1,
                token="a",
                logprob=-0.5,
                top_logprobs=(
                    TopLogprob(token_id=1, token="a", logprob=-0.5),
                    TopLogprob(token_id=2, token="b", logprob=-1.0),
                ),
            ),
        ]

        flat = FlatLogprobs.from_entries(entries, top_k=5)

        assert flat.num_tokens == 1
        assert flat.token_ids[0] == 1
        assert flat.logprobs[0] == pytest.approx(-0.5)

    def test_flat_logprobs_slice(self):
        """Test slicing FlatLogprobs."""
        flat = FlatLogprobs(
            token_ids=np.array([1, 2, 3, 4, 5], dtype=np.int32),
            logprobs=np.array([-0.5, -1.0, -0.8, -0.9, -0.7], dtype=np.float32),
            top_k_token_ids=np.zeros((5, 5), dtype=np.int32),
            top_k_logprobs=np.zeros((5, 5), dtype=np.float32),
        )

        sliced = flat.slice(1, 4)

        assert sliced.num_tokens == 3
        assert list(sliced.token_ids) == [2, 3, 4]

    def test_flat_logprobs_append(self):
        """Test appending FlatLogprobs."""
        flat1 = FlatLogprobs(
            token_ids=np.array([1, 2], dtype=np.int32),
            logprobs=np.array([-0.5, -1.0], dtype=np.float32),
            top_k_token_ids=np.zeros((2, 5), dtype=np.int32),
            top_k_logprobs=np.zeros((2, 5), dtype=np.float32),
        )

        flat2 = FlatLogprobs(
            token_ids=np.array([3, 4], dtype=np.int32),
            logprobs=np.array([-0.8, -0.9], dtype=np.float32),
            top_k_token_ids=np.zeros((2, 5), dtype=np.int32),
            top_k_logprobs=np.zeros((2, 5), dtype=np.float32),
        )

        combined = flat1.append(flat2)

        assert combined.num_tokens == 4
        assert list(combined.token_ids) == [1, 2, 3, 4]

    def test_flat_logprobs_mean_logprob(self):
        """Test mean logprob calculation."""
        flat = FlatLogprobs(
            token_ids=np.array([1, 2], dtype=np.int32),
            logprobs=np.array([-1.0, -2.0], dtype=np.float32),
            top_k_token_ids=np.zeros((2, 5), dtype=np.int32),
            top_k_logprobs=np.zeros((2, 5), dtype=np.float32),
        )

        assert flat.mean_logprob() == pytest.approx(-1.5)

    def test_flat_logprobs_perplexity(self):
        """Test perplexity calculation."""
        flat = FlatLogprobs(
            token_ids=np.array([1, 2], dtype=np.int32),
            logprobs=np.array([-1.0, -1.0], dtype=np.float32),
            top_k_token_ids=np.zeros((2, 5), dtype=np.int32),
            top_k_logprobs=np.zeros((2, 5), dtype=np.float32),
        )

        assert flat.perplexity() == pytest.approx(math.e, rel=0.01)


class TestLogprobsProcessor:
    """Test LogprobsProcessor class."""

    def test_processor_creation(self):
        """Test LogprobsProcessor creation."""
        processor = LogprobsProcessor(top_k=5)

        assert processor.top_k == 5
        assert processor.output_format == LogprobFormat.FLAT

    def test_process_logits_flat(self):
        """Test processing logits to flat format."""
        processor = LogprobsProcessor(
            top_k=3,
            output_format=LogprobFormat.FLAT,
        )

        # Create mock logits [2 tokens, vocab_size=10]
        logits = np.array([
            [1.0, 2.0, 3.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 2.0, 3.0, 0.5, 0.5],
        ])
        token_ids = np.array([2, 7])  # Selected tokens

        result = processor.process_logits(logits, token_ids)

        assert isinstance(result, FlatLogprobs)
        assert result.num_tokens == 2

    def test_process_logits_structured(self):
        """Test processing logits to structured format."""
        processor = LogprobsProcessor(
            top_k=3,
            output_format=LogprobFormat.STRUCTURED,
        )

        logits = np.array([
            [1.0, 2.0, 3.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        ])
        token_ids = np.array([2])

        result = processor.process_logits(logits, token_ids)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], LogprobEntry)

    def test_process_batch(self):
        """Test batch processing."""
        processor = LogprobsProcessor(top_k=3)

        batch_logits = [
            np.array([[1.0, 2.0, 3.0, 0.5, 0.5]]),
            np.array([[0.5, 0.5, 1.0, 2.0, 3.0]]),
        ]
        batch_token_ids = [np.array([2]), np.array([4])]

        results = processor.process_batch(batch_logits, batch_token_ids)

        assert len(results) == 2


class TestStreamingLogprobs:
    """Test StreamingLogprobs class."""

    def test_streaming_creation(self):
        """Test StreamingLogprobs creation."""
        streaming = StreamingLogprobs(top_k=5, max_tokens=1024)

        assert streaming.top_k == 5
        assert streaming.max_tokens == 1024
        assert streaming.num_tokens == 0

    def test_add_token(self):
        """Test adding a single token."""
        streaming = StreamingLogprobs()

        streaming.add_token(
            token_id=100,
            logprob=-0.5,
        )

        assert streaming.num_tokens == 1

    def test_add_from_logits(self):
        """Test adding from raw logits."""
        streaming = StreamingLogprobs(top_k=3)

        logits = np.array([1.0, 2.0, 3.0, 0.5, 0.5])
        streaming.add_from_logits(logits, token_id=2)

        assert streaming.num_tokens == 1

    def test_mean_logprob(self):
        """Test mean logprob property."""
        streaming = StreamingLogprobs()

        streaming.add_token(token_id=1, logprob=-1.0)
        streaming.add_token(token_id=2, logprob=-2.0)

        assert streaming.mean_logprob == pytest.approx(-1.5)

    def test_perplexity(self):
        """Test perplexity property."""
        streaming = StreamingLogprobs()

        streaming.add_token(token_id=1, logprob=-1.0)
        streaming.add_token(token_id=2, logprob=-1.0)

        assert streaming.perplexity == pytest.approx(math.e, rel=0.01)

    def test_finalize(self):
        """Test finalize to FlatLogprobs."""
        streaming = StreamingLogprobs()

        streaming.add_token(token_id=1, logprob=-0.5)
        streaming.add_token(token_id=2, logprob=-1.0)

        flat = streaming.finalize()

        assert isinstance(flat, FlatLogprobs)
        assert flat.num_tokens == 2

    def test_reset(self):
        """Test reset for reuse."""
        streaming = StreamingLogprobs()

        streaming.add_token(token_id=1, logprob=-0.5)
        streaming.reset()

        assert streaming.num_tokens == 0


class TestLogprobsAnalyzer:
    """Test LogprobsAnalyzer class."""

    def test_rank_token_importance(self):
        """Test ranking token importance."""
        flat = FlatLogprobs(
            token_ids=np.array([1, 2, 3, 4, 5], dtype=np.int32),
            logprobs=np.array([-1.0, -10.0, -0.5, -8.0, -2.0], dtype=np.float32),
            top_k_token_ids=np.zeros((5, 5), dtype=np.int32),
            top_k_logprobs=np.zeros((5, 5), dtype=np.float32),
        )

        important = LogprobsAnalyzer.rank_token_importance(flat, threshold=-5.0)

        # Should find tokens with logprob < -5.0 (positions 1 and 3)
        assert len(important) >= 2

    def test_compute_confidence_mean(self):
        """Test confidence computation with mean method."""
        flat = FlatLogprobs(
            token_ids=np.array([1, 2], dtype=np.int32),
            logprobs=np.array([-0.5, -0.5], dtype=np.float32),
            top_k_token_ids=np.zeros((2, 5), dtype=np.int32),
            top_k_logprobs=np.zeros((2, 5), dtype=np.float32),
        )

        confidence = LogprobsAnalyzer.compute_confidence(flat, method="mean")

        assert 0 < confidence < 1

    def test_compute_confidence_geometric(self):
        """Test confidence computation with geometric method."""
        flat = FlatLogprobs(
            token_ids=np.array([1, 2], dtype=np.int32),
            logprobs=np.array([-1.0, -1.0], dtype=np.float32),
            top_k_token_ids=np.zeros((2, 5), dtype=np.int32),
            top_k_logprobs=np.zeros((2, 5), dtype=np.float32),
        )

        confidence = LogprobsAnalyzer.compute_confidence(flat, method="geometric")

        # geometric = exp(mean(logprobs)) = exp(-1.0) ≈ 0.368
        assert confidence == pytest.approx(math.exp(-1.0), rel=0.01)

    def test_detect_anomalies(self):
        """Test anomaly detection."""
        # Use many normal values so the outlier doesn't skew mean too much
        normal_vals = [-1.0, -1.2, -0.8, -1.1, -0.9, -1.3, -1.0, -1.2]
        anomaly_val = [-50.0]
        all_vals = normal_vals + anomaly_val

        flat = FlatLogprobs(
            token_ids=np.array(list(range(len(all_vals))), dtype=np.int32),
            logprobs=np.array(all_vals, dtype=np.float32),
            top_k_token_ids=np.zeros((len(all_vals), 5), dtype=np.int32),
            top_k_logprobs=np.zeros((len(all_vals), 5), dtype=np.float32),
        )

        anomalies = LogprobsAnalyzer.detect_anomalies(flat, z_threshold=2.0)

        # Position 8 (last) has anomalously low logprob (-50.0 vs ~-1.0)
        assert 8 in anomalies

    def test_compute_calibration(self):
        """Test calibration computation."""
        flat = FlatLogprobs(
            token_ids=np.array([1, 2, 3, 4, 5], dtype=np.int32),
            logprobs=np.array([-0.1, -0.5, -1.0, -2.0, -3.0], dtype=np.float32),
            top_k_token_ids=np.zeros((5, 5), dtype=np.int32),
            top_k_logprobs=np.zeros((5, 5), dtype=np.float32),
        )

        cal = LogprobsAnalyzer.compute_calibration(flat, num_bins=5)

        assert "bin_counts" in cal
        assert "bin_means" in cal
        assert "mean_confidence" in cal


class TestUtilityFunctions:
    """Test utility functions."""

    def test_compute_perplexity(self):
        """Test compute_perplexity function."""
        logprobs = [-1.0, -1.0]
        ppl = compute_perplexity(logprobs)

        assert ppl == pytest.approx(math.e, rel=0.01)

    def test_compute_perplexity_empty(self):
        """Test compute_perplexity with empty list."""
        ppl = compute_perplexity([])
        assert ppl == 0.0

    def test_compute_entropy(self):
        """Test compute_entropy function."""
        logprobs = [-0.5, -1.0, -2.0]
        entropy = compute_entropy(logprobs)

        assert entropy > 0

    def test_normalize_logprobs(self):
        """Test normalize_logprobs function."""
        logprobs = np.array([[-1.0, -2.0, -3.0]])
        normalized = normalize_logprobs(logprobs)

        # Should sum to 0 in log space (probabilities sum to 1)
        from scipy.special import logsumexp
        log_sum = np.log(np.sum(np.exp(normalized), axis=-1))
        assert np.allclose(log_sum, 0.0, atol=1e-5)
