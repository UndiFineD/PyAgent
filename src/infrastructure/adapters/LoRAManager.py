"""
LoRA Manager - Dynamic Low-Rank Adapter management for LLM inference.

Inspired by vLLM's LoRA implementation (LoRAModel, LoRAModelManager,
PackedLoRALayerWeights) for efficient multi-adapter serving.

Phase 27: Attention, Quantization & LoRA Patterns
"""

from __future__ import annotations

import hashlib
import math
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Iterator, Protocol

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


class LoRATarget(Enum):
    """Common LoRA target modules."""
    Q_PROJ = "q_proj"
    K_PROJ = "k_proj"
    V_PROJ = "v_proj"
    O_PROJ = "o_proj"
    GATE_PROJ = "gate_proj"
    UP_PROJ = "up_proj"
    DOWN_PROJ = "down_proj"
    QKV_PROJ = "qkv_proj"  # Packed QKV
    GATE_UP_PROJ = "gate_up_proj"  # Packed gate+up
    LM_HEAD = "lm_head"
    EMBED_TOKENS = "embed_tokens"


@dataclass
class LoRAConfig:
    """Configuration for LoRA adapter.
    
    Attributes:
        rank: LoRA rank (r)
        alpha: LoRA alpha for scaling
        dropout: Dropout probability
        target_modules: Set of module names to apply LoRA
        fan_in_fan_out: Whether weight is (in, out) instead of (out, in)
        bias: Bias mode ("none", "all", "lora_only")
        modules_to_save: Modules to save full weights (not LoRA)
    """
    rank: int = 8
    alpha: float = 16.0
    dropout: float = 0.0
    target_modules: set[str] = field(default_factory=lambda: {
        "q_proj", "k_proj", "v_proj", "o_proj"
    })
    fan_in_fan_out: bool = False
    bias: str = "none"
    modules_to_save: set[str] = field(default_factory=set)
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        """Validate configuration."""
        if self.rank <= 0:
            raise ValueError(f"rank must be positive, got {self.rank}")
        if self.alpha <= 0:
            raise ValueError(f"alpha must be positive, got {self.alpha}")
        if self.dropout < 0 or self.dropout >= 1:
            raise ValueError(f"dropout must be in [0, 1), got {self.dropout}")
        if self.bias not in ("none", "all", "lora_only"):
            raise ValueError(f"bias must be 'none', 'all', or 'lora_only', got {self.bias}")
    
    @property
    def scaling(self) -> float:
        """LoRA scaling factor (alpha / rank)."""
        return self.alpha / self.rank


@dataclass
class LoRALayerWeights:
    """LoRA weights for a single layer.
    
    Implements: h = W_0 * x + (B @ A) * x * scaling
    
    Attributes:
        lora_a: Low-rank A matrix [rank, in_features]
        lora_b: Low-rank B matrix [out_features, rank]
        scaling: Scaling factor (alpha / rank)
        module_name: Name of target module
        dropout: Dropout probability
    """
    lora_a: NDArray[np.float32]  # [rank, in_features]
    lora_b: NDArray[np.float32]  # [out_features, rank]
    scaling: float
    module_name: str
    dropout: float = 0.0
    
    @property
    def rank(self) -> int:
        """LoRA rank."""
        return self.lora_a.shape[0]
    
    @property
    def in_features(self) -> int:
        """Input dimension."""
        return self.lora_a.shape[1]
    
    @property
    def out_features(self) -> int:
        """Output dimension."""
        return self.lora_b.shape[0]
    
    def forward(
        self,
        x: NDArray[np.float32],
        apply_dropout: bool = False,
    ) -> NDArray[np.float32]:
        """Compute LoRA output.
        
        Args:
            x: Input tensor [..., in_features]
            apply_dropout: Whether to apply dropout
            
        Returns:
            LoRA output [..., out_features]
        """
        # x @ A.T @ B.T * scaling
        hidden = x @ self.lora_a.T  # [..., rank]
        
        if apply_dropout and self.dropout > 0:
            mask = np.random.binomial(1, 1 - self.dropout, hidden.shape)
            hidden = hidden * mask / (1 - self.dropout)
        
        output = hidden @ self.lora_b.T  # [..., out_features]
        return output * self.scaling
    
    def merge_into_base(
        self,
        base_weight: NDArray[np.float32],
    ) -> NDArray[np.float32]:
        """Merge LoRA weights into base weight.
        
        Args:
            base_weight: Base weight [out_features, in_features]
            
        Returns:
            Merged weight
        """
        # W_merged = W_base + B @ A * scaling
        delta = self.lora_b @ self.lora_a * self.scaling
        return base_weight + delta
    
    def get_memory_bytes(self) -> int:
        """Memory usage in bytes."""
        return self.lora_a.nbytes + self.lora_b.nbytes


@dataclass
class PackedLoRAWeights:
    """Packed LoRA weights for fused QKV or gate+up projections.
    
    Enables efficient batched computation for merged attention/MLP projections.
    
    Attributes:
        lora_a: Packed A matrices [num_layers, rank, in_features]
        lora_b: Packed B matrices [num_layers, out_features, rank]
        scalings: Per-layer scaling factors
        module_names: Ordered list of packed module names
    """
    lora_a: NDArray[np.float32]  # [num_layers, rank, in_features]
    lora_b: NDArray[np.float32]  # [num_layers, out_features, rank]
    scalings: list[float]
    module_names: list[str]
    
    @classmethod
    def from_individual(
        cls,
        layer_weights: list[LoRALayerWeights],
    ) -> PackedLoRAWeights:
        """Create packed weights from individual layer weights.
        
        Args:
            layer_weights: List of LoRA layer weights
            
        Returns:
            Packed LoRA weights
        """
        if not layer_weights:
            raise ValueError("layer_weights cannot be empty")
        
        lora_a = np.stack([lw.lora_a for lw in layer_weights])
        lora_b = np.stack([lw.lora_b for lw in layer_weights])
        scalings = [lw.scaling for lw in layer_weights]
        module_names = [lw.module_name for lw in layer_weights]
        
        return cls(lora_a, lora_b, scalings, module_names)
    
    def unpack(self) -> list[LoRALayerWeights]:
        """Unpack into individual layer weights."""
        return [
            LoRALayerWeights(
                lora_a=self.lora_a[i],
                lora_b=self.lora_b[i],
                scaling=self.scalings[i],
                module_name=self.module_names[i],
            )
            for i in range(len(self.module_names))
        ]
    
    @property
    def num_layers(self) -> int:
        """Number of packed layers."""
        return len(self.module_names)


@dataclass
class LoRAModel:
    """Complete LoRA model with all adapter weights.
    
    Attributes:
        model_id: Unique identifier for this LoRA model
        config: LoRA configuration
        layers: Dictionary mapping module name to weights
        metadata: Optional metadata
    """
    model_id: str
    config: LoRAConfig
    layers: dict[str, LoRALayerWeights] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def add_layer(self, layer: LoRALayerWeights):
        """Add a layer to the model."""
        self.layers[layer.module_name] = layer
    
    def get_layer(self, module_name: str) -> LoRALayerWeights | None:
        """Get layer weights by module name."""
        return self.layers.get(module_name)
    
    def forward(
        self,
        module_name: str,
        x: NDArray[np.float32],
        apply_dropout: bool = False,
    ) -> NDArray[np.float32] | None:
        """Compute LoRA output for a module.
        
        Args:
            module_name: Name of target module
            x: Input tensor
            apply_dropout: Whether to apply dropout
            
        Returns:
            LoRA output or None if module not in adapter
        """
        layer = self.layers.get(module_name)
        if layer is None:
            return None
        return layer.forward(x, apply_dropout)
    
    def get_memory_bytes(self) -> int:
        """Total memory usage in bytes."""
        return sum(layer.get_memory_bytes() for layer in self.layers.values())
    
    @property
    def num_parameters(self) -> int:
        """Total number of LoRA parameters."""
        return sum(
            layer.lora_a.size + layer.lora_b.size
            for layer in self.layers.values()
        )


class LoRAModelState(Enum):
    """State of a LoRA model in the manager."""
    LOADED = "loaded"
    ACTIVE = "active"
    EVICTED = "evicted"


@dataclass
class LoRAModelEntry:
    """Entry in the LoRA registry."""
    model: LoRAModel
    state: LoRAModelState
    load_time: float
    last_access: float
    access_count: int = 0
    
    def touch(self):
        """Update access time and count."""
        self.last_access = time.time()
        self.access_count += 1


class LoRARegistry:
    """Registry for managing multiple LoRA adapters.
    
    Implements LRU eviction when memory budget is exceeded.
    
    Attributes:
        max_memory_bytes: Maximum memory budget
        max_models: Maximum number of models
    """
    
    def __init__(
        self,
        max_memory_bytes: int = 1024 * 1024 * 1024,  # 1GB
        max_models: int = 16,
    ):
        """Initialize registry.
        
        Args:
            max_memory_bytes: Memory budget in bytes
            max_models: Maximum number of loaded models
        """
        self.max_memory_bytes = max_memory_bytes
        self.max_models = max_models
        self._models: OrderedDict[str, LoRAModelEntry] = OrderedDict()
        self._current_memory = 0
    
    def register(self, model: LoRAModel) -> bool:
        """Register a LoRA model.
        
        Args:
            model: LoRA model to register
            
        Returns:
            True if registered, False if rejected
        """
        model_memory = model.get_memory_bytes()
        
        # Evict if needed
        while (
            self._current_memory + model_memory > self.max_memory_bytes
            or len(self._models) >= self.max_models
        ) and self._models:
            self._evict_lru()
        
        if self._current_memory + model_memory > self.max_memory_bytes:
            return False
        
        now = time.time()
        entry = LoRAModelEntry(
            model=model,
            state=LoRAModelState.LOADED,
            load_time=now,
            last_access=now,
        )
        self._models[model.model_id] = entry
        self._models.move_to_end(model.model_id)
        self._current_memory += model_memory
        
        return True
    
    def get(self, model_id: str) -> LoRAModel | None:
        """Get a model by ID.
        
        Args:
            model_id: Model identifier
            
        Returns:
            LoRA model or None
        """
        entry = self._models.get(model_id)
        if entry is None:
            return None
        
        entry.touch()
        self._models.move_to_end(model_id)
        return entry.model
    
    def unregister(self, model_id: str) -> bool:
        """Unregister a model.
        
        Args:
            model_id: Model identifier
            
        Returns:
            True if unregistered
        """
        entry = self._models.pop(model_id, None)
        if entry is None:
            return False
        
        self._current_memory -= entry.model.get_memory_bytes()
        return True
    
    def _evict_lru(self):
        """Evict least recently used model."""
        if not self._models:
            return
        
        # Get LRU (first item)
        model_id, entry = next(iter(self._models.items()))
        self._current_memory -= entry.model.get_memory_bytes()
        del self._models[model_id]
    
    def list_models(self) -> list[str]:
        """List all registered model IDs."""
        return list(self._models.keys())
    
    def get_stats(self) -> dict[str, Any]:
        """Get registry statistics."""
        return {
            "num_models": len(self._models),
            "max_models": self.max_models,
            "current_memory_bytes": self._current_memory,
            "max_memory_bytes": self.max_memory_bytes,
            "memory_utilization": self._current_memory / self.max_memory_bytes,
            "models": [
                {
                    "model_id": model_id,
                    "state": entry.state.value,
                    "memory_bytes": entry.model.get_memory_bytes(),
                    "access_count": entry.access_count,
                }
                for model_id, entry in self._models.items()
            ],
        }


class LoRAManager:
    """High-level manager for LoRA adapter serving.
    
    Handles per-request adapter selection and batched inference
    with multiple adapters.
    """
    
    def __init__(
        self,
        registry: LoRARegistry | None = None,
        default_config: LoRAConfig | None = None,
    ):
        """Initialize LoRA manager.
        
        Args:
            registry: LoRA model registry
            default_config: Default configuration for new adapters
        """
        self.registry = registry or LoRARegistry()
        self.default_config = default_config or LoRAConfig()
        self._active_adapters: dict[int, str] = {}  # request_id -> model_id
    
    def load_adapter(
        self,
        model_id: str,
        weights: dict[str, tuple[NDArray[np.float32], NDArray[np.float32]]],
        config: LoRAConfig | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LoRAModel:
        """Load a LoRA adapter.
        
        Args:
            model_id: Unique model identifier
            weights: Dict of module_name -> (lora_a, lora_b)
            config: Optional config override
            metadata: Optional metadata
            
        Returns:
            Loaded LoRA model
        """
        config = config or self.default_config
        model = LoRAModel(
            model_id=model_id,
            config=config,
            metadata=metadata or {},
        )
        
        for module_name, (lora_a, lora_b) in weights.items():
            layer = LoRALayerWeights(
                lora_a=lora_a.astype(np.float32),
                lora_b=lora_b.astype(np.float32),
                scaling=config.scaling,
                module_name=module_name,
                dropout=config.dropout,
            )
            model.add_layer(layer)
        
        if not self.registry.register(model):
            raise RuntimeError(f"Failed to register LoRA model {model_id}")
        
        return model
    
    def unload_adapter(self, model_id: str) -> bool:
        """Unload a LoRA adapter.
        
        Args:
            model_id: Model identifier
            
        Returns:
            True if unloaded
        """
        # Remove from active adapters
        self._active_adapters = {
            k: v for k, v in self._active_adapters.items() if v != model_id
        }
        return self.registry.unregister(model_id)
    
    def set_request_adapter(
        self,
        request_id: int,
        model_id: str | None,
    ):
        """Set adapter for a request.
        
        Args:
            request_id: Request identifier
            model_id: LoRA model ID (None to use base model)
        """
        if model_id is None:
            self._active_adapters.pop(request_id, None)
        else:
            self._active_adapters[request_id] = model_id
    
    def get_request_adapter(self, request_id: int) -> str | None:
        """Get adapter for a request."""
        return self._active_adapters.get(request_id)
    
    def clear_request(self, request_id: int):
        """Clear request's adapter binding."""
        self._active_adapters.pop(request_id, None)
    
    def apply_lora(
        self,
        request_id: int,
        module_name: str,
        base_output: NDArray[np.float32],
        x: NDArray[np.float32],
    ) -> NDArray[np.float32]:
        """Apply LoRA to base model output.
        
        Args:
            request_id: Request identifier
            module_name: Target module name
            base_output: Output from base model
            x: Input to the layer
            
        Returns:
            Output with LoRA applied
        """
        model_id = self._active_adapters.get(request_id)
        if model_id is None:
            return base_output
        
        model = self.registry.get(model_id)
        if model is None:
            return base_output
        
        lora_output = model.forward(module_name, x)
        if lora_output is None:
            return base_output
        
        return base_output + lora_output
    
    def batched_apply_lora(
        self,
        request_ids: list[int],
        module_name: str,
        base_outputs: NDArray[np.float32],
        inputs: NDArray[np.float32],
    ) -> NDArray[np.float32]:
        """Apply LoRA to batched outputs with different adapters.
        
        Args:
            request_ids: List of request IDs (one per batch item)
            module_name: Target module name
            base_outputs: Batched base outputs [batch, ...]
            inputs: Batched inputs [batch, ...]
            
        Returns:
            Outputs with per-request LoRA applied
        """
        outputs = base_outputs.copy()
        
        # Group by adapter
        adapter_groups: dict[str | None, list[int]] = {}
        for i, req_id in enumerate(request_ids):
            adapter_id = self._active_adapters.get(req_id)
            if adapter_id not in adapter_groups:
                adapter_groups[adapter_id] = []
            adapter_groups[adapter_id].append(i)
        
        # Apply each adapter to its group
        for adapter_id, indices in adapter_groups.items():
            if adapter_id is None:
                continue
            
            model = self.registry.get(adapter_id)
            if model is None:
                continue
            
            layer = model.get_layer(module_name)
            if layer is None:
                continue
            
            # Compute LoRA for this group
            batch_inputs = inputs[indices]
            lora_output = layer.forward(batch_inputs)
            outputs[indices] += lora_output
        
        return outputs
    
    def list_adapters(self) -> list[str]:
        """List all loaded adapters."""
        return self.registry.list_models()
    
    def get_adapter_info(self, model_id: str) -> dict[str, Any] | None:
        """Get adapter information."""
        model = self.registry.get(model_id)
        if model is None:
            return None
        
        return {
            "model_id": model.model_id,
            "config": {
                "rank": model.config.rank,
                "alpha": model.config.alpha,
                "dropout": model.config.dropout,
                "target_modules": list(model.config.target_modules),
            },
            "num_layers": len(model.layers),
            "num_parameters": model.num_parameters,
            "memory_bytes": model.get_memory_bytes(),
            "metadata": model.metadata,
        }
    
    def get_stats(self) -> dict[str, Any]:
        """Get manager statistics."""
        return {
            "registry": self.registry.get_stats(),
            "active_requests": len(self._active_adapters),
            "adapter_usage": dict(
                (adapter, sum(1 for v in self._active_adapters.values() if v == adapter))
                for adapter in set(self._active_adapters.values())
            ),
        }


# Factory functions

def create_lora_weights(
    in_features: int,
    out_features: int,
    rank: int,
    alpha: float = 16.0,
    module_name: str = "linear",
    init_method: str = "kaiming",
) -> LoRALayerWeights:
    """Create initialized LoRA layer weights.
    
    Args:
        in_features: Input dimension
        out_features: Output dimension
        rank: LoRA rank
        alpha: LoRA alpha
        module_name: Module name
        init_method: Initialization method ("kaiming", "gaussian", "zero")
        
    Returns:
        Initialized LoRA layer weights
    """
    if init_method == "kaiming":
        # Kaiming uniform for A, zeros for B
        bound = math.sqrt(6.0 / (rank + in_features))
        lora_a = np.random.uniform(-bound, bound, (rank, in_features)).astype(np.float32)
        lora_b = np.zeros((out_features, rank), dtype=np.float32)
    elif init_method == "gaussian":
        # Gaussian for A, zeros for B
        std = 1.0 / math.sqrt(rank)
        lora_a = np.random.normal(0, std, (rank, in_features)).astype(np.float32)
        lora_b = np.zeros((out_features, rank), dtype=np.float32)
    else:  # zero
        lora_a = np.zeros((rank, in_features), dtype=np.float32)
        lora_b = np.zeros((out_features, rank), dtype=np.float32)
    
    return LoRALayerWeights(
        lora_a=lora_a,
        lora_b=lora_b,
        scaling=alpha / rank,
        module_name=module_name,
    )


def create_lora_model(
    model_id: str,
    layer_dims: dict[str, tuple[int, int]],
    config: LoRAConfig | None = None,
) -> LoRAModel:
    """Create a LoRA model with initialized weights.
    
    Args:
        model_id: Model identifier
        layer_dims: Dict of module_name -> (in_features, out_features)
        config: LoRA configuration
        
    Returns:
        Initialized LoRA model
    """
    config = config or LoRAConfig()
    model = LoRAModel(model_id=model_id, config=config)
    
    for module_name, (in_features, out_features) in layer_dims.items():
        if module_name not in config.target_modules:
            continue
        
        layer = create_lora_weights(
            in_features=in_features,
            out_features=out_features,
            rank=config.rank,
            alpha=config.alpha,
            module_name=module_name,
        )
        model.add_layer(layer)
    
    return model


def merge_lora_weights(
    base_weights: dict[str, NDArray[np.float32]],
    lora_model: LoRAModel,
) -> dict[str, NDArray[np.float32]]:
    """Merge LoRA weights into base model weights.
    
    Args:
        base_weights: Dict of module_name -> weight matrix
        lora_model: LoRA model to merge
        
    Returns:
        Merged weights
    """
    merged = {}
    
    for module_name, base_weight in base_weights.items():
        lora_layer = lora_model.get_layer(module_name)
        if lora_layer is not None:
            merged[module_name] = lora_layer.merge_into_base(base_weight)
        else:
            merged[module_name] = base_weight.copy()
    
    return merged


def compute_effective_rank(
    lora_a: NDArray[np.float32],
    lora_b: NDArray[np.float32],
    threshold: float = 0.01,
) -> int:
    """Compute effective rank of LoRA matrices.
    
    Uses singular value decomposition to find the number of
    significant singular values.
    
    Args:
        lora_a: A matrix [rank, in_features]
        lora_b: B matrix [out_features, rank]
        threshold: Relative threshold for significance
        
    Returns:
        Effective rank
    """
    # Compute BA product
    product = lora_b @ lora_a
    
    # SVD
    _, s, _ = np.linalg.svd(product, full_matrices=False)
    
    # Count significant singular values
    max_s = s[0] if len(s) > 0 else 0
    if max_s == 0:
        return 0
    
    effective = int(np.sum(s / max_s > threshold))
    return effective
