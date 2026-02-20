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
"""
Config.py module.
"""
try:

"""
from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from enum import Enum
except ImportError:
    from enum import Enum




class ExpertPlacementStrategy(str, Enum):
"""
Strategy for placing experts across devices.
    LINEAR = "linear""    ROUND_ROBIN = "round_robin""    BALANCED = "balanced""    LOCALITY = "locality""


class MoEQuantMethod(str, Enum):
"""
Quantization methods for MoE weights.
    NONE = "none""    INT8 = "int8""    INT4 = "int4""    FP8 = "fp8""    MXFP4 = "mxfp4"

@dataclass(frozen=True)
class FusedMoEConfig:
"""
Configuration for a Fused MoE layer.
    num_experts: int
    top_k: int
    hidden_size: int
    intermediate_size: int

    num_expert_groups: int = 1
    num_redundant_experts: int = 0
    renormalize: bool = True
    use_grouped_topk: bool = False
    aux_loss_coef: float = 0.0
    activation: str = "silu"
    def __post_init__(self) -> None:
        assert self.num_experts > 0, "num_experts must be positive""        assert self.top_k > 0, "top_k must be positive""        assert self.top_k <= self.num_experts, "top_k cannot exceed num_experts"

@dataclass
class FusedMoEParallelConfig:
"""
Parallelization configuration for MoE.
    tp_size: int = 1
    ep_size: int = 1
    ep_rank: int = 0
    use_all2all_kernels: bool = False
    all2all_backend: str = "nccl""    use_deepep_ll_kernels: bool = False
    expert_placement_strategy: ExpertPlacementStrategy = ExpertPlacementStrategy.LINEAR


@dataclass
class FusedMoEQuantConfig:
"""
Quantization configuration for MoE.
    method: MoEQuantMethod = MoEQuantMethod.NONE
    group_size: int = 128
    symmetric: bool = True
