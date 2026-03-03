#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
State Space Model (SSM) Infrastructure.

Phase 38: Mamba SSM patterns from vLLM with beyond-vLLM innovations.

Modules:
    MambaMixer: Mamba-1 selective state space model
    MambaUtils: Utilities for Mamba computation
"""

from src.infrastructure.compute.ssm.mamba_mixer import (CausalConv1d,
                                                        HybridMambaMixer,
                                                        Mamba2Mixer,
                                                        MambaConfig,
                                                        MambaMixer,
                                                        MambaOutput,
                                                        MambaState,
                                                        SelectiveScan)
from src.infrastructure.compute.ssm.mamba_utils import (
    apply_ssm_recurrence, compute_conv_state_shape, compute_ssm_state_shape,
    discretize_ssm, silu_activation, swish_activation)

__all__ = [
    # MambaMixer
    "MambaConfig",
    "MambaState",
    "MambaOutput",
    "MambaMixer",
    "Mamba2Mixer",
    "CausalConv1d",
    "SelectiveScan",
    "HybridMambaMixer",
    # MambaUtils
    "compute_ssm_state_shape",
    "compute_conv_state_shape",
    "discretize_ssm",
    "apply_ssm_recurrence",
    "silu_activation",
    "swish_activation",
]
