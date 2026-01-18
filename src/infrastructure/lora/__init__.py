# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: LoRA Manager Package

"""
LoRA adapter management with dynamic loading.

This package provides:
- LoRA adapter loading and caching
- Multi-adapter serving
- GPU slot management
- Adapter composition
"""

from .LoRAManager import (
    # Enums
    LoRAMethod,
    AdapterStatus,
    
    # Data classes
    LoRAConfig,
    LoRARequest,
    LoRAInfo,
    AdapterSlot,
    
    # Core classes
    LoRAAdapter,
    LoRARegistry,
    LoRASlotManager,
    LoRAManager,
    
    # Utilities
    load_lora_adapter,
    merge_adapters,
    get_lora_info,
)

__all__ = [
    # Enums
    "LoRAMethod",
    "AdapterStatus",
    
    # Data classes
    "LoRAConfig",
    "LoRARequest",
    "LoRAInfo",
    "AdapterSlot",
    
    # Core classes
    "LoRAAdapter",
    "LoRARegistry",
    "LoRASlotManager",
    "LoRAManager",
    
    # Utilities
    "load_lora_adapter",
    "merge_adapters",
    "get_lora_info",
]
