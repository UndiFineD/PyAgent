# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Model Registry Package

"""
Model registry for architecture management.

This package provides:
- Model architecture registration
- Capability detection
- Lazy loading support
- VRAM estimation
"""

from .model_registry import (
    # Enums
    ModelCapability,
    ModelArchitecture,
    QuantizationType,

    # Data classes
    ModelConfig,
    ModelInfo,
    ArchitectureSpec,
    VRAMEstimate,

    # Core classes
    ModelRegistry,
    ArchitectureDetector,
    VRAMEstimator,

    # Utilities
    register_model,
    get_model_info,
    detect_architecture,
    estimate_vram,
)

__all__ = [
    # Enums
    "ModelCapability",
    "ModelArchitecture",
    "QuantizationType",

    # Data classes
    "ModelConfig",
    "ModelInfo",
    "ArchitectureSpec",
    "VRAMEstimate",

    # Core classes
    "ModelRegistry",
    "ArchitectureDetector",
    "VRAMEstimator",

    # Utilities
    "register_model",
    "get_model_info",
    "detect_architecture",
    "estimate_vram",
]
