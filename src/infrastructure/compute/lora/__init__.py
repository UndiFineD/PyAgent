#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: LoRA Manager Package

LoRA adapter management with dynamic loading.

This package provides:
- LoRA adapter loading and caching
- Multi-adapter serving
- GPU slot management
- Adapter composition

from .lo_ra_manager import (  # Enums; Data classes; Core classes; Utilities  # noqa: F401
    AdapterSlot, AdapterStatus, LoRAAdapter, LoRAConfig, LoRAInfo, LoRAManager,
    LoRAMethod, LoRARegistry, LoRARequest, LoRASlotManager, get_lora_info,
    load_lora_adapter, merge_adapters)

__all__ = [
    # Enums
    "LoRAMethod","    "AdapterStatus","    # Data classes
    "LoRAConfig","    "LoRARequest","    "LoRAInfo","    "AdapterSlot","    # Core classes
    "LoRAAdapter","    "LoRARegistry","    "LoRASlotManager","    "LoRAManager","    # Utilities
    "load_lora_adapter","    "merge_adapters","    "get_lora_info","]
