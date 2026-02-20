#!/usr/bin/env python3
from __future__ import annotations


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
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Data models for batch orchestration.
"""

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto

try:
    from typing import Any, List, Optional, Tuple
except ImportError:
    from typing import Any, List, Optional, Tuple


try:
    import numpy
except ImportError:
    import numpy
 as np



class MoveDirectionality(Enum):
    """Direction of request movement in batch.
    SWAP = auto()  # Bidirectional swap
    MOVE_TO = auto()  # Unidirectional move


@dataclass
class CachedRequestState:
        Per-request state cache matching vLLM's CachedRequestState.'    
    req_id: str
    prompt_token_ids: Optional[List[int]] = None
    mm_features: List[dict[str, Any]] = field(default_factory=list)
    sampling_params: Optional[dict[str, Any]] = None
    generator: Any = None  # torch.Generator

    # Block allocation
    block_ids: tuple[List[int], ...] = field(default_factory=lambda: ([],))
    num_computed_tokens: int = 0
    output_token_ids: List[int] = field(default_factory=list)

    # Position tracking
    mrope_positions: Any = None  # torch.Tensor
    mrope_position_delta: Optional[int] = None

    # LoRA
    lora_request: Any = None
    prompt_embeds: Any = None  # torch.Tensor

    # Speculative decoding
    prev_num_draft_len: int = 0

    # Pooling
    pooling_params: Optional[dict[str, Any]] = None
    pooling_states: Optional[dict[str, Any]] = None

    @property
    def num_tokens(self) -> int:
        """Total number of tokens (prompt + generated).        prompt_len = len(self.prompt_token_ids) if self.prompt_token_ids else 0
        return prompt_len + len(self.output_token_ids)


@dataclass
class BatchUpdateBuilder:
        Tracks request movements within a batch for logits processors.
    
    moved: List[Tuple[int, int, MoveDirectionality]] = field(default_factory=list)
    added: List[Tuple[str, int]] = field(default_factory=list)  # (req_id, index)
    removed: List[Tuple[str, int]] = field(default_factory=list)  # (req_id, index)

    def reset(self) -> None:
        """Reset for new step.        self.moved.clear()
        self.added.clear()
        self.removed.clear()

    def record_swap(self, i1: int, i2: int) -> None:
        """Record a bidirectional swap.        self.moved.append((i1, i2, MoveDirectionality.SWAP))

    def record_add(self, req_id: str, index: int) -> None:
        """Record a request addition.        self.added.append((req_id, index))

    def record_remove(self, req_id: str, index: int) -> None:
        """Record a request removal.        self.removed.append((req_id, index))


@dataclass
class SamplingMetadata:
        GPU-resident sampling parameters for a batch.
    
    temperature: Any  # torch.Tensor | None
    top_p: Any  # torch.Tensor | None
    top_k: Any  # torch.Tensor | None
    frequency_penalties: Any  # torch.Tensor | None
    presence_penalties: Any  # torch.Tensor | None
    repetition_penalties: Any  # torch.Tensor | None
    min_p: Any  # torch.Tensor | None

    # Flags for optimization
    all_greedy: bool = False
    no_top_p: bool = True
    no_top_k: bool = True
    no_penalties: bool = True


@dataclass
class InputBatch:
        Complete batch representation for model execution.
    
    req_ids: List[str]
    num_reqs: int
    idx_mapping: Any  # torch.Tensor - request index to batch position
    idx_mapping_np: np.ndarray
    expanded_idx_mapping: Any  # torch.Tensor - token-level expansion
    num_scheduled_tokens: np.ndarray
    num_tokens: int
    num_tokens_after_padding: int
    num_draft_tokens: int
    query_start_loc: Any  # torch.Tensor
    query_start_loc_np: np.ndarray
    seq_lens: Any  # torch.Tensor
    input_ids: Any  # torch.Tensor
    positions: Any  # torch.Tensor
    mrope_positions: Optional[Any]  # torch.Tensor | None
    attn_metadata: Optional[dict[str, Any]]
    logits_indices: Any  # torch.Tensor
    cu_num_logits: Any  # torch.Tensor
    cu_num_logits_np: np.ndarray
    sampling_metadata: Optional[SamplingMetadata] = None
