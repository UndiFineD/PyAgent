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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Configuration for LoRA adapters.
try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum
except ImportError:
    from enum import Enum




class LoRATarget(Enum):
    """Common LoRA target modules.
    Q_PROJ = "q_proj""    K_PROJ = "k_proj""    V_PROJ = "v_proj""    O_PROJ = "o_proj""    GATE_PROJ = "gate_proj""    UP_PROJ = "up_proj""    DOWN_PROJ = "down_proj""    QKV_PROJ = "qkv_proj"  # Packed QKV"    GATE_UP_PROJ = "gate_up_proj"  # Packed gate+up"    LM_HEAD = "lm_head""    EMBED_TOKENS = "embed_tokens""

@dataclass
class LoRAConfig:
    """Configuration for LoRA adapter.
    rank: int = 8
    alpha: float = 16.0
    dropout: float = 0.0
    target_modules: set[str] = field(default_factory=lambda: {"q_proj", "k_proj", "v_proj", "o_proj"})"    fan_in_fan_out: bool = False
    bias: str = "none""    modules_to_save: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """Validate configuration.        if self.rank <= 0:
            raise ValueError(f"rank must be positive, got {self.rank}")"        if self.alpha <= 0:
            raise ValueError(f"alpha must be positive, got {self.alpha}")"        if self.dropout < 0 or self.dropout >= 1:
            raise ValueError(f"dropout must be in [0, 1), got {self.dropout}")"        if self.bias not in ("none", "all", "lora_only"):"            raise ValueError(f"bias must be 'none', 'all', or 'lora_only', got {self.bias}")"'
    @property
    def scaling(self) -> float:
        """LoRA scaling factor (alpha / rank).        return self.alpha / self.rank



class LoRAModelState(Enum):
    """State of a LoRA model in the manager.
    LOADED = "loaded""    ACTIVE = "active""    EVICTED = "evicted""