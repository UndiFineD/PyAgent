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

# SPDX-License-Identifier: Apache-2.0
"""
Mamba Configuration and State Classes.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import NamedTuple

import numpy as np


@dataclass(frozen=True)
class MambaConfig:  # pylint: disable=too-many-instance-attributes
    """
    Configuration for Mamba mixer.
    """

    hidden_size: int
    ssm_state_size: int = 16  # N in Mamba paper
    conv_kernel_size: int = 4  # d_conv
    intermediate_size: int | None = None  # d_inner, defaults to 2*hidden_size
    time_step_rank: int | None = None  # dt_rank, defaults to ceil(hidden_size/16)

    # Activation
    activation: str = "silu"

    # Normalization
    use_rms_norm: bool = True
    rms_norm_eps: float = 1e-5
    rms_norm_has_weight: bool = True

    # Bias
    use_conv_bias: bool = True
    use_bias: bool = False

    def __post_init__(self) -> None:
        if self.hidden_size <= 0:
            raise ValueError(f"hidden_size must be > 0, got {self.hidden_size}")
        if self.ssm_state_size <= 0:
            raise ValueError(f"ssm_state_size must be > 0, got {self.ssm_state_size}")
        if self.conv_kernel_size <= 0:
            raise ValueError(f"conv_kernel_size must be > 0, got {self.conv_kernel_size}")

    @property
    def d_inner(self) -> int:
        """Get intermediate size."""
        return self.intermediate_size or (2 * self.hidden_size)

    @property
    def dt_rank(self) -> int:
        """Get time step rank."""
        return self.time_step_rank or math.ceil(self.hidden_size / 16)


@dataclass
class MambaState:
    """
    State for Mamba recurrence.
    """

    conv_state: np.ndarray  # [batch, d_inner, d_conv]
    ssm_state: np.ndarray  # [batch, d_inner, ssm_state_size]

    @classmethod
    def zeros(
        cls,
        batch_size: int,
        config: MambaConfig,
        dtype: np.dtype = np.float32,
    ) -> "MambaState":
        """Create zero-initialized state."""
        return cls(
            conv_state=np.zeros(
                (batch_size, config.d_inner, config.conv_kernel_size),
                dtype=dtype,
            ),
            ssm_state=np.zeros(
                (batch_size, config.d_inner, config.ssm_state_size),
                dtype=dtype,
            ),
        )

    def clone(self) -> "MambaState":
        """Clone state."""
        return MambaState(
            conv_state=self.conv_state.copy(),
            ssm_state=self.ssm_state.copy(),
        )


class MambaOutput(NamedTuple):
    """Output from Mamba forward pass."""

    output: np.ndarray  # [batch, seq_len, hidden_size]
    state: MambaState  # Updated state
