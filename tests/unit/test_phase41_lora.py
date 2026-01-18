# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Unit Tests for LoRA Manager

"""
Tests for LoRAManager module.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import json

from src.infrastructure.lora.LoRAManager import (
    LoRAMethod,
    AdapterStatus,
    TargetModule,
    LoRAConfig,
    LoRARequest,
    LoRAInfo,
    AdapterSlot,
    LoRAWeights,
    LoRAAdapter,
    LoRARegistry,
    LoRASlotManager,
    LoRAManager,
    load_lora_adapter,
    merge_adapters,
    get_lora_info,
)


class TestLoRAEnums:
    """Test LoRA enums."""
    
    def test_lora_method_values(self):
        """Test LoRAMethod enum values."""
        assert LoRAMethod.LORA is not None
        assert LoRAMethod.QLORA is not None
        assert LoRAMethod.DORA is not None
        assert LoRAMethod.RSLORA is not None
        assert LoRAMethod.ADALORA is not None
    
    def test_adapter_status_values(self):
        """Test AdapterStatus enum values."""
        assert AdapterStatus.LOADING is not None
        assert AdapterStatus.READY is not None
        assert AdapterStatus.ACTIVE is not None
        assert AdapterStatus.INACTIVE is not None
        assert AdapterStatus.EVICTING is not None
        assert AdapterStatus.ERROR is not None
    
    def test_target_module_values(self):
        """Test TargetModule enum values."""
        assert TargetModule.Q_PROJ.value == "q_proj"
        assert TargetModule.K_PROJ.value == "k_proj"
        assert TargetModule.V_PROJ.value == "v_proj"
        assert TargetModule.O_PROJ.value == "o_proj"


class TestLoRAConfig:
    """Test LoRAConfig dataclass."""
    
    def test_default_config(self):
        """Test default LoRAConfig values."""
        config = LoRAConfig(
            adapter_name="test-adapter",
            adapter_path="/path/to/adapter",
        )
        
        assert config.adapter_name == "test-adapter"
        assert config.adapter_path == "/path/to/adapter"
        assert config.rank == 8
        assert config.alpha == 16.0
        assert config.dropout == 0.0
        assert config.method == LoRAMethod.LORA
    
    def test_custom_config(self):
        """Test custom LoRAConfig values."""
        config = LoRAConfig(
            adapter_name="custom-adapter",
            adapter_path="/path/to/adapter",
            rank=16,
            alpha=32.0,
            dropout=0.1,
            method=LoRAMethod.QLORA,
            target_modules=["q_proj", "v_proj"],
        )
        
        assert config.rank == 16
        assert config.alpha == 32.0
        assert config.dropout == 0.1
        assert config.method == LoRAMethod.QLORA
        assert len(config.target_modules) == 2
    
    def test_computed_scaling_standard(self):
        """Test standard LoRA scaling."""
        config = LoRAConfig(
            adapter_name="test",
            adapter_path="/path",
            rank=8,
            alpha=16.0,
            use_rslora=False,
        )
        
        # Standard: alpha / rank = 16 / 8 = 2.0
        assert config.computed_scaling == pytest.approx(2.0)
    
    def test_computed_scaling_rslora(self):
        """Test rsLoRA scaling."""
        config = LoRAConfig(
            adapter_name="test",
            adapter_path="/path",
            rank=16,
            alpha=16.0,
            use_rslora=True,
        )
        
        # rsLoRA: alpha / sqrt(rank) = 16 / 4 = 4.0
        assert config.computed_scaling == pytest.approx(4.0)
    
    def test_config_hash(self):
        """Test LoRAConfig hash."""
        config1 = LoRAConfig(adapter_name="test", adapter_path="/path")
        config2 = LoRAConfig(adapter_name="test", adapter_path="/path")
        config3 = LoRAConfig(adapter_name="other", adapter_path="/path")
        
        assert hash(config1) == hash(config2)
        assert hash(config1) != hash(config3)


class TestLoRARequest:
    """Test LoRARequest dataclass."""
    
    def test_lora_request(self):
        """Test LoRARequest creation."""
        request = LoRARequest(
            request_id="req-123",
            adapter_name="test-adapter",
        )
        
        assert request.request_id == "req-123"
        assert request.adapter_name == "test-adapter"
        assert request.priority == 0
    
    def test_lora_request_hash(self):
        """Test LoRARequest hash."""
        req1 = LoRARequest(request_id="req-1", adapter_name="adapter-1")
        req2 = LoRARequest(request_id="req-1", adapter_name="adapter-1")
        
        assert hash(req1) == hash(req2)


class TestLoRAInfo:
    """Test LoRAInfo dataclass."""
    
    def test_lora_info(self):
        """Test LoRAInfo creation."""
        info = LoRAInfo(
            adapter_name="test-adapter",
            rank=8,
            alpha=16.0,
            method=LoRAMethod.LORA,
            target_modules=["q_proj", "v_proj"],
            num_parameters=1000000,
            memory_bytes=4000000,
            status=AdapterStatus.READY,
        )
        
        assert info.adapter_name == "test-adapter"
        assert info.rank == 8
        assert info.alpha == 16.0
        assert info.num_parameters == 1000000
    
    def test_lora_info_to_dict(self):
        """Test LoRAInfo to_dict method."""
        info = LoRAInfo(
            adapter_name="test-adapter",
            rank=8,
            alpha=16.0,
            method=LoRAMethod.LORA,
            target_modules=["q_proj"],
            num_parameters=1000000,
            memory_bytes=4000000,
            status=AdapterStatus.READY,
        )
        
        d = info.to_dict()
        assert d["adapter_name"] == "test-adapter"
        assert d["rank"] == 8
        assert d["method"] == "LORA"
        assert d["status"] == "READY"


class TestAdapterSlot:
    """Test AdapterSlot dataclass."""
    
    def test_adapter_slot_free(self):
        """Test free AdapterSlot."""
        slot = AdapterSlot(slot_id=0)
        
        assert slot.slot_id == 0
        assert slot.is_free
        assert slot.adapter_name is None
    
    def test_adapter_slot_occupied(self):
        """Test occupied AdapterSlot."""
        slot = AdapterSlot(
            slot_id=0,
            adapter_name="test-adapter",
            is_active=True,
        )
        
        assert not slot.is_free
        assert slot.adapter_name == "test-adapter"
        assert slot.is_active


class TestLoRAWeights:
    """Test LoRAWeights dataclass."""
    
    def test_lora_weights_empty(self):
        """Test empty LoRAWeights."""
        weights = LoRAWeights()
        
        assert weights.num_parameters == 0
        assert weights.memory_bytes == 0
    
    def test_lora_weights_with_data(self):
        """Test LoRAWeights with data."""
        lora_a = {"q_proj": np.random.randn(8, 4096).astype(np.float32)}
        lora_b = {"q_proj": np.random.randn(4096, 8).astype(np.float32)}
        
        weights = LoRAWeights(lora_a=lora_a, lora_b=lora_b)
        
        # 8*4096 + 4096*8 = 65536 parameters
        assert weights.num_parameters == 65536
        assert weights.memory_bytes > 0


class TestLoRASlotManager:
    """Test LoRASlotManager class."""
    
    def test_slot_manager_creation(self):
        """Test LoRASlotManager creation."""
        manager = LoRASlotManager(num_slots=8)
        
        assert manager.num_slots == 8
    
    def test_allocate_slot(self):
        """Test slot allocation."""
        manager = LoRASlotManager(num_slots=4)
        
        slot_id = manager.allocate("adapter-1", memory_required=1000)
        
        assert slot_id is not None
        assert slot_id >= 0
        assert slot_id < 4
    
    def test_allocate_same_adapter_twice(self):
        """Test allocating same adapter returns same slot."""
        manager = LoRASlotManager(num_slots=4)
        
        slot1 = manager.allocate("adapter-1")
        slot2 = manager.allocate("adapter-1")
        
        assert slot1 == slot2
    
    def test_release_slot(self):
        """Test releasing a slot."""
        manager = LoRASlotManager(num_slots=4)
        
        manager.allocate("adapter-1")
        manager.release("adapter-1")
        
        # Should still be loaded but inactive
        slot = manager.get_slot("adapter-1")
        assert slot is not None
    
    def test_evict_slot(self):
        """Test evicting a slot."""
        manager = LoRASlotManager(num_slots=4)
        
        manager.allocate("adapter-1")
        result = manager.evict("adapter-1")
        
        assert result is True
        assert manager.get_slot("adapter-1") is None
    
    def test_get_active_adapters(self):
        """Test getting active adapters."""
        manager = LoRASlotManager(num_slots=4)
        
        manager.allocate("adapter-1")
        manager.allocate("adapter-2")
        manager.release("adapter-1")
        
        active = manager.get_active_adapters()
        
        assert "adapter-2" in active
        assert "adapter-1" not in active
    
    def test_get_stats(self):
        """Test getting slot statistics."""
        manager = LoRASlotManager(num_slots=4)
        
        manager.allocate("adapter-1")
        
        stats = manager.get_stats()
        
        assert stats["total_slots"] == 4
        assert stats["free_slots"] == 3
        assert stats["active_slots"] == 1


class TestLoRARegistry:
    """Test LoRARegistry class."""
    
    def test_registry_creation(self):
        """Test LoRARegistry creation."""
        registry = LoRARegistry(max_cached=16)
        
        stats = registry.get_stats()
        assert stats["max_cached"] == 16
    
    def test_list_adapters(self):
        """Test listing adapters."""
        registry = LoRARegistry(max_cached=16)
        
        adapters = registry.list_adapters()
        assert isinstance(adapters, list)
    
    def test_unregister_nonexistent(self):
        """Test unregistering non-existent adapter."""
        registry = LoRARegistry(max_cached=16)
        
        result = registry.unregister("nonexistent")
        assert result is False


class TestLoRAManager:
    """Test LoRAManager class."""
    
    def test_manager_creation(self):
        """Test LoRAManager creation."""
        manager = LoRAManager(
            max_loras=16,
            max_gpu_slots=8,
            max_rank=64,
        )
        
        assert manager.max_loras == 16
        assert manager.max_rank == 64
    
    def test_list_loaded_adapters(self):
        """Test listing loaded adapters."""
        manager = LoRAManager()
        
        adapters = manager.list_loaded_adapters()
        assert isinstance(adapters, list)
    
    def test_get_active_adapters(self):
        """Test getting active adapters."""
        manager = LoRAManager()
        
        active = manager.get_active_adapters()
        assert isinstance(active, list)
    
    def test_get_stats(self):
        """Test getting manager statistics."""
        manager = LoRAManager()
        
        stats = manager.get_stats()
        
        assert "registry" in stats
        assert "slots" in stats
        assert "active_requests" in stats
    
    def test_load_adapter_rank_too_high(self):
        """Test loading adapter with rank too high."""
        manager = LoRAManager(max_rank=32)
        
        config = LoRAConfig(
            adapter_name="test",
            adapter_path="/path",
            rank=64,  # Higher than max_rank
        )
        
        with pytest.raises(ValueError, match="exceeds max_rank"):
            manager.load_adapter(config)


class TestLoRAAdapter:
    """Test LoRAAdapter class."""
    
    def test_adapter_creation(self):
        """Test LoRAAdapter creation."""
        config = LoRAConfig(
            adapter_name="test-adapter",
            adapter_path="/path/to/adapter",
        )
        
        adapter = LoRAAdapter(config)
        
        assert adapter.name == "test-adapter"
        assert adapter.status == AdapterStatus.LOADING
    
    def test_apply_to_linear(self):
        """Test applying LoRA to linear output."""
        config = LoRAConfig(
            adapter_name="test",
            adapter_path="/path",
            rank=8,
            alpha=16.0,
        )
        
        adapter = LoRAAdapter(config)
        
        # Create mock weights
        adapter.weights = LoRAWeights(
            lora_a={"q_proj": np.random.randn(8, 4096).astype(np.float32)},
            lora_b={"q_proj": np.random.randn(4096, 8).astype(np.float32)},
            scales={"q_proj": 2.0},
        )
        
        hidden_states = np.random.randn(1, 4096).astype(np.float32)
        delta = adapter.apply_to_linear("q_proj", hidden_states)
        
        assert delta.shape == hidden_states.shape


class TestMergeAdapters:
    """Test merge_adapters function."""
    
    def test_merge_empty_list(self):
        """Test merging empty list raises error."""
        with pytest.raises(ValueError, match="No adapters to merge"):
            merge_adapters([])
    
    def test_merge_single_adapter(self):
        """Test merging single adapter."""
        config = LoRAConfig(adapter_name="test", adapter_path="/path")
        adapter = LoRAAdapter(config)
        adapter.weights = LoRAWeights(
            lora_a={"q_proj": np.ones((8, 4096), dtype=np.float32)},
            lora_b={"q_proj": np.ones((4096, 8), dtype=np.float32)},
        )
        
        merged = merge_adapters([adapter])
        
        assert "q_proj" in merged.lora_a
        assert "q_proj" in merged.lora_b
    
    def test_merge_with_weights(self):
        """Test merging with custom weights."""
        config = LoRAConfig(adapter_name="test", adapter_path="/path")
        
        adapter1 = LoRAAdapter(config)
        adapter1.weights = LoRAWeights(
            lora_a={"q_proj": np.ones((8, 4096), dtype=np.float32)},
            lora_b={"q_proj": np.ones((4096, 8), dtype=np.float32)},
        )
        
        adapter2 = LoRAAdapter(config)
        adapter2.weights = LoRAWeights(
            lora_a={"q_proj": np.ones((8, 4096), dtype=np.float32) * 2},
            lora_b={"q_proj": np.ones((4096, 8), dtype=np.float32) * 2},
        )
        
        merged = merge_adapters([adapter1, adapter2], weights=[0.5, 0.5])
        
        # Should be average: (1 + 2) / 2 = 1.5
        assert np.allclose(merged.lora_a["q_proj"], 1.5)
    
    def test_merge_mismatched_weights(self):
        """Test merging with mismatched weights count."""
        config = LoRAConfig(adapter_name="test", adapter_path="/path")
        adapter = LoRAAdapter(config)
        adapter.weights = LoRAWeights()
        
        with pytest.raises(ValueError, match="Number of weights must match"):
            merge_adapters([adapter], weights=[0.5, 0.5])
