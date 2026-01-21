# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Models and configuration for LoRA adapters.
"""

import hashlib
import logging
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

# Check vLLM availability
try:
    from vllm.lora.request import LoRARequest
    HAS_LORA = True
except ImportError:
    HAS_LORA = False
    LoRARequest = None

logger = logging.getLogger(__name__)


class AdapterState(Enum):
    """State of a LoRA adapter."""
    UNLOADED = auto()
    LOADING = auto()
    LOADED = auto()
    ACTIVE = auto()
    ERROR = auto()


@dataclass
class LoraConfig:
    """Configuration for LoRA loading and management."""

    # Model settings
    max_lora_rank: int = 64
    max_loras: int = 4  # Max concurrent adapters
    max_cpu_loras: Optional[int] = None

    # Memory management
    lora_dtype: str = "auto"
    enable_lora_bias: bool = False

    # Caching
    cache_enabled: bool = True
    cache_max_adapters: int = 10

    # Loading behavior
    lazy_load: bool = True
    preload_adapters: List[str] = field(default_factory=list)


@dataclass
class LoraAdapter:
    """
    Represents a LoRA adapter.
    """

    adapter_id: int
    name: str
    path: str
    state: AdapterState = AdapterState.UNLOADED

    # Metadata
    base_model: Optional[str] = None
    rank: Optional[int] = None
    alpha: Optional[float] = None
    target_modules: List[str] = field(default_factory=list)

    # Stats
    load_count: int = 0
    last_used: Optional[float] = None
    load_time_ms: Optional[float] = None

    # Computed
    _hash: Optional[str] = None

    @property
    def hash(self) -> str:
        """Get unique hash for this adapter."""
        if self._hash is None:
            content = f"{self.name}:{self.path}:{self.rank}:{self.alpha}"
            self._hash = hashlib.md5(content.encode()).hexdigest()[:12]
        return self._hash

    def to_lora_request(self) -> Optional[Any]:
        """Convert to vLLM LoRARequest."""
        if not HAS_LORA:
            raise RuntimeError("LoRA support not available")

        return LoRARequest(
            lora_name=self.name,
            lora_int_id=self.adapter_id,
            lora_path=self.path,
        )

    def mark_used(self) -> None:
        """Mark adapter as recently used."""
        self.last_used = time.time()
        self.load_count += 1
