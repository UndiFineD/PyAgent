# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Configuration for EAGLE speculative decoding.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


class EagleMethod(Enum):
    """EAGLE method variants."""
    EAGLE_1 = auto()  # Original EAGLE
    EAGLE_2 = auto()  # EAGLE-2 with tree attention
    EAGLE_3 = auto()  # EAGLE-3 with aux hidden states
    EAGLE_3_LFM = auto()  # EAGLE-3 LFM variant


class AttentionBackend(Enum):
    """Attention backend types."""
    FLASH_ATTENTION = auto()
    TREE_ATTENTION = auto()
    TRITON_ATTENTION = auto()
    CUSTOM = auto()


@dataclass(frozen=True, slots=True)
class EagleConfig:
    """Configuration for EAGLE proposer."""
    num_speculative_tokens: int = 5
    max_model_len: int = 4096
    block_size: int = 16
    hidden_size: int = 4096
    dtype: str = "float16"
    method: EagleMethod = EagleMethod.EAGLE_2
    use_cuda_graph: bool = True
    use_tree_attention: bool = True
    max_batch_size: int = 256
    max_num_tokens: int = 8192
    dp_rank: int = 0
    uses_mrope: bool = False
    eagle3_use_aux_hidden_state: bool = False
