# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Phase 28: Request Lifecycle, Sampling & Detokenization Tests.

Tests for:
    - RequestLifecycle.py: Request state machine and queue management
    - EngineLifecycle.py: Engine state management
    - SamplingEngine.py: Unified sampling strategies
    - IncrementalDetokenizer.py: Streaming token-to-text
    - Rust accelerations for Phase 28
"""

import pytest
import time
import math
from typing import Dict, List, Set

# Import Phase 28 modules
from src.infrastructure.engine.request_lifecycle import (
    RequestStatus,
    FinishReason,
    Request,
    RequestQueue,
    RequestTracker,
)
from src.infrastructure.engine.engine_lifecycle import (
    EngineState,
    EngineConfig,
    EngineLifecycleManager,
)
from src.infrastructure.engine.sampling.sampling_engine import (
    SamplingParams,
    SamplingState,
    TopKSampler,
    TopPSampler,
    TopKTopPSampler,
    TemperatureSampler,
    GumbelSampler,
    RepetitionPenaltySampler,
    BeamSearchSampler,
    BeamHypothesis,
    SamplingPipeline,
    sample_logits,
)
from src.infrastructure.engine.tokenization.incremental_detokenizer import (
    DetokenizeResult,
    StopChecker,
    FastIncrementalDetokenizer,
    SlowIncrementalDetokenizer,
    create_detokenizer,
    detokenize_incrementally,
)

# Try to import Rust accelerations
try:
    from rust_core import (
        request_status_transition_rust,
        top_k_mask_rust,
        top_p_mask_rust,
        gumbel_sample_rust,
        beam_score_rust,
        check_stop_tokens_rust,
        update_prefix_offset_rust,
        compute_penalties_rust,
    )
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

# Try to import numpy
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


# ==============================================================================
# Mock Tokenizer for Testing
# ==============================================================================

class MockTokenizer:
    """Mock tokenizer for testing detokenization."""

    def __init__(self):
        self.vocab = {
            "Hello": 0,
            " world": 1,
            "!": 2,
            " How": 3,
            " are": 4,
            " you": 5,
            "?": 6,
            "<eos>": 7,
            "<pad>": 8,
        }
        self.id_to_token = {v: k for k, v in self.vocab.items()}
        self.eos_token_id = 7
        self.is_fast = True
        self.all_special_ids = [7, 8]

    def encode(self, text: str, **kwargs) -> List[int]:
        """Simple encoding."""
        tokens = []
        for token, id in self.vocab.items():
            if token in text:
                tokens.append(id)
        return tokens

    def decode(
        self,
        token_ids,
        skip_special_tokens: bool = True,
        **kwargs,
    ) -> str:
        """Simple decoding."""
        if isinstance(token_ids, int):
            token_ids = [token_ids]

        text = ""
        for tid in token_ids:
            if tid in self.id_to_token:
                token = self.id_to_token[tid]
                if skip_special_tokens and tid in self.all_special_ids:
                    continue
                text += token
        return text

    def convert_ids_to_tokens(self, ids):
        """Convert IDs to tokens."""
        if isinstance(ids, int):
            return self.id_to_token.get(ids, "<unk>")
        return [self.id_to_token.get(id, "<unk>") for id in ids]

    def convert_tokens_to_ids(self, tokens):
        """Convert tokens to IDs."""
        if isinstance(tokens, str):
            return self.vocab.get(tokens, -1)
        return [self.vocab.get(t, -1) for t in tokens]


# ==============================================================================
# Request Lifecycle Tests
# ==============================================================================

class TestRequestStatus:
    """Tests for RequestStatus enum."""

    def test_status_values(self):
        """Test that all expected status values exist."""
        # IntEnum starts at 1 with auto()
        assert RequestStatus.WAITING.value == 1
        assert RequestStatus.RUNNING.value == 4  # After WAITING, WAITING_FOR_FSM, WAITING_FOR_REMOTE_KVS
        assert RequestStatus.PREEMPTED.value == 5
        assert RequestStatus.FINISHED_STOPPED.value == 6

    def test_is_finished(self):
        """Test is_finished static method."""
        assert not RequestStatus.is_finished(RequestStatus.WAITING)
        assert not RequestStatus.is_finished(RequestStatus.RUNNING)
        assert RequestStatus.is_finished(RequestStatus.FINISHED_STOPPED)
        assert RequestStatus.is_finished(RequestStatus.FINISHED_LENGTH_CAPPED)


class TestFinishReason:
    """Tests for FinishReason enum."""

    def test_finish_reason_values(self):
        """Test finish reason values - IntEnum with 0-3."""
        assert FinishReason.STOP.value == 0
        assert FinishReason.LENGTH.value == 1
        assert FinishReason.ABORT.value == 2
        assert FinishReason.ERROR.value == 3
        # String representations via __str__
        assert str(FinishReason.STOP) == "stop"
        assert str(FinishReason.LENGTH) == "length"


class TestRequest:
    """Tests for Request dataclass."""

    def test_create_request(self):
        """Test request creation."""
        req = Request(
            request_id="test-001",
            prompt="Hello world",
            prompt_token_ids=[0, 1],
            max_tokens=100,
        )
        assert req.request_id == "test-001"
        assert req.status == RequestStatus.WAITING
        assert not req.is_finished()

    def test_start_running(self):
        """Test starting a request."""
        req = Request(
            request_id="test-002",
            prompt="Test",
            prompt_token_ids=[0],
            max_tokens=50,
        )
        req.start_running()
        assert req.status == RequestStatus.RUNNING
        assert req.first_scheduled_time is not None

    def test_add_output_token(self):
        """Test adding output tokens."""
        req = Request(
            request_id="test-003",
            prompt="Test",
            prompt_token_ids=[0],
            max_tokens=50,
        )
        req.start_running()
        req.add_output_token(1)
        req.add_output_token(2)
        assert req.output_token_ids == [1, 2]
        assert req.num_output_tokens == 2

    def test_finish_request(self):
        """Test finishing a request."""
        req = Request(
            request_id="test-004",
            prompt="Test",
            prompt_token_ids=[0],
            max_tokens=50,
        )
        req.start_running()
        req.finish(FinishReason.STOP)
        assert req.is_finished()
        assert req.finish_reason == FinishReason.STOP
        assert req.finished_time is not None


class TestRequestQueue:
    """Tests for RequestQueue."""

    def test_add_and_get_waiting(self):
        """Test adding requests to queue."""
        queue = RequestQueue()

        req1 = Request(
            request_id="q1",
            prompt="Test 1",
            prompt_token_ids=[0],
            max_tokens=50,
        )
        req2 = Request(
            request_id="q2",
            prompt="Test 2",
            prompt_token_ids=[1],
            max_tokens=50,
        )

        queue.add_request(req1)
        queue.add_request(req2)

        waiting = queue.get_waiting_requests()
        assert len(waiting) == 2

    def test_schedule_next(self):
        """Test scheduling request to running state."""
        queue = RequestQueue()

        req = Request(
            request_id="run1",
            prompt="Test",
            prompt_token_ids=[0],
            max_tokens=50,
        )
        queue.add_request(req)
        scheduled = queue.schedule_next()

        assert len(queue.get_waiting_requests()) == 0
        assert len(queue.get_running_requests()) == 1
        assert len(scheduled) == 1

    def test_finish_request(self):
        """Test finishing a request in queue."""
        queue = RequestQueue()

        req = Request(
            request_id="fin1",
            prompt="Test",
            prompt_token_ids=[0],
            max_tokens=50,
        )
        queue.add_request(req)
        queue.schedule_next()
        queue.finish_request("fin1", FinishReason.STOP)

        assert len(queue.get_running_requests()) == 0
        finished = queue.get_request("fin1")
        assert finished.is_finished()


class TestRequestTracker:
    """Tests for RequestTracker."""

    def test_track_request(self):
        """Test tracking request metrics."""
        tracker = RequestTracker()

        req = Request(
            request_id="track1",
            prompt="Test",
            prompt_token_ids=[0, 1, 2],
            max_tokens=50,
        )
        # Must finish request before tracking
        req.start_running()
        req.add_output_token(10)
        req.finish(FinishReason.STOP)
        tracker.record_request(req)

        assert tracker.total_requests == 1
        assert tracker.total_prompt_tokens == 3


# ==============================================================================
# Engine Lifecycle Tests
# ==============================================================================

class TestEngineState:
    """Tests for EngineState enum."""

    def test_state_values(self):
        """Test engine state values."""
        # String enum values
        assert EngineState.INITIALIZING.value == "initializing"
        assert EngineState.READY.value == "ready"
        assert EngineState.RUNNING.value == "running"
        assert EngineState.SLEEPING.value == "sleeping"
        assert EngineState.SHUTTING_DOWN.value == "shutting_down"
        assert EngineState.DEAD.value == "dead"


class TestEngineConfig:
    """Tests for EngineConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = EngineConfig()
        assert config.max_requests == 256
        assert config.max_tokens_per_step == 8192

    def test_custom_config(self):
        """Test custom configuration."""
        config = EngineConfig(
            max_requests=128,
            step_timeout=60.0,
        )
        assert config.max_requests == 128
        assert config.step_timeout == 60.0


class TestEngineLifecycleManager:
    """Tests for EngineLifecycleManager."""

    def test_initialization(self):
        """Test engine initialization."""
        config = EngineConfig()
        manager = EngineLifecycleManager(config)

        assert manager.state == EngineState.INITIALIZING
        assert manager.config == config

    def test_start_engine(self):
        """Test starting the engine."""
        manager = EngineLifecycleManager(EngineConfig())
        manager.start()

        assert manager.state == EngineState.READY

    def test_run_and_step(self):
        """Test running engine step."""
        manager = EngineLifecycleManager(EngineConfig())
        manager.start()

        # Add a request to process
        req = Request(
            request_id="step-001",
            prompt="Test",
            max_tokens=50,
        )
        manager.add_request(req)

        # Step should transition to RUNNING
        manager.step()
        assert manager._step_count > 0

    def test_sleep_and_wake(self):
        """Test sleep and wake functionality."""
        manager = EngineLifecycleManager(EngineConfig(enable_sleep_mode=True))
        manager.start()

        manager.sleep(level=1)
        assert manager.state == EngineState.SLEEPING

        manager.wake_up()
        assert manager.state == EngineState.READY

    def test_shutdown(self):
        """Test engine shutdown."""
        manager = EngineLifecycleManager(EngineConfig())
        manager.start()
        manager.shutdown(timeout=1.0)

        assert manager.state == EngineState.DEAD


# ==============================================================================
# Sampling Engine Tests
# ==============================================================================

class TestSamplingParams:
    """Tests for SamplingParams."""

    def test_default_params(self):
        """Test default sampling parameters."""
        params = SamplingParams()
        assert params.temperature == 1.0
        assert params.top_k == -1
        assert params.top_p == 1.0

    def test_greedy_sampling(self):
        """Test greedy sampling config."""
        params = SamplingParams(temperature=0.0)
        assert params.temperature == 0.0


@pytest.mark.skipif(not HAS_NUMPY, reason="NumPy required")
class TestSamplers:
    """Tests for individual samplers."""

    def test_temperature_sampler(self):
        """Test temperature scaling."""
        sampler = TemperatureSampler()
        logits = np.array([[1.0, 2.0, 3.0]])  # [batch_size, vocab_size]
        params = SamplingParams(temperature=2.0)

        result = sampler.forward(logits, params)
        expected = logits / 2.0
        np.testing.assert_array_almost_equal(result, expected)

    def test_top_k_sampler(self):
        """Test top-k filtering."""
        sampler = TopKSampler()
        logits = np.array([[1.0, 3.0, 2.0, 0.5]])  # [1, 4]
        params = SamplingParams(top_k=2)

        result = sampler.forward(logits, params)
        # Should keep top-2: indices 1 (3.0) and 2 (2.0)
        assert np.isfinite(result[0, 1])
        assert np.isfinite(result[0, 2])
        assert result[0, 0] == float('-inf')
        assert result[0, 3] == float('-inf')

    def test_top_p_sampler(self):
        """Test top-p (nucleus) filtering."""
        sampler = TopPSampler()
        # Create logits where softmax gives clear probability distribution
        logits = np.array([[10.0, 0.0, 0.0, 0.0]])
        params = SamplingParams(top_p=0.5)

        result = sampler.forward(logits, params)
        # Token 0 should have most probability and be kept
        assert np.isfinite(result[0, 0])

    def test_beam_search_sampler(self):
        """Test beam search initialization."""
        from src.infrastructure.engine.sampling.sampling_engine import BeamSearchConfig

        config = BeamSearchConfig(
            beam_width=4,
            length_penalty=0.6,
        )
        sampler = BeamSearchSampler(config)
        assert sampler.config.beam_width == 4
        assert sampler.config.length_penalty == 0.6


@pytest.mark.skipif(not HAS_NUMPY, reason="NumPy required")
class TestSamplingPipeline:
    """Tests for sampling pipeline."""

    def test_basic_pipeline(self):
        """Test basic sampling pipeline."""
        params = SamplingParams(temperature=0.5, top_k=5)

        # Build pipeline with samplers
        pipeline = SamplingPipeline([
            TemperatureSampler(),
            TopKSampler(),
            GumbelSampler(),
        ])

        logits = np.random.randn(1, 100)  # [batch_size, vocab_size]
        state = SamplingState(request_id="test-001")

        token_ids = pipeline.sample(logits, params, state)
        assert token_ids.shape[0] == 1
        assert 0 <= token_ids[0] < 100

    def test_greedy_sampling(self):
        """Test greedy (argmax) sampling."""
        params = SamplingParams(temperature=0.0)

        pipeline = SamplingPipeline([
            TemperatureSampler(),
        ])

        logits = np.array([[0.1, 0.5, 0.9, 0.2]])  # [1, 4]

        token_ids = pipeline.sample(logits, params)
        assert token_ids[0] == 2  # Index of max value


@pytest.mark.skipif(not HAS_NUMPY, reason="NumPy required")
class TestSampleLogits:
    """Tests for the sample_logits convenience function."""

    def test_sample_logits(self):
        """Test the high-level sample_logits function."""
        logits = np.random.randn(1, 50)  # [batch_size, vocab_size]
        params = SamplingParams(temperature=0.7, top_k=10)

        token_ids = sample_logits(logits, params)
        assert token_ids.shape[0] == 1
        assert 0 <= token_ids[0] < 50


# ==============================================================================
# Incremental Detokenizer Tests
# ==============================================================================

class TestDetokenizeResult:
    """Tests for DetokenizeResult."""

    def test_result_creation(self):
        """Test creating a result."""
        result = DetokenizeResult(
            new_text="Hello",
            full_text="Hello",
            finished=False,
        )
        assert result.new_text == "Hello"
        assert result.has_new_text

    def test_empty_result(self):
        """Test empty result."""
        result = DetokenizeResult(
            new_text="",
            full_text="Previous text",
            finished=True,
        )
        assert not result.has_new_text
        assert result.finished


class TestStopChecker:
    """Tests for StopChecker."""

    def test_check_stop_token(self):
        """Test stop token checking."""
        checker = StopChecker(stop_token_ids={7, 8})

        assert checker.check_token(7) == 7
        assert checker.check_token(8) == 8
        assert checker.check_token(5) is None

    def test_check_stop_string(self):
        """Test stop string checking."""
        checker = StopChecker(stop_strings=["<|stop|>", "END"])

        stop, text = checker.check_text("Hello world<|stop|>more text")
        assert stop == "<|stop|>"
        assert text == "Hello world"

    def test_no_stop_string(self):
        """Test when no stop string found."""
        checker = StopChecker(stop_strings=["STOP"])

        stop, text = checker.check_text("Hello world")
        assert stop is None
        assert text == "Hello world"

    def test_partial_match(self):
        """Test partial stop string detection."""
        checker = StopChecker(stop_strings=["STOP"])

        # "STO" is a partial match of "STOP"
        buffered = checker.check_partial("Hello STO")
        assert buffered == 3


class TestFastIncrementalDetokenizer:
    """Tests for FastIncrementalDetokenizer."""

    def test_basic_detokenization(self):
        """Test basic token-to-text conversion."""
        tokenizer = MockTokenizer()
        detokenizer = FastIncrementalDetokenizer(tokenizer)

        # Add first token
        result = detokenizer.update([0])  # "Hello"
        assert result.new_text == "Hello"

        # The full text accumulates
        assert result.full_text == "Hello"

    def test_accumulation(self):
        """Test text accumulates correctly."""
        tokenizer = MockTokenizer()
        detokenizer = FastIncrementalDetokenizer(tokenizer)

        # Add multiple tokens
        result = detokenizer.update([0, 1])  # "Hello world"
        assert result.full_text == "Hello world"

    def test_reset(self):
        """Test resetting the detokenizer."""
        tokenizer = MockTokenizer()
        detokenizer = FastIncrementalDetokenizer(tokenizer)

        detokenizer.update([0, 1])
        assert detokenizer.output_text == "Hello world"

        detokenizer.reset()
        assert detokenizer.output_text == ""
        assert len(detokenizer.token_ids) == 0

    def test_stop_on_token(self):
        """Test stopping on EOS token."""
        tokenizer = MockTokenizer()
        stop_checker = StopChecker(stop_token_ids={7})  # EOS
        detokenizer = FastIncrementalDetokenizer(
            tokenizer,
            stop_checker=stop_checker,
        )

        result = detokenizer.update([0])  # "Hello"
        assert not result.finished

        result = detokenizer.update([7])  # EOS
        assert result.finished
        assert result.stop_reason == 7


class TestSlowIncrementalDetokenizer:
    """Tests for SlowIncrementalDetokenizer."""

    def test_basic_detokenization(self):
        """Test basic slow detokenization."""
        tokenizer = MockTokenizer()
        detokenizer = SlowIncrementalDetokenizer(tokenizer)

        result = detokenizer.update([0, 1])
        assert result.full_text == "Hello world"


class TestCreateDetokenizer:
    """Tests for create_detokenizer factory."""

    def test_create_fast_detokenizer(self):
        """Test creating fast detokenizer."""
        tokenizer = MockTokenizer()
        detokenizer = create_detokenizer(tokenizer, use_fast=True)

        assert isinstance(detokenizer, FastIncrementalDetokenizer)

    def test_create_with_stop_strings(self):
        """Test creating detokenizer with stop strings."""
        tokenizer = MockTokenizer()
        detokenizer = create_detokenizer(
            tokenizer,
            stop_strings=["STOP"],
            stop_token_ids={7},
        )

        assert detokenizer.stop_checker is not None


class TestDetokenizeIncrementally:
    """Tests for detokenize_incrementally function."""

    def test_full_sequence(self):
        """Test decoding a full sequence."""
        tokenizer = MockTokenizer()

        # Use the slow detokenizer for more predictable results
        detokenizer = SlowIncrementalDetokenizer(tokenizer)

        # Process tokens
        for tid in [0, 1, 2]:  # "Hello world!"
            result = detokenizer.update(tid)

        # Finalize
        result = detokenizer.finalize()
        assert "Hello" in result.full_text
        assert "world" in result.full_text


# ==============================================================================
# Rust Acceleration Tests
# ==============================================================================

@pytest.mark.skipif(not HAS_RUST, reason="Rust core not available")
class TestRustPhase28:
    """Tests for Phase 28 Rust accelerations."""

    def test_request_status_transition(self):
        """Test request status transition validation."""
        # Valid transitions
        assert request_status_transition_rust(0, 2)  # WAITING -> RUNNING
        assert request_status_transition_rust(2, 4)  # RUNNING -> FINISHED_STOPPED
        assert request_status_transition_rust(3, 0)  # PREEMPTED -> WAITING

        # Invalid transitions
        assert not request_status_transition_rust(4, 0)  # FINISHED -> anything
        assert not request_status_transition_rust(0, 4)  # WAITING -> FINISHED

    def test_top_k_mask(self):
        """Test top-k masking."""
        logits = [1.0, 3.0, 2.0, 0.5, 4.0]
        result = top_k_mask_rust(logits, 2)

        # Top-2 are indices 4 (4.0) and 1 (3.0)
        assert result[4] == 4.0
        assert result[1] == 3.0
        assert result[0] == float('-inf')

    def test_top_p_mask(self):
        """Test top-p masking."""
        logits = [10.0, 0.0, 0.0, 0.0]
        result = top_p_mask_rust(logits, 0.5)

        # First token should have highest probability
        assert result[0] == 10.0

    def test_gumbel_sample(self):
        """Test Gumbel sampling."""
        logits = [0.0, 0.0, 10.0, 0.0]  # Token 2 has highest logit

        # With low temperature, should mostly sample token 2
        samples = [gumbel_sample_rust(logits, 0.1, i) for i in range(10)]
        assert 2 in samples

    def test_beam_score(self):
        """Test beam score computation."""
        log_probs = [
            -1.0, -2.0, -3.0,  # Beam 0, vocab 0-2
            -1.5, -2.5, -3.5,  # Beam 1, vocab 0-2
        ]
        prev_scores = [-5.0, -6.0]
        lengths = [3, 4]

        scores = beam_score_rust(log_probs, prev_scores, lengths, 0.6, 3)
        assert len(scores) == 6

    def test_check_stop_tokens(self):
        """Test stop token checking."""
        assert check_stop_tokens_rust(7, [7, 8, 9])
        assert not check_stop_tokens_rust(5, [7, 8, 9])

    def test_update_prefix_offset(self):
        """Test prefix offset update."""
        new_prefix, new_read = update_prefix_offset_rust(10, 0, 0)
        assert new_prefix == 4  # 10 - 6
        assert new_read == 10

        new_prefix, new_read = update_prefix_offset_rust(3, 0, 0)
        assert new_prefix == 0  # < 6 tokens

    def test_compute_penalties(self):
        """Test penalty computation."""
        logits = [1.0, 2.0, 3.0, 4.0]
        token_counts = [(0, 2), (2, 1)]  # Token 0 seen 2x, token 2 seen 1x

        result = compute_penalties_rust(
            logits,
            token_counts,
            repetition_penalty=1.2,
            presence_penalty=0.5,
            frequency_penalty=0.1,
        )

        assert len(result) == 4
        # Penalized tokens should be lower
        assert result[0] < logits[0]
        assert result[2] < logits[2]
        # Unpenalized tokens unchanged
        assert result[1] == logits[1]
        assert result[3] == logits[3]


# ==============================================================================
# Integration Tests
# ==============================================================================

class TestPhase28Integration:
    """Integration tests for Phase 28 components."""

    def test_request_lifecycle_integration(self):
        """Test full request lifecycle."""
        queue = RequestQueue()
        tracker = RequestTracker()

        # Create and add request
        req = Request(
            request_id="int-001",
            prompt="Test prompt",
            prompt_token_ids=[0, 1, 2],
            max_tokens=100,
        )
        queue.add_request(req)

        # Schedule to running
        queue.schedule_next()
        running = queue.get_running_requests()
        assert len(running) == 1

        # Generate tokens
        r = queue.get_request("int-001")
        r.add_output_token(10)
        r.add_output_token(11)

        # Finish
        queue.finish_request("int-001", FinishReason.STOP)
        r = queue.get_request("int-001")
        assert r.is_finished()

        # Track finished request
        tracker.record_request(r)

    def test_engine_with_requests(self):
        """Test engine lifecycle with requests."""
        config = EngineConfig(max_requests=4)
        manager = EngineLifecycleManager(config)

        # Start engine
        manager.start()
        assert manager.state == EngineState.READY

        # Add a request
        req = Request(
            request_id="eng-001",
            prompt="Test",
            max_tokens=50,
        )
        manager.add_request(req)

        # Step should process
        manager.step()
        assert manager._step_count > 0

        # Shutdown
        manager.shutdown(timeout=1.0)
        assert manager.state == EngineState.DEAD

    @pytest.mark.skipif(not HAS_NUMPY, reason="NumPy required")
    def test_sampling_integration(self):
        """Test sampling with state tracking."""
        params = SamplingParams(
            temperature=0.8,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.1,
        )
        pipeline = SamplingPipeline([
            TemperatureSampler(),
            TopKTopPSampler(),
            GumbelSampler(),
        ])

        state = SamplingState(request_id="int-sample-001")
        generated = []

        for i in range(5):
            # Simulate logits
            logits = np.random.randn(1, 1000)  # [batch, vocab]

            token_ids = pipeline.sample(logits, params, state)
            token_id = int(token_ids[0])
            generated.append(token_id)
            state.add_token(token_id)

        assert len(generated) == 5
        assert len(state.generated_ids) == 5

    def test_detokenization_with_stop(self):
        """Test streaming detokenization with stop conditions."""
        tokenizer = MockTokenizer()
        stop_checker = StopChecker(
            stop_token_ids={7},  # EOS
            stop_strings=["?"],  # Also stop on question mark
        )

        detokenizer = create_detokenizer(
            tokenizer,
            stop_strings=["?"],
            stop_token_ids={7},
        )

        # Generate tokens
        tokens = [0, 1, 6]  # "Hello world?"

        for token in tokens:
            result = detokenizer.update(token)
            if result.finished:
                break

        # Should stop on "?"
        assert "Hello" in result.full_text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
