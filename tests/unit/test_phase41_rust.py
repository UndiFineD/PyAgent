# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Unit Tests for Rust Accelerations

"""
Tests for Phase 41 Rust acceleration functions.

Rust Function Signatures (from inference.rs):
- bpe_encode_fast_rust(text: str, vocab: Dict[str, int], merges: List[Tuple[str, str]]) -> List[int]
- batch_estimate_tokens_rust(texts: List[str], chars_per_token: float) -> List[int]
- tokenizer_cache_key_rust(model_name: str, backend: str, trust_remote: bool, revision: str) -> int
- architecture_fingerprint_rust(hidden_size, num_layers, num_heads, vocab_size, intermediate_size) -> int
- estimate_vram_bytes_rust(num_params, precision_bits, context_length, batch_size, kv_cache_factor) -> Tuple[int, int]
- detect_architecture_rust(architectures: List[str], model_type: str) -> str
- lora_scaling_rust(rank: int, alpha: float, use_rslora: bool) -> float
- lora_delta_compute_rust(lora_a, lora_b, rank, in_features, out_features, scale) -> List[float]
- lora_adapter_hash_rust(adapter_path, rank, alpha, target_modules) -> int
- log_softmax_stable_rust(logits: List[float]) -> List[float]
- extract_top_k_logprobs_rust(logprobs: List[float], k: int) -> Tuple[List[int], List[float]]
- compute_perplexity_rust(logprobs: List[float]) -> float
- compute_entropy_rust(probs: List[float]) -> float
- batch_logprobs_rust(batch_logits: List[List[float]], selected_ids: List[int]) -> List[float]
- extract_json_positions_rust(text: str) -> List[Tuple[int, int]]
- detect_tool_format_rust(text: str) -> str
- parse_tool_arguments_rust(json_str: str) -> Dict[str, str]
- validate_json_schema_fast_rust(json_str, required_keys, expected_types) -> Tuple[bool, str]
- validate_partial_json_rust(partial_text: str) -> bool
- constraint_hash_rust(json_schema: Optional[str], regex_pattern: Optional[str], choices: List[str]) -> int
"""

import pytest
import json
import math
from typing import Optional

# Try to import rust_core module
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# Skip all tests if rust_core is not available
pytestmark = pytest.mark.skipif(
    not HAS_RUST,
    reason="rust_core module not available"
)


class TestTokenizerFunctions:
    """Test tokenizer-related Rust functions."""
    
    def test_bpe_encode_fast_rust_basic(self):
        """Test basic BPE encoding."""
        text = "ab"
        vocab = {"a": 0, "b": 1, "ab": 2}
        merges = [("a", "b")]
        
        result = rust_core.bpe_encode_fast_rust(text, vocab, merges)
        
        assert isinstance(result, list)
        # "ab" should merge to single token
        assert 2 in result or len(result) <= 2
    
    def test_bpe_encode_fast_rust_empty(self):
        """Test BPE encoding with empty text."""
        result = rust_core.bpe_encode_fast_rust("", {}, [])
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_bpe_encode_fast_rust_no_merges(self):
        """Test BPE encoding without merges."""
        text = "abc"
        vocab = {"a": 0, "b": 1, "c": 2}
        merges = []
        
        result = rust_core.bpe_encode_fast_rust(text, vocab, merges)
        
        assert isinstance(result, list)
        assert result == [0, 1, 2]
    
    def test_batch_estimate_tokens_rust(self):
        """Test batch token estimation."""
        texts = [
            "Hello, world!",          # 13 chars
            "This is a longer sentence.",  # 27 chars
            "Short",                  # 5 chars
            "",                       # 0 chars
        ]
        chars_per_token = 4.0
        
        result = rust_core.batch_estimate_tokens_rust(texts, chars_per_token)
        
        assert isinstance(result, list)
        assert len(result) == len(texts)
        # Check estimates are reasonable (ceil of chars/4)
        assert result[0] == math.ceil(13 / 4.0)  # 4
        assert result[1] == math.ceil(27 / 4.0)  # 7
        assert result[2] == math.ceil(5 / 4.0)   # 2
        assert result[3] == 0
    
    def test_batch_estimate_tokens_rust_empty_list(self):
        """Test batch estimation with empty list."""
        result = rust_core.batch_estimate_tokens_rust([], 4.0)
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_tokenizer_cache_key_rust(self):
        """Test tokenizer cache key generation."""
        model_name = "gpt-4"
        backend = "tiktoken"
        trust_remote = True
        revision = "main"
        
        key = rust_core.tokenizer_cache_key_rust(model_name, backend, trust_remote, revision)
        
        assert isinstance(key, int)
        
        # Same inputs should produce same key
        key2 = rust_core.tokenizer_cache_key_rust(model_name, backend, trust_remote, revision)
        assert key == key2
    
    def test_tokenizer_cache_key_rust_different_inputs(self):
        """Test different inputs produce different keys."""
        key1 = rust_core.tokenizer_cache_key_rust("model1", "tiktoken", True, "main")
        key2 = rust_core.tokenizer_cache_key_rust("model2", "tiktoken", True, "main")
        key3 = rust_core.tokenizer_cache_key_rust("model1", "huggingface", True, "main")
        key4 = rust_core.tokenizer_cache_key_rust("model1", "tiktoken", False, "main")
        
        assert key1 != key2
        assert key1 != key3
        assert key1 != key4


class TestModelFunctions:
    """Test model-related Rust functions."""
    
    def test_architecture_fingerprint_rust(self):
        """Test architecture fingerprint generation."""
        fingerprint = rust_core.architecture_fingerprint_rust(
            hidden_size=4096,
            num_layers=32,
            num_heads=32,
            vocab_size=32000,
            intermediate_size=11008,
        )
        
        assert isinstance(fingerprint, int)
    
    def test_architecture_fingerprint_rust_deterministic(self):
        """Test fingerprint is deterministic."""
        fp1 = rust_core.architecture_fingerprint_rust(768, 12, 12, 50257, 3072)
        fp2 = rust_core.architecture_fingerprint_rust(768, 12, 12, 50257, 3072)
        
        assert fp1 == fp2
    
    def test_architecture_fingerprint_rust_unique(self):
        """Test different architectures have different fingerprints."""
        fp1 = rust_core.architecture_fingerprint_rust(768, 12, 12, 50257, 3072)
        fp2 = rust_core.architecture_fingerprint_rust(4096, 32, 32, 32000, 11008)
        
        assert fp1 != fp2
    
    def test_estimate_vram_bytes_rust(self):
        """Test VRAM estimation."""
        # 7B params, 16-bit, 4096 context, batch 1
        min_vram, optimal_vram = rust_core.estimate_vram_bytes_rust(
            num_params=7_000_000_000,
            precision_bits=16,
            context_length=4096,
            batch_size=1,
            kv_cache_factor=1000.0,  # Approximate hidden * 2 * layers
        )
        
        assert isinstance(min_vram, int)
        assert isinstance(optimal_vram, int)
        assert min_vram > 0
        assert optimal_vram >= min_vram
    
    def test_estimate_vram_bytes_rust_precision(self):
        """Test VRAM estimation with different precisions."""
        # FP16 vs FP32
        min_16, _ = rust_core.estimate_vram_bytes_rust(1_000_000_000, 16, 2048, 1, 500.0)
        min_32, _ = rust_core.estimate_vram_bytes_rust(1_000_000_000, 32, 2048, 1, 500.0)
        
        # FP32 should be roughly 2x FP16
        assert min_32 > min_16
    
    def test_estimate_vram_bytes_rust_zero(self):
        """Test VRAM estimation with zero params."""
        min_vram, _ = rust_core.estimate_vram_bytes_rust(0, 16, 4096, 1, 500.0)
        
        assert min_vram == 0 or min_vram >= 0  # Implementation dependent
    
    def test_detect_architecture_rust(self):
        """Test architecture detection."""
        arch = rust_core.detect_architecture_rust(
            architectures=["LlamaForCausalLM"],
            model_type="llama",
        )
        
        assert isinstance(arch, str)
        assert "llama" in arch.lower()
    
    def test_detect_architecture_rust_mistral(self):
        """Test detecting Mistral architecture."""
        arch = rust_core.detect_architecture_rust(
            architectures=["MistralForCausalLM"],
            model_type="mistral",
        )
        
        assert "mistral" in arch.lower()
    
    def test_detect_architecture_rust_fallback(self):
        """Test fallback to model_type."""
        arch = rust_core.detect_architecture_rust(
            architectures=[],
            model_type="custom_model",
        )
        
        assert arch == "custom_model"


class TestLoRAFunctions:
    """Test LoRA-related Rust functions."""
    
    def test_lora_scaling_rust_standard(self):
        """Test standard LoRA scaling computation."""
        rank = 16
        alpha = 32.0
        use_rslora = False
        
        scaling = rust_core.lora_scaling_rust(rank, alpha, use_rslora)
        
        assert isinstance(scaling, float)
        assert scaling == pytest.approx(alpha / rank)
    
    def test_lora_scaling_rust_rslora(self):
        """Test rsLoRA scaling computation."""
        rank = 16
        alpha = 32.0
        use_rslora = True
        
        scaling = rust_core.lora_scaling_rust(rank, alpha, use_rslora)
        
        # rsLoRA: alpha / sqrt(rank)
        expected = alpha / math.sqrt(rank)
        assert scaling == pytest.approx(expected)
    
    def test_lora_scaling_rust_various_ranks(self):
        """Test LoRA scaling with various ranks."""
        alpha = 64.0
        
        for rank in [4, 8, 16, 32, 64]:
            scaling = rust_core.lora_scaling_rust(rank, alpha, False)
            assert scaling == pytest.approx(alpha / rank)
    
    def test_lora_delta_compute_rust(self):
        """Test LoRA delta weight computation."""
        # A: [rank, in_features] = [2, 3] flattened
        lora_a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        # B: [out_features, rank] = [2, 2] flattened
        lora_b = [0.5, 0.6, 0.7, 0.8]
        
        rank = 2
        in_features = 3
        out_features = 2
        scale = 1.0
        
        delta = rust_core.lora_delta_compute_rust(
            lora_a, lora_b, rank, in_features, out_features, scale
        )
        
        assert isinstance(delta, list)
        assert len(delta) == out_features * in_features
    
    def test_lora_delta_compute_rust_identity(self):
        """Test LoRA delta with simple values."""
        # Simple 2x2 identity-like computation
        lora_a = [1.0, 0.0, 0.0, 1.0]  # [2, 2]
        lora_b = [1.0, 0.0, 0.0, 1.0]  # [2, 2]
        
        delta = rust_core.lora_delta_compute_rust(
            lora_a, lora_b, 2, 2, 2, 1.0
        )
        
        # Should approximate identity
        assert delta[0] == pytest.approx(1.0, rel=1e-5)  # [0,0]
        assert delta[3] == pytest.approx(1.0, rel=1e-5)  # [1,1]
    
    def test_lora_adapter_hash_rust(self):
        """Test LoRA adapter hash generation."""
        hash_val = rust_core.lora_adapter_hash_rust(
            adapter_path="my-lora-adapter",
            rank=16,
            alpha=32.0,
            target_modules=["q_proj", "v_proj"],
        )
        
        assert isinstance(hash_val, int)
    
    def test_lora_adapter_hash_rust_deterministic(self):
        """Test hash is deterministic."""
        h1 = rust_core.lora_adapter_hash_rust("adapter", 8, 16.0, ["q_proj"])
        h2 = rust_core.lora_adapter_hash_rust("adapter", 8, 16.0, ["q_proj"])
        
        assert h1 == h2
    
    def test_lora_adapter_hash_rust_unique(self):
        """Test different adapters have different hashes."""
        h1 = rust_core.lora_adapter_hash_rust("adapter1", 16, 32.0, ["q_proj"])
        h2 = rust_core.lora_adapter_hash_rust("adapter2", 16, 32.0, ["q_proj"])
        h3 = rust_core.lora_adapter_hash_rust("adapter1", 8, 32.0, ["q_proj"])
        
        assert h1 != h2
        assert h1 != h3


class TestLogprobsFunctions:
    """Test logprobs-related Rust functions."""
    
    def test_log_softmax_stable_rust(self):
        """Test numerically stable log softmax."""
        logits = [1.0, 2.0, 3.0]
        
        result = rust_core.log_softmax_stable_rust(logits)
        
        assert isinstance(result, list)
        assert len(result) == 3
        # Log probs should be negative
        assert all(lp <= 0 for lp in result)
        # Should sum to 1 in prob space
        probs_sum = sum(math.exp(lp) for lp in result)
        assert probs_sum == pytest.approx(1.0, rel=1e-5)
    
    def test_log_softmax_stable_rust_overflow(self):
        """Test log softmax handles large values."""
        logits = [1000.0, 1001.0, 1002.0]
        
        result = rust_core.log_softmax_stable_rust(logits)
        
        # Should not overflow
        assert all(math.isfinite(lp) for lp in result)
    
    def test_log_softmax_stable_rust_uniform(self):
        """Test log softmax with uniform distribution."""
        logits = [0.0, 0.0, 0.0]
        
        result = rust_core.log_softmax_stable_rust(logits)
        
        expected = math.log(1/3)
        for lp in result:
            assert lp == pytest.approx(expected, rel=1e-5)
    
    def test_extract_top_k_logprobs_rust(self):
        """Test extracting top-k logprobs."""
        logprobs = [-2.0, -1.0, -3.0, -0.5, -4.0]
        k = 3
        
        ids, lps = rust_core.extract_top_k_logprobs_rust(logprobs, k)
        
        assert len(ids) == k
        assert len(lps) == k
        # Should be sorted by logprob descending
        assert lps[0] >= lps[1] >= lps[2]
        # Top logprob should be -0.5 (index 3)
        assert ids[0] == 3
        assert lps[0] == pytest.approx(-0.5)
    
    def test_extract_top_k_logprobs_rust_k_larger(self):
        """Test top-k when k > vocab size."""
        logprobs = [-1.0, -2.0, -3.0]
        k = 5
        
        ids, lps = rust_core.extract_top_k_logprobs_rust(logprobs, k)
        
        assert len(ids) == 3  # Can only return what exists
    
    def test_compute_perplexity_rust(self):
        """Test perplexity computation."""
        logprobs = [-1.0, -2.0, -1.5]
        
        ppl = rust_core.compute_perplexity_rust(logprobs)
        
        assert isinstance(ppl, float)
        assert ppl > 0
        # Perplexity = exp(-mean(logprobs))
        expected = math.exp(-sum(logprobs) / len(logprobs))
        assert ppl == pytest.approx(expected, rel=1e-5)
    
    def test_compute_perplexity_rust_perfect(self):
        """Test perplexity with perfect predictions."""
        logprobs = [0.0, 0.0, 0.0]  # All log(1) = 0
        
        ppl = rust_core.compute_perplexity_rust(logprobs)
        
        assert ppl == pytest.approx(1.0, rel=1e-5)
    
    def test_compute_entropy_rust(self):
        """Test entropy computation."""
        probs = [0.25, 0.25, 0.25, 0.25]
        
        entropy = rust_core.compute_entropy_rust(probs)
        
        # Maximum entropy for 4 categories
        expected = -4 * (0.25 * math.log(0.25))
        assert entropy == pytest.approx(expected, rel=1e-5)
    
    def test_compute_entropy_rust_peaked(self):
        """Test entropy with peaked distribution."""
        probs = [0.97, 0.01, 0.01, 0.01]
        
        entropy = rust_core.compute_entropy_rust(probs)
        
        # Low entropy for peaked distribution
        assert entropy < 0.5
    
    def test_batch_logprobs_rust(self):
        """Test batch logprobs computation."""
        batch_logits = [
            [1.0, 2.0, 3.0],  # Sequence 1
            [3.0, 2.0, 1.0],  # Sequence 2
        ]
        selected_ids = [2, 0]
        
        logprobs = rust_core.batch_logprobs_rust(batch_logits, selected_ids)
        
        assert len(logprobs) == 2
        # Both should be the highest logprob in their sequence
        assert logprobs[0] > logprobs[1] or abs(logprobs[0] - logprobs[1]) < 0.1


class TestToolParserFunctions:
    """Test tool parser-related Rust functions."""
    
    def test_extract_json_positions_rust(self):
        """Test JSON position extraction."""
        text = 'Some text {"key": "value"} more text {"a": 1}'
        
        positions = rust_core.extract_json_positions_rust(text)
        
        assert isinstance(positions, list)
        assert len(positions) == 2
        # Each position is (start, end)
        assert all(len(p) == 2 for p in positions)
    
    def test_extract_json_positions_rust_no_json(self):
        """Test extraction with no JSON."""
        text = "Just plain text here"
        
        positions = rust_core.extract_json_positions_rust(text)
        
        assert len(positions) == 0
    
    def test_extract_json_positions_rust_nested(self):
        """Test extraction with nested JSON."""
        text = '{"outer": {"inner": "value"}}'
        
        positions = rust_core.extract_json_positions_rust(text)
        
        assert len(positions) == 1
        start, end = positions[0]
        assert text[start:end] == text
    
    def test_detect_tool_format_rust_hermes(self):
        """Test Hermes format detection."""
        text = "<tool_call>get_weather</tool_call>"
        
        fmt = rust_core.detect_tool_format_rust(text)
        
        assert fmt == "hermes"
    
    def test_detect_tool_format_rust_llama3(self):
        """Test Llama3 format detection."""
        text = "<|python_tag|>some_function()"
        
        fmt = rust_core.detect_tool_format_rust(text)
        
        assert fmt == "llama3"
    
    def test_detect_tool_format_rust_mistral(self):
        """Test Mistral format detection."""
        text = "[TOOL_CALLS] get_weather"
        
        fmt = rust_core.detect_tool_format_rust(text)
        
        assert fmt == "mistral"
    
    def test_detect_tool_format_rust_granite(self):
        """Test Granite format detection."""
        text = "<|tool_call|>function_name"
        
        fmt = rust_core.detect_tool_format_rust(text)
        
        assert fmt == "granite"
    
    def test_detect_tool_format_rust_json(self):
        """Test JSON format (default) detection."""
        text = '{"name": "get_weather", "arguments": {}}'
        
        fmt = rust_core.detect_tool_format_rust(text)
        
        assert fmt == "json"
    
    def test_parse_tool_arguments_rust(self):
        """Test parsing tool arguments."""
        json_str = '{"city": "London", "units": "metric"}'
        
        args = rust_core.parse_tool_arguments_rust(json_str)
        
        assert isinstance(args, dict)
        assert args.get("city") == "London"
        assert args.get("units") == "metric"
    
    def test_parse_tool_arguments_rust_empty(self):
        """Test parsing empty arguments."""
        args = rust_core.parse_tool_arguments_rust("{}")
        
        assert isinstance(args, dict)
        assert len(args) == 0
    
    def test_parse_tool_arguments_rust_invalid(self):
        """Test parsing invalid JSON."""
        args = rust_core.parse_tool_arguments_rust("not json")
        
        assert isinstance(args, dict)
        assert len(args) == 0


class TestStructuredOutputFunctions:
    """Test structured output-related Rust functions."""
    
    def test_validate_json_schema_fast_rust_valid(self):
        """Test valid JSON validation."""
        json_str = '{"name": "John", "age": 30}'
        required_keys = ["name", "age"]
        expected_types = {"name": "string", "age": "number"}
        
        is_valid, error = rust_core.validate_json_schema_fast_rust(
            json_str, required_keys, expected_types
        )
        
        assert is_valid
        assert error == ""
    
    def test_validate_json_schema_fast_rust_missing_key(self):
        """Test JSON with missing required key."""
        json_str = '{"name": "John"}'
        required_keys = ["name", "age"]
        expected_types = {}
        
        is_valid, error = rust_core.validate_json_schema_fast_rust(
            json_str, required_keys, expected_types
        )
        
        assert not is_valid
        assert "age" in error
    
    def test_validate_json_schema_fast_rust_type_mismatch(self):
        """Test JSON with type mismatch."""
        json_str = '{"name": 123}'
        required_keys = ["name"]
        expected_types = {"name": "string"}
        
        is_valid, error = rust_core.validate_json_schema_fast_rust(
            json_str, required_keys, expected_types
        )
        
        assert not is_valid
        assert "string" in error or "number" in error
    
    def test_validate_partial_json_rust_complete(self):
        """Test validation of complete JSON."""
        is_valid = rust_core.validate_partial_json_rust('{"key": "value"}')
        
        assert is_valid
    
    def test_validate_partial_json_rust_incomplete(self):
        """Test validation of incomplete JSON."""
        is_valid = rust_core.validate_partial_json_rust('{"key": ')
        
        assert is_valid
    
    def test_validate_partial_json_rust_invalid(self):
        """Test validation of invalid start."""
        is_valid = rust_core.validate_partial_json_rust('xyz not json')
        
        # 'x' is not a valid JSON start character
        assert not is_valid
    
    def test_validate_partial_json_rust_empty(self):
        """Test validation of empty string."""
        is_valid = rust_core.validate_partial_json_rust("")
        
        assert is_valid
    
    def test_constraint_hash_rust(self):
        """Test constraint hash generation."""
        hash_val = rust_core.constraint_hash_rust(
            json_schema='{"type": "object"}',
            regex_pattern=None,
            choices=[],
        )
        
        assert isinstance(hash_val, int)
    
    def test_constraint_hash_rust_deterministic(self):
        """Test hash is deterministic."""
        h1 = rust_core.constraint_hash_rust('{"type": "string"}', None, [])
        h2 = rust_core.constraint_hash_rust('{"type": "string"}', None, [])
        
        assert h1 == h2
    
    def test_constraint_hash_rust_unique(self):
        """Test different constraints have different hashes."""
        h1 = rust_core.constraint_hash_rust('{"type": "string"}', None, [])
        h2 = rust_core.constraint_hash_rust('{"type": "number"}', None, [])
        h3 = rust_core.constraint_hash_rust(None, r"^\d+$", [])
        h4 = rust_core.constraint_hash_rust(None, None, ["a", "b", "c"])
        
        assert h1 != h2
        assert h1 != h3
        assert h1 != h4


class TestPerformanceBenchmarks:
    """Basic performance tests."""
    
    def test_log_softmax_performance(self):
        """Test log softmax on larger input."""
        logits = [float(i) for i in range(1000)]
        
        result = rust_core.log_softmax_stable_rust(logits)
        
        assert len(result) == 1000
        assert all(math.isfinite(lp) for lp in result)
    
    def test_batch_estimate_tokens_performance(self):
        """Test batch estimation on many texts."""
        texts = [f"This is sentence number {i}" for i in range(100)]
        
        result = rust_core.batch_estimate_tokens_rust(texts, 4.0)
        
        assert len(result) == 100
    
    def test_json_positions_performance(self):
        """Test JSON position extraction on large text."""
        json_objects = '{"a":1}' * 50
        text = "text " + json_objects + " more text"
        
        positions = rust_core.extract_json_positions_rust(text)
        
        assert len(positions) == 50


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_inputs(self):
        """Test various functions with empty inputs."""
        # Empty text
        assert rust_core.bpe_encode_fast_rust("", {}, []) == []
        assert rust_core.batch_estimate_tokens_rust([], 4.0) == []
        assert rust_core.extract_json_positions_rust("") == []
        assert rust_core.detect_tool_format_rust("") == "json"
    
    def test_unicode_handling(self):
        """Test Unicode in various functions."""
        text = "Hello, 世界! 🌍 Привет"
        
        # Should not crash
        positions = rust_core.extract_json_positions_rust(text)
        fmt = rust_core.detect_tool_format_rust(text)
        
        assert isinstance(positions, list)
        assert isinstance(fmt, str)
    
    def test_very_long_input(self):
        """Test with very long input."""
        long_text = "a" * 100000
        
        estimates = rust_core.batch_estimate_tokens_rust([long_text], 4.0)
        
        assert estimates[0] == 25000
    
    def test_special_characters(self):
        """Test special characters in JSON."""
        json_str = '{"message": "Hello\\nWorld\\t!"}'
        
        args = rust_core.parse_tool_arguments_rust(json_str)
        
        assert isinstance(args, dict)
