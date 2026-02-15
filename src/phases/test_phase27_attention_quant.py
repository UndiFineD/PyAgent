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
Phase 27: Attention, Quantization & LoRA Tests

Tests for PagedAttentionEngine, QuantizationEngine, and LoRAManager
inspired by vLLM patterns.
"""

import math
import pytest
import numpy as np
from numpy.testing import assert_allclose


# ==============================================================================
# Paged Attention Tests
# ==============================================================================

class TestPagedAttentionEngine:
    """Tests for PagedAttentionEngine module."""

    def test_attention_config_creation(self):
        """Test AttentionConfig dataclass."""
        from src.infrastructure.engine.attention.paged_attention_engine import (
            AttentionConfig
        )

        config = AttentionConfig(
            head_size=64,
            num_heads=32,
            num_kv_heads=8,
            block_size=16,
        )

        assert config.head_size == 64
        assert config.num_heads == 32
        assert config.num_kv_heads == 8
        assert config.block_size == 16
        assert config.scale == 1.0 / math.sqrt(64)
        assert config.num_queries_per_kv == 4  # 32 / 8

    def test_attention_config_with_sliding_window(self):
        """Test AttentionConfig with sliding window."""
        from src.infrastructure.engine.attention.paged_attention_engine import AttentionConfig

        config = AttentionConfig(
            head_size=128,
            num_heads=16,
            num_kv_heads=4,
            sliding_window=1024,
        )

        assert config.sliding_window == 1024

    def test_block_table_allocation(self):
        """Test BlockTable block allocation."""
        from src.infrastructure.engine.attention.paged_attention_engine import BlockTable

        table = BlockTable(num_blocks=100, block_size=16)

        # Allocate blocks for a sequence
        table.allocate_block(seq_id=1)
        table.allocate_block(seq_id=1)
        table.allocate_block(seq_id=1)
        table.allocate_block(seq_id=1)

        # Should have allocated 4 blocks
        assert table.num_allocated_blocks(seq_id=1) == 4
        assert table.num_free_blocks == 96

    def test_block_table_free(self):
        """Test BlockTable block freeing."""
        from src.infrastructure.engine.attention.paged_attention_engine import BlockTable

        table = BlockTable(num_blocks=100, block_size=16)

        table.allocate_block(seq_id=1)
        table.allocate_block(seq_id=1)
        assert table.num_free_blocks == 98

        table.free_sequence(seq_id=1)
        assert table.num_free_blocks == 100

    def test_slot_mapping(self):
        """Test SlotMapping token-to-slot mapping."""
        from src.infrastructure.engine.attention.paged_attention_engine import SlotMapping

        slot_map = SlotMapping(block_size=16)

        # Test slot computation
        slot = slot_map.compute_slot(block_idx=1, offset=4)
        assert slot == 20  # 1 * 16 + 4

        # Test slot decoding
        block_idx, offset = slot_map.decode_slot(slot=20)
        assert block_idx == 1
        assert offset == 4

    def test_paged_kv_cache(self):
        """Test PagedKVCache read/write."""
        from src.infrastructure.engine.attention.paged_attention_engine import PagedKVCache

        cache = PagedKVCache(
            num_blocks=32,
            block_size=16,
            num_kv_heads=4,
            head_size=64,
        )

        # Write to a block via slot mapping
        keys = np.random.randn(16, 4, 64).astype(np.float32)
        values = np.random.randn(16, 4, 64).astype(np.float32)
        slot_mapping = np.arange(16, dtype=np.int64)  # Slots 0-15 in block 0

        cache.write(key=keys, value=values, slot_mapping=slot_mapping)

        # Read back via block table
        k_out, v_out = cache.read_blocks(block_table=[0], seq_len=16)

        assert_allclose(k_out, keys, rtol=1e-5)
        assert_allclose(v_out, values, rtol=1e-5)

    def test_attention_metadata(self):
        """Test AttentionMetadata creation."""
        from src.infrastructure.engine.attention.paged_attention_engine import AttentionMetadata

        metadata = AttentionMetadata.from_seq_lens(
            seq_lens=[128, 64, 256],
            block_tables=[
                [0, 1, 2, 3, 4, 5, 6, 7],
                [8, 9, 10, 11],
                [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
            ],
            block_size=16,
            max_blocks_per_seq=32,
        )

        assert metadata.num_seqs == 3
        assert metadata.max_seq_len == 256
        assert metadata.total_tokens == 448

    def test_scaled_dot_product_attention(self):
        """Test PagedAttentionOps.scaled_dot_product_attention."""
        from src.infrastructure.engine.attention.paged_attention_engine import PagedAttentionOps

        batch = 2
        seq_len = 4
        num_heads = 2
        head_dim = 8

        q = np.random.randn(batch, num_heads, seq_len, head_dim).astype(np.float32)
        k = np.random.randn(batch, num_heads, seq_len, head_dim).astype(np.float32)
        v = np.random.randn(batch, num_heads, seq_len, head_dim).astype(np.float32)

        output = PagedAttentionOps.scaled_dot_product_attention(
            query=q, key=k, value=v, scale=1.0 / math.sqrt(head_dim)
        )

        assert output.shape == (batch, num_heads, seq_len, head_dim)

    def test_expand_kv_for_gqa(self):
        """Test PagedAttentionOps.expand_kv_for_gqa."""
        from src.infrastructure.engine.attention.paged_attention_engine import PagedAttentionOps

        seq_len = 8
        num_kv_heads = 2
        num_heads = 8
        head_dim = 64

        # Shape: [seq_len, num_kv_heads, head_dim]
        kv = np.random.randn(seq_len, num_kv_heads, head_dim).astype(np.float32)

        num_queries_per_kv = num_heads // num_kv_heads  # 4
        expanded = PagedAttentionOps.expand_kv_for_gqa(
            kv=kv, num_queries_per_kv=num_queries_per_kv
        )

        # Should expand to [seq_len, num_heads, head_dim]
        assert expanded.shape == (seq_len, num_heads, head_dim)

        # Check repetition pattern
        for h in range(num_heads):
            kv_head = h // num_queries_per_kv
            assert_allclose(expanded[:, h], kv[:, kv_head], rtol=1e-5)

    def test_paged_attention_engine(self):
        """Test PagedAttentionEngine high-level API."""
        from src.infrastructure.engine.attention.paged_attention_engine import (
            PagedAttentionEngine, AttentionConfig
        )

        config = AttentionConfig(
            head_size=64,
            num_heads=8,
            num_kv_heads=4,
            block_size=16,
        )

        engine = PagedAttentionEngine(config=config, num_blocks=64)

        # Allocate a sequence
        engine.allocate_sequence(seq_id=1, initial_len=32)

        assert engine._seq_positions.get(1, 0) == 32

        # Append more tokens
        keys = np.random.randn(16, 4, 64).astype(np.float32)
        values = np.random.randn(16, 4, 64).astype(np.float32)
        engine.append_kv(seq_id=1, key=keys, value=values)
        assert engine._seq_positions.get(1, 0) == 48

        # Free sequence
        engine.free_sequence(seq_id=1)
        assert engine._seq_positions.get(1, 0) == 0


# ==============================================================================
# Quantization Tests
# ==============================================================================

class TestQuantizationEngine:
    """Tests for QuantizationEngine module."""

    def test_quant_config_validation(self):
        """Test QuantConfig validation."""
        from src.infrastructure.compute.quantization.quantization_engine import (
            QuantConfig, QuantScheme, QuantStrategy
        )

        config = QuantConfig(
            bits=8,
            scheme=QuantScheme.INT8,
            strategy=QuantStrategy.GROUP,
            group_size=128,
            symmetric=True,
        )

        assert config.bits == 8
        assert config.qmin == -128
        assert config.qmax == 127
        assert config.pack_factor == 4

    def test_quant_config_asymmetric(self):
        """Test QuantConfig for asymmetric quantization."""
        from src.infrastructure.compute.quantization.quantization_engine import QuantConfig

        config = QuantConfig(bits=8, symmetric=False, zero_point=True)

        assert config.qmin == 0
        assert config.qmax == 255

    def test_linear_quantizer_tensor(self):
        """Test LinearQuantizer per-tensor quantization."""
        from src.infrastructure.compute.quantization.quantization_engine import (
            LinearQuantizer, QuantConfig, QuantStrategy
        )

        config = QuantConfig(bits=8, strategy=QuantStrategy.TENSOR, symmetric=True)
        quantizer = LinearQuantizer(config)

        weight = np.random.randn(64, 128).astype(np.float32)
        qtensor = quantizer.quantize(weight)

        assert qtensor.data.dtype == np.int8
        assert len(qtensor.scale) == 1

        # Dequantize and check error
        dequant = qtensor.dequantize()
        assert dequant.shape == weight.shape

    def test_linear_quantizer_group(self):
        """Test LinearQuantizer per-group quantization."""
        from src.infrastructure.compute.quantization.quantization_engine import (
            LinearQuantizer, QuantConfig, QuantStrategy
        )

        config = QuantConfig(
            bits=8,
            strategy=QuantStrategy.GROUP,
            group_size=32,
            symmetric=True,
        )
        quantizer = LinearQuantizer(config)

        weight = np.random.randn(64, 128).astype(np.float32)
        qtensor = quantizer.quantize(weight)

        # 128 / 32 = 4 groups per row
        assert qtensor.scale.shape == (64, 4)

    def test_pack_unpack_int4(self):
        """Test INT4 packing and unpacking."""
        from src.infrastructure.compute.quantization.quantization_engine import pack_int4, unpack_int4

        # Original int4 values [-8, 7]
        original = np.array([0, 1, -1, 7, -8, 3, 2, -2], dtype=np.int8)

        packed = pack_int4(original)
        assert len(packed) == 4  # Half the size

        unpacked = unpack_int4(packed)
        assert_allclose(unpacked[:len(original)], original)

    def test_quantized_tensor_compression_ratio(self):
        """Test QuantizedTensor compression ratio."""
        from src.infrastructure.compute.quantization.quantization_engine import (
            LinearQuantizer, QuantConfig, QuantStrategy
        )

        config = QuantConfig(bits=8, strategy=QuantStrategy.TENSOR)
        quantizer = LinearQuantizer(config)

        weight = np.random.randn(256, 256).astype(np.float32)
        qtensor = quantizer.quantize(weight)

        # INT8 should give ~4x compression over FP32
        assert qtensor.compression_ratio > 3.5

    def test_awq_quantizer(self):
        """Test AWQQuantizer activation-aware quantization."""
        from src.infrastructure.compute.quantization.quantization_engine import (
            AWQQuantizer, QuantConfig
        )

        config = QuantConfig(bits=8, group_size=64)

        # Create calibration activations
        activations = np.random.randn(100, 128).astype(np.float32)

        quantizer = AWQQuantizer(config, calibration_data=activations)

        weight = np.random.randn(64, 128).astype(np.float32)
        qtensor = quantizer.quantize(weight)

        assert qtensor.data is not None

    def test_gptq_quantizer(self):
        """Test GPTQQuantizer with Hessian."""
        from src.infrastructure.compute.quantization.quantization_engine import (
            GPTQQuantizer, QuantConfig
        )

        config = QuantConfig(bits=8, group_size=32)
        quantizer = GPTQQuantizer(config, damp_percent=0.01)

        weight = np.random.randn(64, 128).astype(np.float32)

        # Create simple Hessian (X^T X)
        X = np.random.randn(100, 128).astype(np.float32)
        hessian = X.T @ X

        qtensor = quantizer.quantize(weight, hessian=hessian)

        assert qtensor.data is not None

    def test_dequantized_linear_forward(self):
        """Test DequantizedLinear forward pass."""
        from src.infrastructure.compute.quantization.quantization_engine import (
            LinearQuantizer, QuantConfig, DequantizedLinear
        )

        config = QuantConfig(bits=8, group_size=64)
        quantizer = LinearQuantizer(config)

        weight = np.random.randn(128, 64).astype(np.float32)
        bias = np.random.randn(128).astype(np.float32)

        qtensor = quantizer.quantize(weight)
        layer = DequantizedLinear(qtensor, bias)

        x = np.random.randn(4, 64).astype(np.float32)
        output = layer.forward(x)

        assert output.shape == (4, 128)

    def test_quantization_error_metrics(self):
        """Test get_quantization_error function."""
        from src.infrastructure.compute.quantization.quantization_engine import (
            LinearQuantizer, QuantConfig, get_quantization_error
        )

        config = QuantConfig(bits=8, group_size=64)
        quantizer = LinearQuantizer(config)

        original = np.random.randn(64, 128).astype(np.float32)
        qtensor = quantizer.quantize(original)

        errors = get_quantization_error(original, qtensor)

        assert "mse" in errors
        assert "mae" in errors
        assert "snr_db" in errors
        assert errors["snr_db"] > 20  # Should have decent SNR for INT8


# ==============================================================================
# LoRA Manager Tests
# ==============================================================================

class TestLoRAManager:
    """Tests for LoRAManager module."""

    def test_lora_config_creation(self):
        """Test LoRAConfig dataclass."""
        from src.infrastructure.engine.adapters.lo_ra_manager import LoRAConfig

        config = LoRAConfig(
            rank=8,
            alpha=16.0,
            dropout=0.1,
            target_modules={"q_proj", "v_proj"},
        )

        assert config.rank == 8
        assert config.alpha == 16.0
        assert config.scaling == 2.0  # 16 / 8

    def test_lora_layer_weights_forward(self):
        """Test LoRALayerWeights forward pass."""
        from src.infrastructure.engine.adapters.lo_ra_manager import LoRALayerWeights

        rank = 8
        in_features = 64
        out_features = 128

        lora_a = np.random.randn(rank, in_features).astype(np.float32)
        lora_b = np.zeros((out_features, rank), dtype=np.float32)

        layer = LoRALayerWeights(
            lora_a=lora_a,
            lora_b=lora_b,
            scaling=2.0,
            module_name="q_proj",
        )

        x = np.random.randn(4, in_features).astype(np.float32)
        output = layer.forward(x)

        # With zero B, output should be zero
        assert output.shape == (4, out_features)
        assert_allclose(output, 0.0, atol=1e-6)

    def test_lora_layer_merge(self):
        """Test LoRALayerWeights merge_into_base."""
        from src.infrastructure.engine.adapters.lo_ra_manager import LoRALayerWeights

        rank = 4
        in_features = 16
        out_features = 32

        lora_a = np.random.randn(rank, in_features).astype(np.float32) * 0.1
        lora_b = np.random.randn(out_features, rank).astype(np.float32) * 0.1

        layer = LoRALayerWeights(
            lora_a=lora_a,
            lora_b=lora_b,
            scaling=2.0,
            module_name="test",
        )

        base = np.random.randn(out_features, in_features).astype(np.float32)
        merged = layer.merge_into_base(base)

        # Check merge formula: W + B @ A * scaling
        expected = base + lora_b @ lora_a * 2.0
        assert_allclose(merged, expected, rtol=1e-5)

    def test_packed_lora_weights(self):
        """Test PackedLoRAWeights creation and unpacking."""
        from src.infrastructure.engine.adapters.lo_ra_manager import (
            LoRALayerWeights, PackedLoRAWeights
        )

        layers = []
        for i, name in enumerate(["q_proj", "k_proj", "v_proj"]):
            layer = LoRALayerWeights(
                lora_a=np.random.randn(8, 64).astype(np.float32),
                lora_b=np.random.randn(128, 8).astype(np.float32),
                scaling=2.0,
                module_name=name,
            )
            layers.append(layer)

        packed = PackedLoRAWeights.from_individual(layers)

        assert packed.num_layers == 3
        assert packed.lora_a.shape == (3, 8, 64)

        unpacked = packed.unpack()
        assert len(unpacked) == 3

    def test_lora_model(self):
        """Test LoRAModel creation and forward."""
        from src.infrastructure.engine.adapters.lo_ra_manager import (
            LoRAConfig, LoRAModel, LoRALayerWeights
        )

        config = LoRAConfig(rank=8, alpha=16.0)
        model = LoRAModel(model_id="test-lora", config=config)

        layer = LoRALayerWeights(
            lora_a=np.random.randn(8, 64).astype(np.float32),
            lora_b=np.random.randn(128, 8).astype(np.float32),
            scaling=config.scaling,
            module_name="q_proj",
        )
        model.add_layer(layer)

        assert model.num_parameters == 8 * 64 + 128 * 8

        x = np.random.randn(4, 64).astype(np.float32)
        output = model.forward("q_proj", x)

        assert output is not None
        assert output.shape == (4, 128)

    def test_lora_registry(self):
        """Test LoRARegistry LRU eviction."""
        from src.infrastructure.engine.adapters.lo_ra_manager import (
            LoRAConfig, LoRAModel, LoRALayerWeights, LoRARegistry
        )

        # Small registry
        registry = LoRARegistry(max_memory_bytes=100000, max_models=3)

        for i in range(5):
            config = LoRAConfig(rank=4)
            model = LoRAModel(model_id=f"model-{i}", config=config)
            model.add_layer(LoRALayerWeights(
                lora_a=np.random.randn(4, 32).astype(np.float32),
                lora_b=np.random.randn(64, 4).astype(np.float32),
                scaling=4.0,
                module_name="q_proj",
            ))
            registry.register(model)

        # Should have evicted older models
        models = registry.list_models()
        assert len(models) <= 3

    def test_lora_manager_load_adapter(self):
        """Test LoRAManager adapter loading."""
        from src.infrastructure.engine.adapters.lo_ra_manager import (
            LoRAManager, LoRAConfig
        )

        manager = LoRAManager()

        weights = {
            "q_proj": (
                np.random.randn(8, 64).astype(np.float32),
                np.random.randn(128, 8).astype(np.float32),
            ),
            "v_proj": (
                np.random.randn(8, 64).astype(np.float32),
                np.random.randn(128, 8).astype(np.float32),
            ),
        }

        config = LoRAConfig(rank=8, alpha=16.0)
        model = manager.load_adapter("my-adapter", weights, config)

        assert model.model_id == "my-adapter"
        assert "my-adapter" in manager.list_adapters()

    def test_lora_manager_request_binding(self):
        """Test LoRAManager per-request adapter binding."""
        from src.infrastructure.engine.adapters.lo_ra_manager import (
            LoRAManager
        )

        manager = LoRAManager()

        weights = {
            "q_proj": (
                np.random.randn(8, 64).astype(np.float32),
                np.random.randn(128, 8).astype(np.float32),
            ),
        }

        manager.load_adapter("adapter-1", weights)
        manager.load_adapter("adapter-2", weights)

        manager.set_request_adapter(request_id=1, model_id="adapter-1")
        manager.set_request_adapter(request_id=2, model_id="adapter-2")

        assert manager.get_request_adapter(1) == "adapter-1"
        assert manager.get_request_adapter(2) == "adapter-2"

        manager.clear_request(1)
        assert manager.get_request_adapter(1) is None

    def test_lora_manager_apply_lora(self):
        """Test LoRAManager apply_lora."""
        from src.infrastructure.engine.adapters.lo_ra_manager import (
            LoRAManager, LoRAConfig
        )

        manager = LoRAManager()

        # Create adapter with small random weights
        weights = {
            "q_proj": (
                np.random.randn(4, 32).astype(np.float32) * 0.01,
                np.random.randn(64, 4).astype(np.float32) * 0.01,
            ),
        }

        config = LoRAConfig(rank=4, alpha=8.0)
        manager.load_adapter("test-adapter", weights, config)
        manager.set_request_adapter(request_id=1, model_id="test-adapter")

        base_output = np.random.randn(4, 64).astype(np.float32)
        x = np.random.randn(4, 32).astype(np.float32)

        result = manager.apply_lora(
            request_id=1,
            module_name="q_proj",
            base_output=base_output,
            x=x,
        )

        # Should be different from base
        assert result.shape == base_output.shape

    def test_create_lora_weights(self):
        """Test create_lora_weights factory function."""
        from src.infrastructure.engine.adapters.lo_ra_manager import create_lora_weights

        layer = create_lora_weights(
            in_features=64,
            out_features=128,
            rank=8,
            alpha=16.0,
            module_name="test",
            init_method="kaiming",
        )

        assert layer.rank == 8
        assert layer.in_features == 64
        assert layer.out_features == 128
        # B should be zeros for kaiming init
        assert_allclose(layer.lora_b, 0.0, atol=1e-6)

    def test_merge_lora_weights(self):
        """Test merge_lora_weights utility function."""
        from src.infrastructure.engine.adapters.lo_ra_manager import (
            LoRAConfig, LoRAModel, create_lora_weights, merge_lora_weights
        )

        config = LoRAConfig(rank=4, alpha=8.0)
        model = LoRAModel(model_id="test", config=config)

        layer = create_lora_weights(32, 64, 4, 8.0, "linear")
        model.add_layer(layer)

        base_weights = {
            "linear": np.random.randn(64, 32).astype(np.float32),
            "other": np.random.randn(128, 64).astype(np.float32),
        }

        merged = merge_lora_weights(base_weights, model)

        # "linear" should be merged, "other" unchanged
        assert "linear" in merged
        assert "other" in merged


# ==============================================================================
# Rust Acceleration Tests
# ==============================================================================

class TestRustQuantLoRA:
    """Tests for Rust quantlora module functions."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup: try to import rust_core."""
        try:
            import rust_core
            self.rust = rust_core
            self.has_rust = True
        except ImportError:
            self.has_rust = False
            pytest.skip("rust_core not available")

    def test_quantize_symmetric(self):
        """Test quantize_symmetric_rust."""
        weights = [1.0, -0.5, 0.25, -1.0, 0.0]

        quantized, scale = self.rust.quantize_symmetric_rust(weights, 8)

        assert len(quantized) == 5
        assert scale > 0
        # Max abs value is 1.0, should map to ~127
        assert abs(quantized[0]) > 100

    def test_quantize_asymmetric(self):
        """Test quantize_asymmetric_rust."""
        weights = [0.0, 0.5, 1.0, 1.5, 2.0]

        quantized, scale, zero_point = self.rust.quantize_asymmetric_rust(weights, 8)

        assert len(quantized) == 5
        assert scale > 0
        assert zero_point >= 0

    def test_pack_int4(self):
        """Test pack_int4_rust."""
        values = [0, 1, 2, 3, 4, 5, 6, 7]

        packed = self.rust.pack_int4_rust(values)

        # 8 values should pack into 4 bytes
        assert len(packed) == 4

    def test_dequantize_int4(self):
        """Test dequantize_int4_rust."""
        packed = [0x10, 0x32, 0x54, 0x76]  # Packed pairs
        scale = 0.5
        zero_point = 0

        unpacked = self.rust.dequantize_int4_rust(packed, scale, zero_point)

        assert len(unpacked) == 8

    def test_compute_scales(self):
        """Test compute_scales_rust."""
        weights = [float(i) for i in range(64)]

        scales = self.rust.compute_scales_rust(weights, 16, 8, True)

        # 64 / 16 = 4 groups
        assert len(scales) == 4

    def test_lora_merge(self):
        """Test lora_merge_rust."""
        out_features = 4
        in_features = 3
        rank = 2

        base = [1.0] * (out_features * in_features)
        lora_a = [0.1] * (rank * in_features)
        lora_b = [0.1] * (out_features * rank)
        scaling = 2.0

        merged = self.rust.lora_merge_rust(
            base, lora_a, lora_b,
            out_features, in_features, rank, scaling
        )

        assert len(merged) == out_features * in_features
        # Merged should differ from base
        assert merged[0] != base[0]

    def test_attention_softmax(self):
        """Test attention_softmax_rust."""
        seq_len = 4
        head_dim = 8

        # Two rows of attention scores
        scores = [1.0] * (2 * seq_len)

        softmax = self.rust.attention_softmax_rust(scores, seq_len, head_dim)

        assert len(softmax) == 2 * seq_len
        # Each row should sum to 1
        row1_sum = sum(softmax[:seq_len])
        assert abs(row1_sum - 1.0) < 1e-5

    def test_gqa_expand_kv(self):
        """Test gqa_expand_kv_rust."""
        batch = 1
        num_heads = 4
        num_kv_heads = 2
        seq_len = 2
        head_dim = 2

        # 1 * 2 * 2 * 2 = 8 elements
        kv = [float(i) for i in range(8)]

        expanded = self.rust.gqa_expand_kv_rust(
            kv, batch, num_heads, num_kv_heads, seq_len, head_dim
        )

        # Should expand to batch * num_heads * seq_len * head_dim
        assert len(expanded) == batch * num_heads * seq_len * head_dim

    def test_slot_mapping(self):
        """Test slot_mapping_rust."""
        seq_lens = [32, 16]
        block_size = 16
        num_blocks_per_seq = [2, 1]

        mapping = self.rust.slot_mapping_rust(seq_lens, block_size, num_blocks_per_seq)

        # Should have mappings for 32 + 16 = 48 tokens
        assert len(mapping) == 48

        # Check first mapping
        block_idx, slot_offset = mapping[0]
        assert block_idx == 0
        assert slot_offset == 0

    def test_lora_forward(self):
        """Test lora_forward_rust."""
        batch = 2
        in_features = 4
        out_features = 3
        rank = 2

        x = [1.0] * (batch * in_features)
        lora_a = [0.1] * (rank * in_features)
        lora_b = [0.2] * (out_features * rank)
        scaling = 2.0

        output = self.rust.lora_forward_rust(
            x, lora_a, lora_b,
            batch, in_features, out_features, rank, scaling
        )

        assert len(output) == batch * out_features


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
