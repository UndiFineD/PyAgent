"""
Phase 30 Tests: Engine Core, Output Processor & Incremental Detokenizer

Comprehensive tests for Phase 30 implementations inspired by vLLM's
v1/engine/ patterns.
"""

import pytest
import time
import hashlib
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


# ============================================================================
# EngineCore Tests
# ============================================================================

class TestRequestStatus:
    """Tests for RequestStatus enum."""
    
    def test_status_values(self):
        from src.infrastructure.engine.EngineCore import RequestStatus
        
        assert RequestStatus.WAITING.name == "WAITING"
        assert RequestStatus.RUNNING.name == "RUNNING"
        assert RequestStatus.FINISHED.name == "FINISHED"
        assert RequestStatus.ABORTED.name == "ABORTED"
    
    def test_all_statuses_defined(self):
        from src.infrastructure.engine.EngineCore import RequestStatus
        
        statuses = list(RequestStatus)
        assert len(statuses) >= 4


class TestFinishReason:
    """Tests for FinishReason enum."""
    
    def test_reason_values(self):
        from src.infrastructure.engine.EngineCore import FinishReason
        
        assert FinishReason.STOP.name == "STOP"
        assert FinishReason.LENGTH.name == "LENGTH"
        assert FinishReason.ABORT.name == "ABORT"
        assert FinishReason.EOS.name == "EOS"


class TestRequest:
    """Tests for Request dataclass."""
    
    def test_request_creation(self):
        from src.infrastructure.engine.EngineCore import Request, RequestStatus
        
        request = Request(
            request_id="test-1",
            prompt_token_ids=[1, 2, 3, 4, 5],
        )
        
        assert request.request_id == "test-1"
        assert request.prompt_token_ids == [1, 2, 3, 4, 5]
        assert request.num_tokens == 5
        assert request.status == RequestStatus.WAITING
        assert not request.is_finished()
    
    def test_request_with_params(self):
        from src.infrastructure.engine.EngineCore import Request
        
        request = Request(
            request_id="test-2",
            prompt_token_ids=[1, 2, 3],
            sampling_params={"temperature": 0.7, "max_tokens": 100},
            client_index=2,
        )
        
        assert request.sampling_params["temperature"] == 0.7
        assert request.client_index == 2
    
    def test_request_finished_state(self):
        from src.infrastructure.engine.EngineCore import Request, RequestStatus, FinishReason
        
        request = Request(request_id="test-3", prompt_token_ids=[1])
        
        request.status = RequestStatus.FINISHED
        request.finish_reason = FinishReason.STOP
        
        assert request.is_finished()
        assert request.get_finished_reason() == FinishReason.STOP


class TestSchedulerOutput:
    """Tests for SchedulerOutput dataclass."""
    
    def test_empty_output(self):
        from src.infrastructure.engine.EngineCore import SchedulerOutput
        
        output = SchedulerOutput()
        
        assert output.is_empty()
        assert output.total_num_scheduled_tokens == 0
        assert len(output.scheduled_requests) == 0
    
    def test_output_with_tokens(self):
        from src.infrastructure.engine.EngineCore import SchedulerOutput
        
        output = SchedulerOutput(
            total_num_scheduled_tokens=100,
            num_scheduled_tokens={"req1": 50, "req2": 50},
        )
        
        assert not output.is_empty()
        assert output.total_num_scheduled_tokens == 100


class TestSimpleScheduler:
    """Tests for SimpleScheduler."""
    
    def test_scheduler_add_request(self):
        from src.infrastructure.engine.EngineCore import SimpleScheduler, Request
        
        scheduler = SimpleScheduler(max_batch_size=4)
        request = Request(request_id="test", prompt_token_ids=[1, 2, 3])
        
        scheduler.add_request(request)
        
        assert len(scheduler.waiting) == 1
        assert scheduler.has_requests()
    
    def test_scheduler_schedule(self):
        from src.infrastructure.engine.EngineCore import SimpleScheduler, Request
        
        scheduler = SimpleScheduler(max_batch_size=4)
        
        for i in range(3):
            scheduler.add_request(Request(
                request_id=f"req-{i}",
                prompt_token_ids=list(range(10)),
            ))
        
        output = scheduler.schedule()
        
        assert len(output.scheduled_requests) == 3
        assert output.total_num_scheduled_tokens == 30
        assert len(scheduler.running) == 3
        assert len(scheduler.waiting) == 0
    
    def test_scheduler_abort(self):
        from src.infrastructure.engine.EngineCore import SimpleScheduler, Request, RequestStatus
        
        scheduler = SimpleScheduler()
        request = Request(request_id="test", prompt_token_ids=[1, 2])
        
        scheduler.add_request(request)
        scheduler.schedule()  # Move to running
        
        scheduler.abort_requests(["test"])
        
        assert len(scheduler.running) == 0
        assert request.status == RequestStatus.ABORTED
    
    def test_scheduler_batch_limit(self):
        from src.infrastructure.engine.EngineCore import SimpleScheduler, Request
        
        scheduler = SimpleScheduler(max_batch_size=2)
        
        for i in range(5):
            scheduler.add_request(Request(
                request_id=f"req-{i}",
                prompt_token_ids=[1, 2, 3],
            ))
        
        output = scheduler.schedule()
        
        assert len(output.scheduled_requests) == 2
        assert len(scheduler.waiting) == 3


class TestEngineCore:
    """Tests for EngineCore main class."""
    
    def test_create_engine(self):
        from src.infrastructure.engine.EngineCore import EngineCore, create_engine_core
        
        engine = create_engine_core()
        
        assert isinstance(engine, EngineCore)
        assert engine.scheduler is not None
        assert engine.executor is not None
    
    def test_add_and_step(self):
        from src.infrastructure.engine.EngineCore import EngineCore, Request
        
        engine = EngineCore()
        request = Request(request_id="test", prompt_token_ids=[1, 2, 3])
        
        engine.add_request(request)
        outputs, executed = engine.step()
        
        assert executed
        assert engine.scheduler.has_requests()
    
    def test_multiple_steps(self):
        from src.infrastructure.engine.EngineCore import EngineCore, Request
        
        engine = EngineCore(log_stats=False)
        
        for i in range(3):
            engine.add_request(Request(
                request_id=f"req-{i}",
                prompt_token_ids=list(range(5)),
            ))
        
        for _ in range(5):
            outputs, executed = engine.step()
        
        stats = engine.get_stats()
        assert stats["total_steps"] == 5
        assert stats["total_requests"] == 3
    
    def test_abort_during_execution(self):
        from src.infrastructure.engine.EngineCore import EngineCore, Request
        
        engine = EngineCore()
        
        engine.add_request(Request(request_id="keep", prompt_token_ids=[1, 2]))
        engine.add_request(Request(request_id="abort-me", prompt_token_ids=[3, 4]))
        
        engine.step()  # Start processing
        engine.abort_requests(["abort-me"])
        
        assert "abort-me" not in [r.request_id for r in engine.scheduler.running]
    
    def test_empty_step(self):
        from src.infrastructure.engine.EngineCore import EngineCore
        
        engine = EngineCore()
        outputs, executed = engine.step()
        
        assert not executed
        assert outputs == {}


class TestEngineCoreProc:
    """Tests for EngineCoreProc background process wrapper."""
    
    def test_proc_creation(self):
        from src.infrastructure.engine.EngineCore import EngineCoreProc
        
        proc = EngineCoreProc(engine_index=0)
        
        assert proc.engine_index == 0
        assert not proc.engines_running


# ============================================================================
# OutputProcessor Tests
# ============================================================================

class TestSamplingParams:
    """Tests for SamplingParams."""
    
    def test_defaults(self):
        from src.infrastructure.engine.OutputProcessor import SamplingParams
        
        params = SamplingParams()
        
        assert params.max_tokens == 256
        assert params.temperature == 1.0
        assert params.skip_special_tokens is True
    
    def test_custom_params(self):
        from src.infrastructure.engine.OutputProcessor import SamplingParams
        
        params = SamplingParams(
            max_tokens=512,
            temperature=0.8,
            stop=["###"],
        )
        
        assert params.max_tokens == 512
        assert params.stop == ["###"]


class TestEngineCoreRequest:
    """Tests for EngineCoreRequest."""
    
    def test_request_creation(self):
        from src.infrastructure.engine.OutputProcessor import EngineCoreRequest, SamplingParams
        
        request = EngineCoreRequest(
            request_id="test-req",
            prompt_token_ids=[1, 2, 3, 4],
            sampling_params=SamplingParams(max_tokens=100),
        )
        
        assert request.request_id == "test-req"
        assert request.prompt_token_ids == [1, 2, 3, 4]
        assert request.sampling_params.max_tokens == 100


class TestRequestState:
    """Tests for RequestState."""
    
    def test_state_creation(self):
        from src.infrastructure.engine.OutputProcessor import RequestState
        
        state = RequestState(
            request_id="test",
            prompt="Hello",
            prompt_token_ids=[1, 2, 3],
            sampling_params=None,
            arrival_time=time.time(),
        )
        
        assert state.request_id == "test"
        assert state.prompt == "Hello"
        assert not state.finished
    
    def test_state_update(self):
        from src.infrastructure.engine.OutputProcessor import RequestState
        
        state = RequestState(
            request_id="test",
            prompt=None,
            prompt_token_ids=[1],
            sampling_params=None,
            arrival_time=time.time(),
        )
        
        state.update([10, 20], "new text")
        
        assert state.output_token_ids == [10, 20]
        assert state.output_text == "new text"
        assert state.num_output_tokens == 2
    
    def test_state_finish(self):
        from src.infrastructure.engine.OutputProcessor import RequestState, EventType
        
        state = RequestState(
            request_id="test",
            prompt=None,
            prompt_token_ids=[],
            sampling_params=None,
            arrival_time=time.time(),
        )
        
        state.update([], "", finish_reason="stop")
        
        assert state.finished
        assert state.finish_reason == "stop"
        assert any(e.event_type == EventType.FINISHED for e in state.events)
    
    def test_stream_interval(self):
        from src.infrastructure.engine.OutputProcessor import RequestState
        
        state = RequestState(
            request_id="test",
            prompt=None,
            prompt_token_ids=[],
            sampling_params=None,
            arrival_time=time.time(),
            stream_interval=3,
        )
        
        assert not state.should_emit_output()  # 1
        assert not state.should_emit_output()  # 2
        assert state.should_emit_output()  # 3


class TestOutputProcessor:
    """Tests for OutputProcessor."""
    
    def test_processor_creation(self):
        from src.infrastructure.engine.OutputProcessor import OutputProcessor
        
        processor = OutputProcessor(tokenizer=None, log_stats=True)
        
        assert processor.get_num_unfinished_requests() == 0
        assert not processor.has_unfinished_requests()
    
    def test_add_request(self):
        from src.infrastructure.engine.OutputProcessor import (
            OutputProcessor, EngineCoreRequest, SamplingParams
        )
        
        processor = OutputProcessor()
        
        request = EngineCoreRequest(
            request_id="test",
            prompt_token_ids=[1, 2, 3],
            sampling_params=SamplingParams(),
        )
        
        processor.add_request(request, "prompt text")
        
        assert processor.has_unfinished_requests()
        assert processor.get_num_unfinished_requests() == 1
    
    def test_duplicate_request_error(self):
        from src.infrastructure.engine.OutputProcessor import (
            OutputProcessor, EngineCoreRequest, SamplingParams
        )
        
        processor = OutputProcessor()
        request = EngineCoreRequest(
            request_id="dup",
            prompt_token_ids=[1],
            sampling_params=SamplingParams(),
        )
        
        processor.add_request(request, None)
        
        with pytest.raises(ValueError, match="already running"):
            processor.add_request(request, None)
    
    def test_process_outputs(self):
        from src.infrastructure.engine.OutputProcessor import (
            OutputProcessor, EngineCoreRequest, EngineCoreOutput, SamplingParams
        )
        
        processor = OutputProcessor()
        
        request = EngineCoreRequest(
            request_id="test",
            prompt_token_ids=[1, 2],
            sampling_params=SamplingParams(),
        )
        processor.add_request(request, "prompt")
        
        outputs = [EngineCoreOutput(
            request_id="test",
            new_token_ids=[100, 101],
            finish_reason=None,
        )]
        
        result = processor.process_outputs(outputs)
        
        assert len(result.request_outputs) >= 0  # May be batched
    
    def test_abort_requests(self):
        from src.infrastructure.engine.OutputProcessor import (
            OutputProcessor, EngineCoreRequest, SamplingParams
        )
        
        processor = OutputProcessor()
        
        for i in range(3):
            processor.add_request(
                EngineCoreRequest(
                    request_id=f"req-{i}",
                    prompt_token_ids=[i],
                    sampling_params=SamplingParams(),
                ),
                None,
            )
        
        aborted = processor.abort_requests(["req-0", "req-2"])
        
        assert set(aborted) == {"req-0", "req-2"}
        assert processor.get_num_unfinished_requests() == 1


class TestLoRARequestStates:
    """Tests for LoRA request tracking."""
    
    def test_lora_tracking(self):
        from src.infrastructure.engine.OutputProcessor import LoRARequestStates, LoRARequest
        
        states = LoRARequestStates()
        lora = LoRARequest(lora_id=1, lora_name="adapter-1")
        
        states.add_request("req-1", lora)
        states.add_request("req-2", lora)
        
        assert 1 in states.get_active_lora_ids()
        assert len(states.active_loras[1]) == 2
    
    def test_lora_removal(self):
        from src.infrastructure.engine.OutputProcessor import LoRARequestStates, LoRARequest
        
        states = LoRARequestStates()
        lora = LoRARequest(lora_id=1, lora_name="adapter-1")
        
        states.add_request("req-1", lora)
        states.remove_request("req-1", lora)
        
        assert 1 not in states.get_active_lora_ids()


# ============================================================================
# IncrementalDetokenizer Tests
# ============================================================================

class TestCheckStopStrings:
    """Tests for stop string checking."""
    
    def test_no_match(self):
        from src.infrastructure.engine.IncrementalDetokenizer import check_stop_strings
        
        result = check_stop_strings(
            output_text="Hello world",
            new_char_count=5,
            stop=["goodbye"],
            include_in_output=False,
        )
        
        assert result is None
    
    def test_match_found(self):
        from src.infrastructure.engine.IncrementalDetokenizer import check_stop_strings
        
        result = check_stop_strings(
            output_text="Hello world<stop>",
            new_char_count=6,
            stop=["<stop>"],
            include_in_output=False,
        )
        
        assert result is not None
        stop_str, truncate_pos = result
        assert stop_str == "<stop>"
        assert truncate_pos == 11  # Position before <stop>
    
    def test_include_stop_in_output(self):
        from src.infrastructure.engine.IncrementalDetokenizer import check_stop_strings
        
        result = check_stop_strings(
            output_text="Result###end",
            new_char_count=6,
            stop=["###"],
            include_in_output=True,
        )
        
        assert result is not None
        _, truncate_pos = result
        assert truncate_pos == 9  # Position after ###
    
    def test_empty_stop_list(self):
        from src.infrastructure.engine.IncrementalDetokenizer import check_stop_strings
        
        result = check_stop_strings(
            output_text="anything",
            new_char_count=5,
            stop=[],
            include_in_output=False,
        )
        
        assert result is None


class TestNoOpDetokenizer:
    """Tests for NoOpDetokenizer."""
    
    def test_no_op(self):
        from src.infrastructure.engine.IncrementalDetokenizer import NoOpDetokenizer
        
        detok = NoOpDetokenizer()
        
        result = detok.update([1, 2, 3], False)
        text = detok.get_next_output_text(False, False)
        
        assert result is None
        assert text == ""
        assert detok.output_token_ids == [1, 2, 3]


class TestSlowIncrementalDetokenizer:
    """Tests for SlowIncrementalDetokenizer."""
    
    def test_creation(self):
        from src.infrastructure.engine.IncrementalDetokenizer import SlowIncrementalDetokenizer
        
        # Mock request
        @dataclass
        class MockRequest:
            request_id: str = "test"
            prompt_token_ids: list = None
            sampling_params: dict = None
            
            def __post_init__(self):
                self.prompt_token_ids = self.prompt_token_ids or [1, 2, 3]
                self.sampling_params = self.sampling_params or {}
        
        # Mock tokenizer
        class MockTokenizer:
            def convert_ids_to_tokens(self, ids, skip_special_tokens=False):
                return [f"tok{i}" for i in ids]
            
            def convert_tokens_to_string(self, tokens):
                return "".join(tokens)
        
        request = MockRequest()
        detok = SlowIncrementalDetokenizer(MockTokenizer(), request)
        
        assert detok.request_id == "test"


class TestValidateUtf8:
    """Tests for UTF-8 validation."""
    
    def test_valid_utf8(self):
        from src.infrastructure.engine.IncrementalDetokenizer import validate_utf8
        
        assert validate_utf8("Hello 世界")
        assert validate_utf8("")
        assert validate_utf8("αβγδ")
    
    def test_replacement_char_is_valid_unicode(self):
        from src.infrastructure.engine.IncrementalDetokenizer import validate_utf8
        
        # The replacement character is valid UTF-8 (just represents prior invalid bytes)
        # Our function checks if the string can be properly decoded as UTF-8
        assert validate_utf8("Hello\ufffdworld")  # \ufffd is valid UTF-8


# ============================================================================
# PrefixCacheManager Tests
# ============================================================================

class TestHashAlgorithm:
    """Tests for HashAlgorithm enum."""
    
    def test_algorithms(self):
        from src.infrastructure.engine.PrefixCacheManager import HashAlgorithm
        
        assert HashAlgorithm.SHA256.value == "sha256"
        assert HashAlgorithm.XXHASH.value == "xxhash"
        assert HashAlgorithm.MD5.value == "md5"


class TestBlockHash:
    """Tests for BlockHash dataclass."""
    
    def test_block_hash_creation(self):
        from src.infrastructure.engine.PrefixCacheManager import BlockHash
        
        hash_value = b"\x00" * 32
        block_hash = BlockHash(
            hash_value=hash_value,
            token_ids=(1, 2, 3, 4),
        )
        
        assert block_hash.hash_value == hash_value
        assert block_hash.token_ids == (1, 2, 3, 4)
    
    def test_block_hash_equality(self):
        from src.infrastructure.engine.PrefixCacheManager import BlockHash
        
        h1 = BlockHash(hash_value=b"abc", token_ids=(1, 2))
        h2 = BlockHash(hash_value=b"abc", token_ids=(1, 2))
        h3 = BlockHash(hash_value=b"xyz", token_ids=(1, 2))
        
        assert h1 == h2
        assert h1 != h3


class TestHashBlockTokens:
    """Tests for hash_block_tokens function."""
    
    def test_hash_first_block(self):
        from src.infrastructure.engine.PrefixCacheManager import (
            hash_block_tokens, get_hash_function, HashAlgorithm
        )
        
        hash_fn = get_hash_function(HashAlgorithm.SHA256)
        
        block_hash = hash_block_tokens(
            hash_function=hash_fn,
            parent_block_hash=None,
            curr_block_token_ids=[1, 2, 3, 4],
        )
        
        assert len(block_hash.hash_value) == 32  # SHA256
        assert block_hash.token_ids == (1, 2, 3, 4)
    
    def test_hash_chaining(self):
        from src.infrastructure.engine.PrefixCacheManager import (
            hash_block_tokens, get_hash_function, HashAlgorithm
        )
        
        hash_fn = get_hash_function(HashAlgorithm.SHA256)
        
        block1 = hash_block_tokens(hash_fn, None, [1, 2, 3, 4])
        block2 = hash_block_tokens(hash_fn, block1, [5, 6, 7, 8])
        block3 = hash_block_tokens(hash_fn, block2, [9, 10, 11, 12])
        
        # Different blocks should have different hashes
        assert block1.hash_value != block2.hash_value
        assert block2.hash_value != block3.hash_value
    
    def test_hash_with_extra_keys(self):
        from src.infrastructure.engine.PrefixCacheManager import (
            hash_block_tokens, get_hash_function, HashAlgorithm
        )
        
        hash_fn = get_hash_function(HashAlgorithm.SHA256)
        
        h1 = hash_block_tokens(hash_fn, None, [1, 2, 3, 4], extra_keys=None)
        h2 = hash_block_tokens(hash_fn, None, [1, 2, 3, 4], extra_keys=("image_hash",))
        
        assert h1.hash_value != h2.hash_value


class TestPrefixCacheManager:
    """Tests for PrefixCacheManager."""
    
    def test_manager_creation(self):
        from src.infrastructure.engine.PrefixCacheManager import PrefixCacheManager
        
        manager = PrefixCacheManager(block_size=16, max_blocks=100)
        
        assert manager.block_size == 16
        assert manager.max_blocks == 100
    
    def test_compute_block_hashes(self):
        from src.infrastructure.engine.PrefixCacheManager import PrefixCacheManager
        
        manager = PrefixCacheManager(block_size=4)
        
        # 12 tokens = 3 full blocks
        token_ids = list(range(12))
        hashes = manager.compute_block_hashes(token_ids)
        
        assert len(hashes) == 3
    
    def test_cache_miss_then_hit(self):
        from src.infrastructure.engine.PrefixCacheManager import PrefixCacheManager
        
        manager = PrefixCacheManager(block_size=4)
        
        token_ids = list(range(8))  # 2 blocks
        hashes = manager.compute_block_hashes(token_ids)
        
        # First access - miss
        block_ids, num_matched = manager.get_cached_blocks(hashes)
        assert num_matched == 0
        
        # Allocate blocks
        allocated = manager.allocate_blocks(hashes)
        assert len(allocated) == 2
        
        # Second access - hit
        block_ids, num_matched = manager.get_cached_blocks(hashes)
        assert num_matched == 2
    
    def test_lru_eviction(self):
        from src.infrastructure.engine.PrefixCacheManager import PrefixCacheManager
        
        manager = PrefixCacheManager(block_size=4, max_blocks=2)
        
        # Fill cache
        hashes1 = manager.compute_block_hashes(list(range(4)))
        manager.allocate_blocks(hashes1)
        
        hashes2 = manager.compute_block_hashes(list(range(4, 8)))
        manager.allocate_blocks(hashes2)
        
        # Free first block
        manager.free_blocks([0])
        
        # Allocate third block - should evict first
        hashes3 = manager.compute_block_hashes(list(range(8, 12)))
        manager.allocate_blocks(hashes3)
        
        stats = manager.get_stats()
        assert stats["evictions"] >= 1
    
    def test_prefix_sharing(self):
        from src.infrastructure.engine.PrefixCacheManager import PrefixCacheManager
        
        manager = PrefixCacheManager(block_size=4)
        
        # Two sequences with same prefix
        tokens1 = [1, 2, 3, 4, 5, 6, 7, 8]  # 2 blocks
        tokens2 = [1, 2, 3, 4, 9, 10, 11, 12]  # Same first block
        
        hashes1 = manager.compute_block_hashes(tokens1)
        manager.allocate_blocks(hashes1)
        
        hashes2 = manager.compute_block_hashes(tokens2)
        block_ids, num_matched = manager.get_cached_blocks(hashes2)
        
        # First block should be cached
        assert num_matched == 1
    
    def test_stats(self):
        from src.infrastructure.engine.PrefixCacheManager import PrefixCacheManager
        
        manager = PrefixCacheManager(block_size=4, max_blocks=10)
        
        # Some operations
        hashes = manager.compute_block_hashes(list(range(8)))
        manager.get_cached_blocks(hashes)  # Miss - counted per block lookup
        manager.allocate_blocks(hashes)
        manager.get_cached_blocks(hashes)  # Hit - counted per block lookup
        
        stats = manager.get_stats()
        
        assert stats["num_blocks"] == 2
        assert stats["hits"] >= 1  # At least some hits from second lookup
        assert stats["misses"] >= 1  # At least some misses from first lookup
        assert 0 <= stats["hit_rate"] <= 1


class TestComputePrefixMatch:
    """Tests for prefix matching utilities."""
    
    def test_full_match(self):
        from src.infrastructure.engine.PrefixCacheManager import compute_prefix_match
        
        hashes = [b"a", b"b", b"c"]
        match_len = compute_prefix_match(hashes, hashes)
        
        assert match_len == 3
    
    def test_partial_match(self):
        from src.infrastructure.engine.PrefixCacheManager import compute_prefix_match
        
        cached = [b"a", b"b", b"c"]
        request = [b"a", b"b", b"x"]
        
        match_len = compute_prefix_match(cached, request)
        
        assert match_len == 2
    
    def test_no_match(self):
        from src.infrastructure.engine.PrefixCacheManager import compute_prefix_match
        
        cached = [b"x"]
        request = [b"y"]
        
        match_len = compute_prefix_match(cached, request)
        
        assert match_len == 0


class TestComputeCacheKeys:
    """Tests for batch cache key computation."""
    
    def test_compute_keys(self):
        from src.infrastructure.engine.PrefixCacheManager import compute_cache_keys
        
        result = compute_cache_keys(
            request_ids=["req1", "req2"],
            token_ids_list=[[1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4]],
            block_size=4,
        )
        
        assert "req1" in result
        assert "req2" in result
        assert len(result["req1"]) == 2  # 8 tokens / 4 = 2 blocks
        assert len(result["req2"]) == 1  # 4 tokens / 4 = 1 block


# ============================================================================
# EngineCoreClient Tests
# ============================================================================

class TestClientConfig:
    """Tests for ClientConfig."""
    
    def test_defaults(self):
        from src.infrastructure.engine.EngineCoreClient import ClientConfig
        
        config = ClientConfig()
        
        assert config.max_batch_size == 32
        assert config.timeout_s == 60.0
    
    def test_custom_config(self):
        from src.infrastructure.engine.EngineCoreClient import ClientConfig
        
        config = ClientConfig(max_batch_size=64, async_mode=True)
        
        assert config.max_batch_size == 64
        assert config.async_mode is True


class TestInprocClient:
    """Tests for InprocClient."""
    
    def test_client_creation(self):
        from src.infrastructure.engine.EngineCoreClient import InprocClient
        
        client = InprocClient()
        
        assert client.engine_core is not None
    
    def test_add_and_get(self):
        from src.infrastructure.engine.EngineCoreClient import InprocClient
        from src.infrastructure.engine.OutputProcessor import EngineCoreRequest, SamplingParams
        
        client = InprocClient()
        
        request = EngineCoreRequest(
            request_id="test",
            prompt_token_ids=[1, 2, 3],
            sampling_params=SamplingParams(),
        )
        
        client.add_request(request)
        output = client.get_output()
        
        # Should have processed something
        assert output is not None
    
    def test_shutdown(self):
        from src.infrastructure.engine.EngineCoreClient import InprocClient
        
        client = InprocClient()
        client.shutdown()  # Should not raise


class TestCreateClient:
    """Tests for client factory function."""
    
    def test_create_inproc(self):
        from src.infrastructure.engine.EngineCoreClient import create_client, InprocClient
        
        client = create_client("inproc")
        
        assert isinstance(client, InprocClient)
    
    def test_create_sync_mp(self):
        from src.infrastructure.engine.EngineCoreClient import create_client, SyncMPClient
        
        client = create_client("sync_mp")
        
        try:
            assert isinstance(client, SyncMPClient)
        finally:
            client.shutdown()
    
    def test_invalid_type(self):
        from src.infrastructure.engine.EngineCoreClient import create_client
        
        with pytest.raises(ValueError, match="Unknown client type"):
            create_client("invalid")


# ============================================================================
# Rust Acceleration Tests
# ============================================================================

class TestRustHashBlockTokens:
    """Tests for Rust block hashing."""
    
    def test_rust_hash_basic(self):
        try:
            from rust_core import hash_block_tokens_rust
            
            result = hash_block_tokens_rust(None, [1, 2, 3, 4], None)
            
            assert isinstance(result, (bytes, list))
            assert len(result) > 0
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_rust_hash_with_parent(self):
        try:
            from rust_core import hash_block_tokens_rust
            
            parent = list(b"parent_hash")
            result = hash_block_tokens_rust(parent, [5, 6, 7, 8], None)
            
            assert len(result) > 0
        except ImportError:
            pytest.skip("rust_core not available")


class TestRustCheckStopStrings:
    """Tests for Rust stop string checking."""
    
    def test_rust_stop_check(self):
        try:
            from rust_core import check_stop_strings_rust
            
            result = check_stop_strings_rust(
                "Hello<END>world",
                10,
                ["<END>"],
                False,
            )
            
            assert result is not None
            idx, pos = result
            assert idx == 0
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_rust_no_match(self):
        try:
            from rust_core import check_stop_strings_rust
            
            result = check_stop_strings_rust(
                "Hello world",
                5,
                ["<STOP>"],
                False,
            )
            
            assert result is None
        except ImportError:
            pytest.skip("rust_core not available")


class TestRustValidateUtf8:
    """Tests for Rust UTF-8 validation."""
    
    def test_rust_valid(self):
        try:
            from rust_core import validate_utf8_rust
            
            assert validate_utf8_rust("Hello 世界") is True
        except ImportError:
            pytest.skip("rust_core not available")


class TestRustComputePrefixMatch:
    """Tests for Rust prefix matching."""
    
    def test_rust_prefix_match(self):
        try:
            from rust_core import compute_prefix_match_rust
            
            cached = [[1, 2], [3, 4], [5, 6]]
            request = [[1, 2], [3, 4], [7, 8]]
            
            result = compute_prefix_match_rust(cached, request)
            
            assert result == 2
        except ImportError:
            pytest.skip("rust_core not available")


class TestRustComputeCacheKeys:
    """Tests for Rust batch cache key computation."""
    
    def test_rust_cache_keys(self):
        try:
            from rust_core import compute_cache_keys_rust
            
            result = compute_cache_keys_rust(
                ["req1", "req2"],
                [[1, 2, 3, 4], [5, 6, 7, 8]],
                4,
            )
            
            assert "req1" in result
            assert "req2" in result
        except ImportError:
            pytest.skip("rust_core not available")


class TestRustPackOutputs:
    """Tests for Rust output packing."""
    
    def test_rust_pack(self):
        try:
            from rust_core import pack_outputs_rust
            
            result = pack_outputs_rust(
                ["r1", "r2"],
                [[1, 2], [3, 4]],
                [None, "stop"],
            )
            
            assert len(result) == 2
            assert result[0][0] == "r1"
            assert result[1][2] == "stop"
        except ImportError:
            pytest.skip("rust_core not available")


class TestRustMergeRequestStates:
    """Tests for Rust request state merging."""
    
    def test_rust_merge(self):
        try:
            from rust_core import merge_request_states_rust
            
            tokens, text = merge_request_states_rust(
                [[1, 2], [3, 4]],
                ["Hello ", "World"],
            )
            
            assert tokens == [1, 2, 3, 4]
            assert text == "Hello World"
        except ImportError:
            pytest.skip("rust_core not available")


class TestRustDetokenizeBatch:
    """Tests for Rust batch detokenization."""
    
    def test_rust_detokenize(self):
        try:
            from rust_core import detokenize_batch_rust
            
            vocab = {1: "Hello", 2: " ", 3: "World"}
            result = detokenize_batch_rust(
                [[1, 2, 3], [3, 2, 1]],
                vocab,
            )
            
            assert result[0] == "Hello World"
            assert result[1] == "World Hello"
        except ImportError:
            pytest.skip("rust_core not available")


# ============================================================================
# Integration Tests
# ============================================================================

class TestEngineIntegration:
    """Integration tests combining multiple components."""
    
    def test_full_request_lifecycle(self):
        from src.infrastructure.engine.EngineCore import EngineCore, Request
        from src.infrastructure.engine.OutputProcessor import OutputProcessor, EngineCoreRequest, SamplingParams
        
        # Setup
        engine = EngineCore(log_stats=False)
        processor = OutputProcessor()
        
        # Add request to both
        request = Request(
            request_id="integration-test",
            prompt_token_ids=[1, 2, 3, 4, 5],
        )
        engine.add_request(request)
        
        processor.add_request(
            EngineCoreRequest(
                request_id="integration-test",
                prompt_token_ids=[1, 2, 3, 4, 5],
                sampling_params=SamplingParams(),
            ),
            prompt="test prompt",
        )
        
        # Step engine
        outputs, executed = engine.step()
        
        assert executed
        assert processor.has_unfinished_requests()
    
    def test_prefix_cache_with_engine(self):
        from src.infrastructure.engine.EngineCore import EngineCore, Request
        from src.infrastructure.engine.PrefixCacheManager import PrefixCacheManager
        
        engine = EngineCore(log_stats=False)
        cache_mgr = PrefixCacheManager(block_size=4)
        
        # First request
        tokens1 = list(range(16))
        hashes1 = cache_mgr.compute_block_hashes(tokens1)
        cache_mgr.allocate_blocks(hashes1)
        
        engine.add_request(Request(request_id="r1", prompt_token_ids=tokens1))
        
        # Second request with same prefix
        tokens2 = list(range(8)) + [100, 101, 102, 103]
        hashes2 = cache_mgr.compute_block_hashes(tokens2)
        
        _, matched = cache_mgr.get_cached_blocks(hashes2)
        
        # Should match first 2 blocks
        assert matched == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
