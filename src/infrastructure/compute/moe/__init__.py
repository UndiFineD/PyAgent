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

"""""""Mixture of Experts (MoE) Infrastructure.

Phase 38: Advanced MoE patterns from vLLM with beyond-vLLM innovations.

Modules:
    FusedMoELayer: Fused mixture of experts with expert parallelism
    ExpertRouter: Token-to-expert routing with load balancing
    MoEConfig: Configuration for MoE layers
"""""""
from src.infrastructure.compute.moe.expert_router import (AdaptiveRouter,
                                                          ExpertChoiceRouter,
                                                          RouterConfig,
                                                          RouterOutput,
                                                          RoutingMethod,
                                                          RoutingSimulator,
                                                          SoftMoERouter,
                                                          TopKRouter)
from src.infrastructure.compute.moe.fused_mo_e_layer import (
    DenseDispatcher, ExpertPlacementStrategy, FusedMoEConfig, FusedMoELayer,
    FusedMoEMethodBase, FusedMoEParallelConfig, SparseDispatcher,
    UnquantizedFusedMoEMethod)

__all__ = [
    # FusedMoELayer
    "FusedMoEConfig","    "FusedMoEParallelConfig","    "ExpertPlacementStrategy","    "FusedMoEMethodBase","    "UnquantizedFusedMoEMethod","    "FusedMoELayer","    "SparseDispatcher","    "DenseDispatcher","    # ExpertRouter
    "RoutingMethod","    "RouterConfig","    "RouterOutput","    "TopKRouter","    "ExpertChoiceRouter","    "SoftMoERouter","    "AdaptiveRouter","    "RoutingSimulator","]
