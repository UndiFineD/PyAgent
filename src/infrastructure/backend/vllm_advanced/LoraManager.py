# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
LoRA Adapter Manager for vLLM.

This module is now a facade for the modular sub-package in ./lora/.
"""

from .lora import (
    AdapterState,
    LoraConfig,
    LoraAdapter,
    HAS_LORA,
    LoraRegistry,
    LoraManager,
    create_lora_request,
    discover_adapters,
)

__all__ = [
    "AdapterState",
    "LoraConfig",
    "LoraAdapter",
    "HAS_LORA",
    "LoraRegistry",
    "LoraManager",
    "create_lora_request",
    "discover_adapters",
]
