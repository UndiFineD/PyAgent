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
# Phase 41: Model Registry Package

"""
Model registry for architecture management.

This package provides:
- Model architecture registration
- Capability detection
- Lazy loading support
- VRAM estimation
"""

from .model_registry import (  # Enums; Data classes; Core classes; Utilities  # noqa: F401
    ArchitectureDetector, ArchitectureSpec, ModelArchitecture, ModelCapability,
    ModelConfig, ModelInfo, ModelRegistry, QuantizationType, VRAMEstimate,
    VRAMEstimator, detect_architecture, estimate_vram, get_model_info,
    register_model)

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
