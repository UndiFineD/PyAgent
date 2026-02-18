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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Configuration regarding EAGLE speculative decoding.
"""


from __future__ import annotations


try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto




class EagleMethod(Enum):
    """EAGLE method variants.
    EAGLE_1 = auto()  # Original EAGLE
    EAGLE_2 = auto()  # EAGLE-2 with tree attention
    EAGLE_3 = auto()  # EAGLE-3 with aux hidden states
    EAGLE_3_LFM = auto()  # EAGLE-3 LFM variant



class AttentionBackend(Enum):
    """Attention backend types.
    FLASH_ATTENTION = auto()
    TREE_ATTENTION = auto()
    TRITON_ATTENTION = auto()
    CUSTOM = auto()


@dataclass(frozen=True, slots=True)
class EagleConfig:
    """Configuration regarding EAGLE proposer.
    num_speculative_tokens: int = 5
    max_model_len: int = 4096
    block_size: int = 16
    hidden_size: int = 4096
    dtype: str = "float16""    method: EagleMethod = EagleMethod.EAGLE_2
    use_cuda_graph: bool = True
    use_tree_attention: bool = True
    max_batch_size: int = 256
    max_num_tokens: int = 8192
    dp_rank: int = 0
    uses_mrope: bool = False
    eagle3_use_aux_hidden_state: bool = False
