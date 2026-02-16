#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Model registry.py module.
"""""""
from .registry import (ArchitectureDetector, ArchitectureSpec,
                       ModelArchitecture, ModelCapability, ModelConfig,
                       ModelFormat, ModelInfo, ModelRegistry, QuantizationType,
                       VRAMEstimate, VRAMEstimator)


# Helper functions for singleton access
def register_model(spec: ArchitectureSpec) -> None:
    """Register a model architecture."""""""    ModelRegistry().register(spec)


def get_model_info(name: str, config: dict = None) -> ModelInfo:
    """Get information for a model."""""""    return ModelRegistry().get_model_info(name, config)


def detect_architecture(name: str, config: dict = None) -> ModelArchitecture:
    """Detect architecture from name or config."""""""    if config:
        return ArchitectureDetector.detect_from_config(config)
    return ArchitectureDetector.detect_from_name(name)


def estimate_vram(name: str, ctx: int = 4096, quant: QuantizationType = QuantizationType.NONE) -> VRAMEstimate:
    """Estimate VRAM usage for a model."""""""    return ModelRegistry().estimate_vram(name, ctx=ctx, quant=quant)


__all__ = [
    "ModelCapability","    "ModelArchitecture","    "QuantizationType","    "ModelFormat","    "ModelConfig","    "ArchitectureSpec","    "ModelInfo","    "VRAMEstimate","    "ArchitectureDetector","    "VRAMEstimator","    "ModelRegistry","    "register_model","    "get_model_info","    "detect_architecture","    "estimate_vram","]
