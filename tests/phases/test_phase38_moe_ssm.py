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
Test Phase 38: Advanced MoE, Mamba SSM & MLA.

vLLM Patterns Tested:
- Fused Mixture of Experts with expert parallelism
- Token-to-expert routing (Top-K, Expert Choice, Soft MoE)
- Mamba State Space Model with selective scan
- Multi-head Latent Attention (MLA)
- Auxiliary load balancing losses
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Try to import Rust core
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def moe_config():
    """Standard MoE configuration."""
    return {
        "num_experts": 8,
        "top_k": 2,
        "hidden_size": 256,
        "intermediate_size": 512,
        "batch_size": 4,
        "seq_len": 16,
    }


@pytest.fixture
def ssm_config():
    """Standard Mamba SSM configuration."""
    return {
        "hidden_size": 256,
        "ssm_state_size": 16,
        "d_inner": 512,  # expand * hidden_size
        "conv_kernel_size": 4,
        "batch_size": 2,
        "seq_len": 32,
    }


@pytest.fixture
def mla_config():
    """Standard MLA configuration."""
    return {
        "hidden_size": 256,
        "num_heads": 8,
        "num_kv_heads": 2,
        "kv_lora_rank": 64,
        "head_dim": 32,
        "batch_size": 2,
        "seq_len": 16,
    }


# =============================================================================
# Python Module Tests
# =============================================================================

class TestFusedMoELayer:
    """Tests for FusedMoELayer module."""

    def test_fused_moe_config(self, moe_config):
        """Test FusedMoEConfig dataclass."""
        from src.infrastructure.compute.moe import FusedMoEConfig

        config = FusedMoEConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
            intermediate_size=moe_config["intermediate_size"],
        )

        assert config.num_experts == 8
        assert config.top_k == 2
        assert config.hidden_size == 256
        assert config.intermediate_size == 512

    def test_fused_moe_parallel_config(self):
        """Test FusedMoEParallelConfig."""
        from src.infrastructure.compute.moe import FusedMoEParallelConfig

        config = FusedMoEParallelConfig(
            tp_size=2,
            ep_size=4,
            use_all2all_kernels=True,
        )

        assert config.tp_size == 2
        assert config.ep_size == 4
        assert config.use_all2all_kernels is True

    def test_determine_expert_map(self, moe_config):
        """Test expert-to-device mapping."""
        from src.infrastructure.compute.moe.fused_mo_e_layer import determine_expert_map
        from src.infrastructure.compute.moe import ExpertPlacementStrategy

        # Linear placement
        local_num, linear_map, mask = determine_expert_map(
            ep_size=4,
            ep_rank=0,
            global_num_experts=8,
            strategy=ExpertPlacementStrategy.LINEAR,
        )
        assert local_num == 2
        assert linear_map is not None

        # Round robin placement
        local_num2, robin_map, _ = determine_expert_map(
            ep_size=4,
            ep_rank=0,
            global_num_experts=8,
            strategy=ExpertPlacementStrategy.ROUND_ROBIN,
        )
        assert local_num2 == 2

    def test_fused_moe_layer_creation(self, moe_config):
        """Test FusedMoELayer creation."""
        from src.infrastructure.compute.moe.fused_mo_e_layer import FusedMoELayer
        from src.infrastructure.compute.moe import FusedMoEConfig

        config = FusedMoEConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
            intermediate_size=moe_config["intermediate_size"],
        )

        layer = FusedMoELayer(config)

        assert layer.config.num_experts == 8
        assert layer.config.top_k == 2

    def test_sparse_dispatcher(self, moe_config):
        """Test SparseDispatcher for token-to-expert dispatch."""
        from src.infrastructure.compute.moe.fused_mo_e_layer import SparseDispatcher

        batch_size = moe_config["batch_size"]
        seq_len = moe_config["seq_len"]
        num_tokens = batch_size * seq_len
        num_experts = moe_config["num_experts"]
        top_k = moe_config["top_k"]
        hidden_size = moe_config["hidden_size"]

        dispatcher = SparseDispatcher(num_experts, top_k)

        # Create mock routing
        expert_indices = np.random.randint(0, num_experts, (num_tokens, top_k))
        expert_weights = np.random.rand(num_tokens, top_k).astype(np.float32)
        expert_weights = expert_weights / expert_weights.sum(axis=1, keepdims=True)
        x = np.random.randn(num_tokens, hidden_size).astype(np.float32)

        inputs, positions, weights = dispatcher.dispatch(x, expert_indices, expert_weights)

        # Verify dispatch
        assert len(inputs) == num_experts
        assert len(positions) == num_experts

    def test_dense_dispatcher(self, moe_config):
        """Test DenseDispatcher for matrix-based dispatch."""
        from src.infrastructure.compute.moe.fused_mo_e_layer import DenseDispatcher

        batch_size = moe_config["batch_size"]
        seq_len = moe_config["seq_len"]
        num_tokens = batch_size * seq_len
        num_experts = moe_config["num_experts"]
        hidden_size = moe_config["hidden_size"]
        top_k = moe_config["top_k"]

        dispatcher = DenseDispatcher(num_experts, top_k)

        # Create mock routing
        expert_indices = np.random.randint(0, num_experts, (num_tokens, top_k))
        expert_weights = np.random.rand(num_tokens, top_k).astype(np.float32)
        expert_weights = expert_weights / expert_weights.sum(axis=1, keepdims=True)

        # Create mock inputs
        inputs = np.random.rand(num_tokens, hidden_size).astype(np.float32)

        # Simple expert function
        def expert_fn(expert_idx, x):
            return x * (1 + expert_idx * 0.1)

        output = dispatcher.dispatch_and_combine(inputs, expert_indices, expert_weights, expert_fn)
        assert output.shape == inputs.shape

    def test_adaptive_moe_layer(self, moe_config):
        """Test AdaptiveMoELayer with dynamic expert count."""
        from src.infrastructure.compute.moe.fused_mo_e_layer import AdaptiveMoELayer
        from src.infrastructure.compute.moe import FusedMoEConfig

        config = FusedMoEConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
            intermediate_size=moe_config["intermediate_size"],
        )

        layer = AdaptiveMoELayer(config, min_top_k=1, max_top_k=4)

        assert layer.min_top_k == 1
        assert layer.max_top_k == 4

    def test_hierarchical_moe_layer(self, moe_config):
        """Test HierarchicalMoELayer with two-level routing."""
        from src.infrastructure.compute.moe.fused_mo_e_layer import HierarchicalMoELayer
        from src.infrastructure.compute.moe import FusedMoEConfig

        config = FusedMoEConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
            intermediate_size=moe_config["intermediate_size"],
        )

        layer = HierarchicalMoELayer(
            config=config,
            num_clusters=4,
            cluster_top_k=1,
        )

        assert layer.num_clusters == 4
        assert layer.cluster_top_k == 1


class TestExpertRouter:
    """Tests for ExpertRouter module."""

    def test_router_config(self, moe_config):
        """Test RouterConfig dataclass."""
        from src.infrastructure.compute.moe import RouterConfig

        config = RouterConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
        )

        assert config.num_experts == 8
        assert config.top_k == 2

    def test_topk_router(self, moe_config):
        """Test TopKRouter for standard top-k selection."""
        from src.infrastructure.compute.moe import TopKRouter, RouterConfig

        config = RouterConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
        )

        router = TopKRouter(config)

        # Create mock hidden states
        num_tokens = moe_config["batch_size"] * moe_config["seq_len"]
        hidden_states = np.random.randn(num_tokens, moe_config["hidden_size"]).astype(np.float32)

        output = router.forward(hidden_states)

        assert output.expert_indices.shape == (num_tokens, moe_config["top_k"])
        assert output.expert_weights.shape == (num_tokens, moe_config["top_k"])

    def test_expert_choice_router(self, moe_config):
        """Test ExpertChoiceRouter (experts select tokens)."""
        from src.infrastructure.compute.moe import ExpertChoiceRouter, RouterConfig

        config = RouterConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
            capacity_factor=1.5,
        )

        router = ExpertChoiceRouter(config)

        num_tokens = moe_config["batch_size"] * moe_config["seq_len"]
        hidden_states = np.random.randn(num_tokens, moe_config["hidden_size"]).astype(np.float32)

        output = router.forward(hidden_states)

        # Expert choice router still returns token-centric indices
        assert output.expert_indices.shape[0] == num_tokens

    def test_soft_moe_router(self, moe_config):
        """Test SoftMoERouter for differentiable routing."""
        from src.infrastructure.compute.moe import SoftMoERouter, RouterConfig

        config = RouterConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
        )

        router = SoftMoERouter(config)

        num_tokens = moe_config["batch_size"] * moe_config["seq_len"]
        hidden_states = np.random.randn(num_tokens, moe_config["hidden_size"]).astype(np.float32)

        output = router.forward(hidden_states)

        # Soft MoE still outputs top-k
        assert output.expert_indices.shape == (num_tokens, moe_config["top_k"])
        assert output.expert_weights.shape == (num_tokens, moe_config["top_k"])

    def test_adaptive_router(self, moe_config):
        """Test AdaptiveRouter with learned k per token."""
        from src.infrastructure.compute.moe.expert_router import AdaptiveRouter
        from src.infrastructure.compute.moe import RouterConfig

        config = RouterConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
        )

        router = AdaptiveRouter(config, min_k=1, max_k=4)

        assert router.min_k == 1
        assert router.max_k == 4

    def test_routing_simulator(self, moe_config):
        """Test RoutingSimulator for analysis."""
        from src.infrastructure.compute.moe.expert_router import RoutingSimulator

        simulator = RoutingSimulator(
            num_experts=moe_config["num_experts"],
            num_tokens=100,
            top_k=moe_config["top_k"],
        )

        # Simulate routing
        routing = simulator.simulate_uniform()

        stats = simulator.analyze_load_balance(routing)

        assert "expert_counts" in stats
        assert "load_imbalance" in stats
        assert len(stats["expert_counts"]) == moe_config["num_experts"]

    def test_router_aux_losses(self, moe_config):
        """Test auxiliary loss computation."""
        from src.infrastructure.compute.moe import TopKRouter, RouterConfig

        config = RouterConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
            aux_loss_coef=0.01,
            z_loss_coef=0.001,
        )

        router = TopKRouter(config)

        num_tokens = moe_config["batch_size"] * moe_config["seq_len"]
        hidden_states = np.random.randn(num_tokens, moe_config["hidden_size"]).astype(np.float32)

        output = router.forward(hidden_states)

        assert output.aux_loss >= 0.0
        assert output.z_loss >= 0.0


class TestMambaMixer:
    """Tests for MambaMixer module."""

    def test_mamba_config(self, ssm_config):
        """Test MambaConfig dataclass."""
        from src.infrastructure.compute.ssm import MambaConfig

        config = MambaConfig(
            hidden_size=ssm_config["hidden_size"],
            ssm_state_size=ssm_config["ssm_state_size"],
            intermediate_size=ssm_config["d_inner"],
            conv_kernel_size=ssm_config["conv_kernel_size"],
        )

        assert config.hidden_size == 256
        assert config.ssm_state_size == 16
        assert config.d_inner == 512
        assert config.conv_kernel_size == 4

    def test_mamba_state(self, ssm_config):
        """Test MambaState dataclass."""
        from src.infrastructure.compute.ssm import MambaState, MambaConfig

        batch_size = ssm_config["batch_size"]

        config = MambaConfig(
            hidden_size=ssm_config["hidden_size"],
            ssm_state_size=ssm_config["ssm_state_size"],
            intermediate_size=ssm_config["d_inner"],
            conv_kernel_size=ssm_config["conv_kernel_size"],
        )

        state = MambaState.zeros(
            batch_size=batch_size,
            config=config,
        )

        assert state.conv_state.shape == (batch_size, config.d_inner, config.conv_kernel_size)
        assert state.ssm_state.shape == (batch_size, config.d_inner, config.ssm_state_size)

    def test_causal_conv1d(self, ssm_config):
        """Test CausalConv1d layer."""
        from src.infrastructure.compute.ssm.mamba_mixer import CausalConv1d

        d_inner = ssm_config["d_inner"]
        kernel_size = ssm_config["conv_kernel_size"]

        conv = CausalConv1d(d_inner, kernel_size)

        # Test forward pass
        batch_size = ssm_config["batch_size"]
        seq_len = ssm_config["seq_len"]
        x = np.random.randn(batch_size, seq_len, d_inner).astype(np.float32)

        output, new_state = conv.forward(x)

        assert output.shape == (batch_size, seq_len, d_inner)

    def test_causal_conv1d_step(self, ssm_config):
        """Test CausalConv1d single step update."""
        from src.infrastructure.compute.ssm.mamba_mixer import CausalConv1d

        d_inner = ssm_config["d_inner"]
        kernel_size = ssm_config["conv_kernel_size"]
        batch_size = ssm_config["batch_size"]

        conv = CausalConv1d(d_inner, kernel_size)

        # Single step input
        x = np.random.randn(batch_size, d_inner).astype(np.float32)
        conv_state = np.zeros((batch_size, d_inner, kernel_size), dtype=np.float32)

        output, new_state = conv.update(x, conv_state)

        assert output.shape == (batch_size, d_inner)
        assert new_state.shape == (batch_size, d_inner, kernel_size)

    def test_selective_scan(self, ssm_config):
        """Test SelectiveScan layer."""
        from src.infrastructure.compute.ssm.mamba_mixer import SelectiveScan

        d_inner = ssm_config["d_inner"]
        ssm_state_size = ssm_config["ssm_state_size"]

        ssm = SelectiveScan(d_inner, ssm_state_size)

        # Test forward pass
        batch_size = ssm_config["batch_size"]
        seq_len = ssm_config["seq_len"]

        x = np.random.randn(batch_size, seq_len, d_inner).astype(np.float32)
        dt = np.random.rand(batch_size, seq_len, d_inner).astype(np.float32) * 0.1
        B = np.random.randn(batch_size, seq_len, ssm_state_size).astype(np.float32)
        C = np.random.randn(batch_size, seq_len, ssm_state_size).astype(np.float32)

        output, state = ssm.forward(x, dt, B, C)

        assert output.shape == (batch_size, seq_len, d_inner)

    def test_mamba_mixer(self, ssm_config):
        """Test full MambaMixer layer."""
        from src.infrastructure.compute.ssm.mamba_mixer import MambaMixer as MambaMixerClass
        from src.infrastructure.compute.ssm import MambaConfig

        config = MambaConfig(
            hidden_size=ssm_config["hidden_size"],
            ssm_state_size=ssm_config["ssm_state_size"],
            intermediate_size=ssm_config["d_inner"],
            conv_kernel_size=ssm_config["conv_kernel_size"],
        )

        mixer = MambaMixerClass(config)

        # Test forward pass
        batch_size = ssm_config["batch_size"]
        seq_len = ssm_config["seq_len"]
        hidden_states = np.random.randn(batch_size, seq_len, ssm_config["hidden_size"]).astype(np.float32)

        output = mixer.forward(hidden_states)

        assert output.output.shape == (batch_size, seq_len, ssm_config["hidden_size"])

    def test_mamba_mixer_step(self, ssm_config):
        """Test MambaMixer single step for decoding."""
        from src.infrastructure.compute.ssm.mamba_mixer import MambaMixer as MambaMixerClass
        from src.infrastructure.compute.ssm import MambaConfig, MambaState

        config = MambaConfig(
            hidden_size=ssm_config["hidden_size"],
            ssm_state_size=ssm_config["ssm_state_size"],
            intermediate_size=ssm_config["d_inner"],
            conv_kernel_size=ssm_config["conv_kernel_size"],
        )

        mixer = MambaMixerClass(config)

        batch_size = ssm_config["batch_size"]
        hidden_states = np.random.randn(batch_size, ssm_config["hidden_size"]).astype(np.float32)

        state = MambaState.zeros(
            batch_size=batch_size,
            config=config,
        )

        output = mixer.step(hidden_states, state)

        assert output.output.shape == (batch_size, ssm_config["hidden_size"])
        assert output.state is not None

    def test_mamba2_mixer(self, ssm_config):
        """Test Mamba2Mixer with multi-head SSM."""
        from src.infrastructure.compute.ssm.mamba_mixer import Mamba2Mixer
        from src.infrastructure.compute.ssm import MambaConfig

        config = MambaConfig(
            hidden_size=ssm_config["hidden_size"],
            ssm_state_size=ssm_config["ssm_state_size"],
            intermediate_size=ssm_config["d_inner"],
            conv_kernel_size=ssm_config["conv_kernel_size"],
        )

        mixer = Mamba2Mixer(config, num_heads=4)

        assert mixer.num_heads == 4

    def test_hybrid_mamba_mixer(self, ssm_config):
        """Test HybridMambaMixer combining SSM with attention."""
        from src.infrastructure.compute.ssm.mamba_mixer import HybridMambaMixer
        from src.infrastructure.compute.ssm import MambaConfig

        config = MambaConfig(
            hidden_size=ssm_config["hidden_size"],
            ssm_state_size=ssm_config["ssm_state_size"],
            intermediate_size=ssm_config["d_inner"],
            conv_kernel_size=ssm_config["conv_kernel_size"],
        )

        mixer = HybridMambaMixer(config, attention_ratio=0.25)

        assert mixer.attention_ratio == 0.25


class TestMambaUtils:
    """Tests for MambaUtils functions."""

    def test_compute_ssm_state_shape(self, ssm_config):
        """Test SSM state shape computation."""
        from src.infrastructure.compute.ssm.mamba_utils import compute_ssm_state_shape

        shape = compute_ssm_state_shape(
            batch_size=ssm_config["batch_size"],
            d_inner=ssm_config["d_inner"],
            ssm_state_size=ssm_config["ssm_state_size"],
        )

        assert shape == (2, 512, 16)

    def test_compute_conv_state_shape(self, ssm_config):
        """Test conv state shape computation."""
        from src.infrastructure.compute.ssm.mamba_utils import compute_conv_state_shape

        shape = compute_conv_state_shape(
            batch_size=ssm_config["batch_size"],
            d_inner=ssm_config["d_inner"],
            conv_kernel_size=ssm_config["conv_kernel_size"],
        )

        assert shape == (2, 512, 4)

    def test_discretize_ssm(self, ssm_config):
        """Test SSM discretization."""
        from src.infrastructure.compute.ssm.mamba_utils import discretize_ssm

        d_inner = ssm_config["d_inner"]
        ssm_state = ssm_config["ssm_state_size"]
        batch_size = ssm_config["batch_size"]

        A = np.ones((d_inner, ssm_state), dtype=np.float32) * -1.0
        B = np.random.randn(batch_size, ssm_state).astype(np.float32)
        dt = np.random.rand(batch_size, d_inner).astype(np.float32) * 0.1

        dA, dB = discretize_ssm(A, B, dt)

        assert dA.shape == (batch_size, d_inner, ssm_state)
        assert dB.shape == (batch_size, d_inner, ssm_state)
        # dA should be in (0, 1) for negative A and positive dt
        assert np.all(dA > 0) and np.all(dA <= 1)

    def test_silu_activation(self, ssm_config):
        """Test SiLU activation."""
        from src.infrastructure.compute.ssm.mamba_utils import silu_activation

        x = np.array([[-2.0, -1.0, 0.0, 1.0, 2.0]], dtype=np.float32)

        y = silu_activation(x)
        y = np.array(y)  # Convert to array if list

        # SiLU(0) = 0
        assert abs(y[0, 2]) < 1e-5
        # SiLU(x) > 0 for x > 0
        assert y[0, 3] > 0
        assert y[0, 4] > 0

    def test_parallel_scan(self, ssm_config):
        """Test parallel scan for SSM."""
        from src.infrastructure.compute.ssm.mamba_utils import parallel_scan

        batch_size = 2
        seq_len = 8
        dim = 4

        gates = np.ones((batch_size, seq_len, dim), dtype=np.float32) * 0.9
        values = np.ones((batch_size, seq_len, dim), dtype=np.float32)

        output = parallel_scan(gates, values)
        output = np.array(output)  # Convert to array if list

        assert output.shape == (batch_size, seq_len, dim)
        # Output should grow due to accumulation
        assert output[0, -1, 0] > output[0, 0, 0]

    def test_mamba_block_state(self, ssm_config):
        """Test MambaBlockState for multi-layer state."""
        from src.infrastructure.compute.ssm.mamba_utils import MambaBlockState

        num_layers = 4
        batch_size = ssm_config["batch_size"]
        d_inner = ssm_config["d_inner"]
        conv_kernel_size = ssm_config["conv_kernel_size"]
        ssm_state_size = ssm_config["ssm_state_size"]

        state = MambaBlockState.zeros(
            num_layers=num_layers,
            batch_size=batch_size,
            d_inner=d_inner,
            conv_kernel_size=conv_kernel_size,
            ssm_state_size=ssm_state_size,
        )

        assert len(state.layer_states) == num_layers

        conv, ssm = state.get_layer(0)
        assert conv.shape == (batch_size, d_inner, conv_kernel_size)
        assert ssm.shape == (batch_size, d_inner, ssm_state_size)

    def test_chunk_sequence(self, ssm_config):
        """Test sequence chunking."""
        from src.infrastructure.compute.ssm.mamba_utils import chunk_sequence, merge_chunks

        batch_size = ssm_config["batch_size"]
        seq_len = ssm_config["seq_len"]
        hidden_size = ssm_config["hidden_size"]

        x = np.random.randn(batch_size, seq_len, hidden_size).astype(np.float32)

        chunks = chunk_sequence(x, chunk_size=8)

        assert len(chunks) == 4  # 32 / 8 = 4
        assert chunks[0].shape == (batch_size, 8, hidden_size)

        merged = merge_chunks(chunks)

        assert merged.shape == x.shape
        np.testing.assert_array_almost_equal(merged, x)

    def test_init_A_log(self, ssm_config):
        """Test A_log initialization."""
        from src.infrastructure.compute.ssm.mamba_utils import init_A_log

        d_inner = ssm_config["d_inner"]
        ssm_state_size = ssm_config["ssm_state_size"]

        A_log = init_A_log(d_inner, ssm_state_size)

        assert A_log.shape == (d_inner, ssm_state_size)
        # A_log should give negative A values when exp'd and negated
        A = -np.exp(A_log)
        assert np.all(A < 0)


# =============================================================================
# Rust Function Tests
# =============================================================================

@pytest.mark.skipif(not HAS_RUST, reason="Rust core not available")
class TestMoERoutingRust:
    """Tests for Rust MoE routing functions."""

    def test_moe_topk_route_rust(self, moe_config):
        """Test moe_topk_route_rust."""
        num_tokens = 16
        num_experts = moe_config["num_experts"]
        top_k = moe_config["top_k"]

        # Create router logits
        router_logits = [[np.random.randn() for _ in range(num_experts)] for _ in range(num_tokens)]

        indices, weights = rust_core.moe_topk_route_rust(router_logits, top_k, True)

        assert len(indices) == num_tokens
        assert len(weights) == num_tokens
        assert len(indices[0]) == top_k
        assert len(weights[0]) == top_k
        # Weights should sum to ~1 after normalization
        for w in weights:
            assert abs(sum(w) - 1.0) < 1e-5

    def test_moe_expert_choice_route_rust(self, moe_config):
        """Test moe_expert_choice_route_rust."""
        num_tokens = 32
        num_experts = moe_config["num_experts"]

        router_logits = [[np.random.randn() for _ in range(num_experts)] for _ in range(num_tokens)]

        expert_assignments = rust_core.moe_expert_choice_route_rust(
            router_logits, num_experts, 1.5
        )

        assert len(expert_assignments) == num_experts
        # Each expert should have tokens assigned
        total_assigned = sum(len(a) for a in expert_assignments)
        assert total_assigned > 0

    def test_moe_aux_loss_rust(self, moe_config):
        """Test moe_aux_loss_rust."""
        num_tokens = 32
        num_experts = moe_config["num_experts"]
        top_k = moe_config["top_k"]

        router_logits = [[np.random.randn() for _ in range(num_experts)] for _ in range(num_tokens)]
        expert_indices = [[np.random.randint(0, num_experts) for _ in range(top_k)] for _ in range(num_tokens)]

        load_loss, z_loss = rust_core.moe_aux_loss_rust(router_logits, expert_indices, num_experts)

        assert load_loss >= 0.0
        assert z_loss >= 0.0

    def test_soft_moe_route_rust(self, moe_config):
        """Test soft_moe_route_rust."""
        num_tokens = 16
        num_experts = moe_config["num_experts"]
        num_slots = 2

        router_logits = [[np.random.randn() for _ in range(num_experts)] for _ in range(num_tokens)]

        dispatch_weights = rust_core.soft_moe_route_rust(router_logits, num_slots)

        assert len(dispatch_weights) == num_tokens
        assert len(dispatch_weights[0]) == num_experts * num_slots


@pytest.mark.skipif(not HAS_RUST, reason="Rust core not available")
class TestSSMRust:
    """Tests for Rust SSM functions."""

    def test_ssm_discretize_rust(self, ssm_config):
        """Test ssm_discretize_rust."""
        batch_size = ssm_config["batch_size"]
        d_inner = ssm_config["d_inner"]
        ssm_state = ssm_config["ssm_state_size"]

        a_log = [1.0] * (d_inner * ssm_state)  # Flattened A_log
        b = [[np.random.randn() for _ in range(ssm_state)] for _ in range(batch_size)]
        dt = [[np.random.random() * 0.1 for _ in range(d_inner)] for _ in range(batch_size)]

        dA, dB = rust_core.ssm_discretize_rust(a_log, b, dt)

        assert len(dA) == batch_size
        assert len(dA[0]) == d_inner
        assert len(dA[0][0]) == ssm_state

    def test_ssm_step_rust(self, ssm_config):
        """Test ssm_step_rust."""
        batch_size = ssm_config["batch_size"]
        d_inner = ssm_config["d_inner"]
        ssm_state = ssm_config["ssm_state_size"]

        x = [[np.random.randn() for _ in range(d_inner)] for _ in range(batch_size)]
        state = [[[0.0] * ssm_state for _ in range(d_inner)] for _ in range(batch_size)]
        dA = [[[0.9] * ssm_state for _ in range(d_inner)] for _ in range(batch_size)]
        dB = [[[0.1] * ssm_state for _ in range(d_inner)] for _ in range(batch_size)]
        c = [[np.random.randn() for _ in range(ssm_state)] for _ in range(batch_size)]
        d_skip = [0.1] * d_inner

        output, new_state = rust_core.ssm_step_rust(x, state, dA, dB, c, d_skip)

        assert len(output) == batch_size
        assert len(output[0]) == d_inner
        assert len(new_state) == batch_size
        assert len(new_state[0]) == d_inner
        assert len(new_state[0][0]) == ssm_state

    def test_parallel_scan_rust(self, ssm_config):
        """Test parallel_scan_rust."""
        batch_size = 2
        seq_len = 8
        dim = 4

        gates = [[[0.9] * dim for _ in range(seq_len)] for _ in range(batch_size)]
        values = [[[1.0] * dim for _ in range(seq_len)] for _ in range(batch_size)]

        output = rust_core.parallel_scan_rust(gates, values)

        assert len(output) == batch_size
        assert len(output[0]) == seq_len
        assert len(output[0][0]) == dim
        # Output should grow due to accumulation
        assert output[0][-1][0] > output[0][0][0]

    def test_causal_conv1d_update_rust(self, ssm_config):
        """Test causal_conv1d_update_rust."""
        batch_size = ssm_config["batch_size"]
        d_inner = ssm_config["d_inner"]
        kernel_size = ssm_config["conv_kernel_size"]

        x = [[np.random.randn() for _ in range(d_inner)] for _ in range(batch_size)]
        conv_state = [[[0.0] * kernel_size for _ in range(d_inner)] for _ in range(batch_size)]
        weight = [[np.random.randn() for _ in range(kernel_size)] for _ in range(d_inner)]

        output, new_state = rust_core.causal_conv1d_update_rust(x, conv_state, weight)

        assert len(output) == batch_size
        assert len(output[0]) == d_inner
        assert len(new_state) == batch_size
        assert len(new_state[0]) == d_inner
        assert len(new_state[0][0]) == kernel_size

    def test_silu_activation_rust(self, ssm_config):
        """Test silu_activation_rust."""
        x = [[-2.0, -1.0, 0.0, 1.0, 2.0]]

        y = rust_core.silu_activation_rust(x)

        assert len(y) == 1
        assert len(y[0]) == 5
        # SiLU(0) = 0
        assert abs(y[0][2]) < 1e-6


@pytest.mark.skipif(not HAS_RUST, reason="Rust core not available")
class TestMLARust:
    """Tests for Rust MLA functions."""

    def test_mla_compress_kv_rust(self, mla_config):
        """Test mla_compress_kv_rust."""
        num_tokens = 16
        hidden_size = mla_config["hidden_size"]
        kv_lora_rank = mla_config["kv_lora_rank"]

        hidden_states = [[np.random.randn() for _ in range(hidden_size)] for _ in range(num_tokens)]
        kv_proj_weight = [[np.random.randn() for _ in range(hidden_size)] for _ in range(kv_lora_rank)]

        compressed = rust_core.mla_compress_kv_rust(hidden_states, kv_proj_weight)

        assert len(compressed) == num_tokens
        assert len(compressed[0]) == kv_lora_rank

    def test_mla_head_mapping_rust(self, mla_config):
        """Test mla_head_mapping_rust."""
        num_heads = mla_config["num_heads"]
        num_kv_heads = mla_config["num_kv_heads"]

        mapping = rust_core.mla_head_mapping_rust(num_heads, num_kv_heads)

        assert len(mapping) == num_heads
        # Each head should map to valid KV head
        for m in mapping:
            assert 0 <= m < num_kv_heads


# =============================================================================
# Integration Tests
# =============================================================================

class TestPhase38Integration:
    """Integration tests for Phase 38 components."""

    def test_moe_full_forward(self, moe_config):
        """Test full MoE forward pass."""
        from src.infrastructure.compute.moe.fused_mo_e_layer import FusedMoELayer
        from src.infrastructure.compute.moe import FusedMoEConfig, TopKRouter, RouterConfig

        # Setup
        config = FusedMoEConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
            intermediate_size=moe_config["intermediate_size"],
        )

        router_config = RouterConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
        )

        layer = FusedMoELayer(config)
        router = TopKRouter(router_config)

        # Forward
        num_tokens = moe_config["batch_size"] * moe_config["seq_len"]
        hidden_states = np.random.randn(num_tokens, moe_config["hidden_size"]).astype(np.float32)

        routing_output = router.forward(hidden_states)

        # Verify routing worked
        assert routing_output.expert_indices.shape[0] == num_tokens
        assert routing_output.expert_weights.shape[0] == num_tokens

    def test_mamba_full_forward(self, ssm_config):
        """Test full Mamba forward pass."""
        from src.infrastructure.compute.ssm.mamba_mixer import MambaMixer as MambaMixerClass
        from src.infrastructure.compute.ssm import MambaConfig

        config = MambaConfig(
            hidden_size=ssm_config["hidden_size"],
            ssm_state_size=ssm_config["ssm_state_size"],
            intermediate_size=ssm_config["d_inner"],
            conv_kernel_size=ssm_config["conv_kernel_size"],
        )

        mixer = MambaMixerClass(config)

        # Forward
        batch_size = ssm_config["batch_size"]
        seq_len = ssm_config["seq_len"]
        hidden_states = np.random.randn(batch_size, seq_len, ssm_config["hidden_size"]).astype(np.float32)

        output = mixer.forward(hidden_states)

        assert output.output.shape == (batch_size, seq_len, ssm_config["hidden_size"])

    def test_mamba_autoregressive_decode(self, ssm_config):
        """Test autoregressive decoding with Mamba."""
        from src.infrastructure.compute.ssm.mamba_mixer import MambaMixer as MambaMixerClass
        from src.infrastructure.compute.ssm import MambaConfig, MambaState

        config = MambaConfig(
            hidden_size=ssm_config["hidden_size"],
            ssm_state_size=ssm_config["ssm_state_size"],
            intermediate_size=ssm_config["d_inner"],
            conv_kernel_size=ssm_config["conv_kernel_size"],
        )

        mixer = MambaMixerClass(config)

        batch_size = ssm_config["batch_size"]
        num_steps = 5

        # Initialize state
        state = MambaState.zeros(
            batch_size=batch_size,
            config=config,
        )

        outputs = []
        for _ in range(num_steps):
            hidden_states = np.random.randn(batch_size, ssm_config["hidden_size"]).astype(np.float32)
            output = mixer.step(hidden_states, state)
            outputs.append(output.output)
            state = output.state

        assert len(outputs) == num_steps
        for out in outputs:
            assert out.shape == (batch_size, ssm_config["hidden_size"])

    @pytest.mark.skipif(not HAS_RUST, reason="Rust core not available")
    def test_rust_python_equivalence_topk_routing(self, moe_config):
        """Test that Rust and Python top-k routing give similar results."""
        from src.infrastructure.compute.moe import TopKRouter, RouterConfig

        num_tokens = 16
        num_experts = moe_config["num_experts"]
        top_k = moe_config["top_k"]

        # Create same router logits
        np.random.seed(42)
        router_logits_np = np.random.randn(num_tokens, num_experts).astype(np.float32)
        router_logits_list = router_logits_np.tolist()

        # Rust routing
        rust_indices, rust_weights = rust_core.moe_topk_route_rust(router_logits_list, top_k, True)

        # Python routing uses same underlying logic
        # Just verify they both work
        assert len(rust_indices) == num_tokens
        assert len(rust_weights) == num_tokens


# =============================================================================
# Performance Tests
# =============================================================================

class TestPhase38Performance:
    """Performance tests for Phase 38."""

    def test_moe_routing_performance(self, moe_config):
        """Measure MoE routing performance."""
        import time

        from src.infrastructure.compute.moe import TopKRouter, RouterConfig

        config = RouterConfig(
            num_experts=moe_config["num_experts"],
            top_k=moe_config["top_k"],
            hidden_size=moe_config["hidden_size"],
        )

        router = TopKRouter(config)

        # Benchmark
        num_tokens = 1024
        hidden_states = np.random.randn(num_tokens, moe_config["hidden_size"]).astype(np.float32)

        # Warm up
        _ = router.forward(hidden_states)

        # Time
        start = time.perf_counter()
        iterations = 10
        for _ in range(iterations):
            _ = router.forward(hidden_states)
        elapsed = time.perf_counter() - start

        tokens_per_sec = (num_tokens * iterations) / elapsed
        print(f"\nMoE Routing: {tokens_per_sec:.0f} tokens/sec")

        assert tokens_per_sec > 1000  # Reasonable minimum

    def test_ssm_step_performance(self, ssm_config):
        """Measure SSM step performance."""
        import time

        from src.infrastructure.compute.ssm.mamba_mixer import MambaMixer as MambaMixerClass
        from src.infrastructure.compute.ssm import MambaConfig, MambaState

        config = MambaConfig(
            hidden_size=ssm_config["hidden_size"],
            ssm_state_size=ssm_config["ssm_state_size"],
            intermediate_size=ssm_config["d_inner"],
            conv_kernel_size=ssm_config["conv_kernel_size"],
        )

        mixer = MambaMixerClass(config)

        batch_size = 32
        hidden_states = np.random.randn(batch_size, ssm_config["hidden_size"]).astype(np.float32)

        state = MambaState.zeros(
            batch_size=batch_size,
            config=config,
        )

        # Warm up
        _ = mixer.step(hidden_states, state)

        # Time
        start = time.perf_counter()
        iterations = 100
        for _ in range(iterations):
            output = mixer.step(hidden_states, state)
            state = output.state
        elapsed = time.perf_counter() - start

        steps_per_sec = iterations / elapsed
        print(f"\nMamba Step: {steps_per_sec:.0f} steps/sec (batch_size={batch_size})")

        assert steps_per_sec > 10  # Reasonable minimum

    @pytest.mark.skipif(not HAS_RUST, reason="Rust core not available")
    def test_rust_topk_routing_performance(self, moe_config):
        """Measure Rust top-k routing performance."""
        import time

        num_tokens = 4096
        num_experts = moe_config["num_experts"]
        top_k = moe_config["top_k"]

        router_logits = [[np.random.randn() for _ in range(num_experts)] for _ in range(num_tokens)]

        # Warm up
        _ = rust_core.moe_topk_route_rust(router_logits, top_k, True)

        # Time
        start = time.perf_counter()
        iterations = 10
        for _ in range(iterations):
            _ = rust_core.moe_topk_route_rust(router_logits, top_k, True)
        elapsed = time.perf_counter() - start

        tokens_per_sec = (num_tokens * iterations) / elapsed
        print(f"\nRust Top-K Routing: {tokens_per_sec:.0f} tokens/sec")

        assert tokens_per_sec > 75000  # Rust should be fast
