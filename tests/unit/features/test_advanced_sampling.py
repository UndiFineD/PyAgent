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
# Phase 40: Advanced Sampling Parameters Tests

"""
Tests for AdvancedSamplingParams - extended sampling strategies.
"""

import pytest
import numpy as np
from typing import List

from src.infrastructure.sampling import (
    OutputKind,
    StopCondition,
    TemperatureSchedule,
    SamplingParams,
    AdvancedSamplingParams,
    LogitBiasBuilder,
    BadWordsProcessor,
    TokenWhitelistProcessor,
    MirostatSampler,
    SamplingEngine,
    create_sampling_params,
    create_advanced_sampling_params,
)


class TestEnums:
    """Test enum values."""

    def test_output_kind_values(self):
        """Test OutputKind enum."""
        assert OutputKind.CUMULATIVE is not None
        assert OutputKind.DELTA is not None
        assert OutputKind.FINAL_ONLY is not None

    def test_stop_condition_values(self):
        """Test StopCondition enum."""
        assert StopCondition.EOS is not None
        assert StopCondition.MAX_TOKENS is not None
        assert StopCondition.STOP_STRING is not None

    def test_temperature_schedule_values(self):
        """Test TemperatureSchedule enum."""
        assert TemperatureSchedule.CONSTANT is not None
        assert TemperatureSchedule.LINEAR_DECAY is not None
        assert TemperatureSchedule.COSINE_DECAY is not None
        assert TemperatureSchedule.ADAPTIVE is not None


class TestSamplingParams:
    """Test basic SamplingParams."""

    def test_create_default_params(self):
        """Test creating default params."""
        params = SamplingParams()

        assert params.temperature == 1.0
        assert params.top_p == 1.0
        assert params.top_k == -1

    def test_create_custom_params(self):
        """Test creating custom params."""
        params = SamplingParams(
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            max_tokens=100,
        )

        assert params.temperature == 0.7
        assert params.top_p == 0.9
        assert params.top_k == 50
        assert params.max_tokens == 100

    def test_params_with_repetition_penalty(self):
        """Test params with repetition penalty."""
        params = SamplingParams(
            repetition_penalty=1.1,
            frequency_penalty=0.5,
            presence_penalty=0.3,
        )

        assert params.repetition_penalty == 1.1
        assert params.frequency_penalty == 0.5

    def test_params_validation(self):
        """Test parameter validation."""
        with pytest.raises(ValueError):
            SamplingParams(temperature=-1.0)

        with pytest.raises(ValueError):
            SamplingParams(top_p=1.5)

    def test_params_with_stop_strings(self):
        """Test params with stop token IDs."""
        params = SamplingParams(
            stop_token_ids=[50256, 50257],
        )

        assert len(params.stop_token_ids) == 2


class TestAdvancedSamplingParams:
    """Test AdvancedSamplingParams."""

    def test_create_advanced_params(self):
        """Test creating advanced params."""
        params = AdvancedSamplingParams(
            temperature=0.8,
            bad_words_ids=[[1, 2, 3]],
            flat_logprobs=True,
        )

        assert params.temperature == 0.8
        assert params.flat_logprobs is True

    def test_temperature_scheduling(self):
        """Test temperature scheduling."""
        params = AdvancedSamplingParams(
            temperature=1.0,
            temperature_schedule=TemperatureSchedule.LINEAR_DECAY,
            temperature_decay_target=0.1,
            temperature_decay_steps=100,
        )

        # At step 0
        temp0 = params.get_temperature(0)
        assert temp0 == 1.0

        # At step 50 (midpoint)
        temp50 = params.get_temperature(50)
        assert 0.5 <= temp50 <= 0.6

        # At step 100 (end)
        temp100 = params.get_temperature(100)
        assert temp100 == pytest.approx(0.1, abs=0.01)

    def test_cosine_temperature_schedule(self):
        """Test cosine temperature scheduling."""
        params = AdvancedSamplingParams(
            temperature=1.0,
            temperature_schedule=TemperatureSchedule.COSINE_DECAY,
            temperature_decay_target=0.0,
            temperature_decay_steps=100,
        )

        # Cosine should decay smoothly
        temp50 = params.get_temperature(50)
        assert 0.4 <= temp50 <= 0.6

    def test_adaptive_top_k(self):
        """Test adaptive top_k based on entropy."""
        params = AdvancedSamplingParams(
            adaptive_top_k=True,
            entropy_threshold=2.0,
            min_adaptive_k=5,
            max_adaptive_k=100,
        )

        # Low entropy -> small k
        k_low = params.get_adaptive_top_k(0.5)
        assert k_low < 50

        # High entropy -> large k
        k_high = params.get_adaptive_top_k(4.0)
        assert k_high > 50

    def test_contextual_penalty(self):
        """Test contextual repetition penalty."""
        params = AdvancedSamplingParams(
            repetition_penalty=1.2,
            repetition_penalty_range=100,
            repetition_penalty_decay=0.99,
        )

        # Near token (distance 1)
        penalty_near = params.get_contextual_penalty(1)
        assert penalty_near > 1.1

        # Far token (distance 50)
        penalty_far = params.get_contextual_penalty(50)
        assert penalty_far < penalty_near

        # Beyond range
        penalty_beyond = params.get_contextual_penalty(200)
        assert penalty_beyond == 1.0

    def test_mirostat_params(self):
        """Test mirostat parameters."""
        params = AdvancedSamplingParams(
            mirostat_mode=2,
            mirostat_tau=5.0,
            mirostat_eta=0.1,
        )

        assert params.mirostat_mode == 2
        assert params.mirostat_tau == 5.0


class TestLogitBiasBuilder:
    """Test LogitBiasBuilder."""

    def test_add_bias(self):
        """Test adding bias."""
        builder = LogitBiasBuilder()
        builder.add_bias(100, 2.0)
        builder.add_bias(200, -1.0)

        biases = builder.build()

        assert biases[100] == 2.0
        assert biases[200] == -1.0

    def test_ban_token(self):
        """Test banning token."""
        builder = LogitBiasBuilder()
        builder.ban_token(500)

        biases = builder.build()

        assert biases[500] == -100.0

    def test_prefer_token(self):
        """Test preferring token."""
        builder = LogitBiasBuilder()
        builder.prefer_token(300, strength=10.0)

        biases = builder.build()

        assert biases[300] == 10.0

    def test_chain_operations(self):
        """Test chaining operations."""
        biases = (
            LogitBiasBuilder()
            .add_bias(1, 1.0)
            .ban_token(2)
            .prefer_token(3)
            .build()
        )

        assert 1 in biases
        assert 2 in biases
        assert 3 in biases


class TestBadWordsProcessor:
    """Test BadWordsProcessor."""

    def test_single_token_ban(self):
        """Test banning single tokens."""
        processor = BadWordsProcessor(bad_words_ids=[[5], [10], [15]])

        banned = processor.get_banned_tokens([1, 2, 3])

        assert 5 in banned
        assert 10 in banned
        assert 15 in banned

    def test_multi_token_sequence(self):
        """Test banning multi-token sequences."""
        processor = BadWordsProcessor(bad_words_ids=[[1, 2, 3]])

        # Context ends with [1, 2] -> should ban 3
        banned = processor.get_banned_tokens([0, 1, 2])
        assert 3 in banned

        # Context doesn't match -> shouldn't ban
        banned2 = processor.get_banned_tokens([0, 0, 0])
        assert 3 not in banned2

    def test_apply_to_logits(self):
        """Test applying bad words to logits."""
        processor = BadWordsProcessor(bad_words_ids=[[5]])

        logits = np.zeros(10)
        logits = processor.apply_to_logits(logits, [1, 2, 3])

        assert logits[5] == -float('inf')


class TestTokenWhitelistProcessor:
    """Test TokenWhitelistProcessor."""

    def test_whitelist_tokens(self):
        """Test whitelisting tokens."""
        processor = TokenWhitelistProcessor(allowed_token_ids=[0, 1, 2])

        logits = np.zeros(10)
        logits = processor.apply_to_logits(logits, vocab_size=10)

        # Allowed tokens should keep 0
        assert logits[0] == 0
        assert logits[1] == 0
        assert logits[2] == 0

        # Non-allowed should be -inf
        assert logits[5] == -float('inf')

    def test_build_mask(self):
        """Test building mask."""
        processor = TokenWhitelistProcessor(allowed_token_ids=[1, 3, 5])

        mask = processor.build_mask(vocab_size=10)

        assert mask[1] == True
        assert mask[3] == True
        assert mask[5] == True
        assert mask[0] == False
        assert mask[2] == False


class TestMirostatSampler:
    """Test MirostatSampler."""

    def test_create_sampler(self):
        """Test creating sampler."""
        sampler = MirostatSampler(tau=5.0, eta=0.1, mode=2)

        assert sampler.tau == 5.0
        assert sampler.eta == 0.1

    def test_sample(self):
        """Test sampling."""
        sampler = MirostatSampler(tau=5.0, eta=0.1, mode=2)

        # Create logits with one dominant token
        logits = np.array([-10.0, -10.0, 5.0, -10.0, -10.0])

        token_id, prob = sampler.sample(logits)

        # Should likely select token 2
        assert token_id == 2
        assert prob > 0.5

    def test_mu_update(self):
        """Test mu is updated after sampling."""
        sampler = MirostatSampler(tau=5.0, eta=0.1)
        initial_mu = sampler.mu

        logits = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        sampler.sample(logits)

        # mu should change
        assert sampler.mu != initial_mu


class TestSamplingEngine:
    """Test SamplingEngine."""

    def test_create_engine(self):
        """Test creating engine."""
        params = SamplingParams(temperature=0.7)
        engine = SamplingEngine(params)

        assert engine is not None

    def test_sample_with_temperature(self):
        """Test sampling with temperature."""
        params = SamplingParams(temperature=0.5)
        engine = SamplingEngine(params)

        logits = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        token_id, prob = engine.sample(logits)

        assert 0 <= token_id < 5
        assert 0 < prob <= 1

    def test_sample_greedy(self):
        """Test greedy sampling (temperature=0)."""
        params = SamplingParams(temperature=0.0)
        engine = SamplingEngine(params)

        logits = np.array([1.0, 2.0, 5.0, 3.0, 4.0])
        token_id, prob = engine.sample(logits)

        # Should always select argmax
        assert token_id == 2

    def test_sample_with_top_k(self):
        """Test sampling with top_k."""
        params = SamplingParams(temperature=1.0, top_k=2)
        engine = SamplingEngine(params)

        logits = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

        # Sample multiple times
        selections = set()
        for _ in range(100):
            token_id, _ = engine.sample(logits)
            selections.add(token_id)

        # Should only select from top 2 tokens
        assert all(s in [3, 4] for s in selections)

    def test_sample_with_top_p(self):
        """Test sampling with top_p."""
        params = SamplingParams(temperature=1.0, top_p=0.5)
        engine = SamplingEngine(params)

        logits = np.array([0.0, 0.0, 0.0, 0.0, 10.0])
        token_id, _ = engine.sample(logits)

        # Should likely select the dominant token
        assert token_id == 4

    def test_sample_with_bad_words(self):
        """Test sampling with bad words."""
        params = AdvancedSamplingParams(
            temperature=1.0,
            bad_words_ids=[[2]],
        )
        engine = SamplingEngine(params)

        logits = np.array([1.0, 1.0, 10.0, 1.0, 1.0])  # Token 2 is best

        # Sample multiple times
        for _ in range(10):
            token_id, _ = engine.sample(logits, context_ids=[0, 1])
            assert token_id != 2  # Token 2 should be banned

    def test_sample_with_whitelist(self):
        """Test sampling with token whitelist."""
        params = AdvancedSamplingParams(
            temperature=1.0,
            allowed_token_ids=[0, 1],
        )
        engine = SamplingEngine(params)

        logits = np.array([1.0, 2.0, 10.0, 5.0, 5.0])

        # Should only select from whitelist
        for _ in range(10):
            token_id, _ = engine.sample(logits)
            assert token_id in [0, 1]

    def test_reset(self):
        """Test resetting engine."""
        params = SamplingParams(temperature=0.7)
        engine = SamplingEngine(params)

        # Sample a few times
        for _ in range(5):
            engine.sample(np.array([1.0, 2.0, 3.0]))

        # Reset
        engine.reset()

        # Should not raise
        assert True


class TestFactoryFunctions:
    """Test factory functions."""

    def test_create_sampling_params(self):
        """Test create_sampling_params."""
        params = create_sampling_params(
            temperature=0.7,
            top_p=0.9,
            max_tokens=100,
        )

        assert params.temperature == 0.7
        assert params.top_p == 0.9

    def test_create_advanced_sampling_params(self):
        """Test create_advanced_sampling_params."""
        params = create_advanced_sampling_params(
            temperature=0.8,
            adaptive=True,
        )

        assert params.temperature == 0.8
        assert params.adaptive_top_k is True

    def test_create_params_with_defaults(self):
        """Test creating params with defaults."""
        params = create_sampling_params()

        assert params.temperature == 1.0
        assert params.top_p == 1.0


# Run pytest if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
