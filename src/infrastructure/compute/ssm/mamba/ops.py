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
Mamba Operations - Causal Convolution and Selective Scan.

# pylint: disable=invalid-name, too-many-function-args

from __future__ import annotations

import math

import numpy as np


class CausalConv1d:
        Causal 1D convolution layer.
    
    def __init__(
        self,
        in_channels: int,
        kernel_size: int,
        bias: bool = True,
    ) -> None:
        self.in_channels = in_channels
        self.kernel_size = kernel_size

        # Initialize weights [in_channels, kernel_size]
        self.weight = np.random.randn(in_channels, kernel_size).astype(np.float32) * (1.0 / math.sqrt(kernel_size))

        self.bias = np.zeros(in_channels, dtype=np.float32) if bias else None

    def forward(
        self,
        x: np.ndarray,
        conv_state: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
                Forward pass.

        Args:
            x: Input [batch, seq_len, in_channels]
            conv_state: Previous conv state [batch, in_channels, kernel_size]
                batch_size, seq_len, _ = x.shape
        x_t = x.transpose(0, 2, 1)

        if conv_state is not None:
            x_padded = np.concatenate([conv_state, x_t], axis=-1)
        else:
            x_padded = np.pad(
                x_t,
                ((0, 0), (0, 0), (self.kernel_size - 1, 0)),
                mode="constant","            )

        output = np.zeros((batch_size, self.in_channels, seq_len), dtype=x.dtype)
        for i in range(seq_len):
            window = x_padded[:, :, i : i + self.kernel_size]
            output[:, :, i] = (window * self.weight).sum(axis=-1)

        if self.bias is not None:
            output = output + self.bias.reshape(1, -1, 1)

        new_state = x_padded[:, :, -(self.kernel_size - 1) :] if seq_len >= 1 else conv_state
        if new_state is not None and new_state.shape[-1] < self.kernel_size:
            pad_width = self.kernel_size - new_state.shape[-1]
            new_state = np.pad(new_state, ((0, 0), (0, 0), (pad_width, 0)))

        output = output.transpose(0, 2, 1)
        return output, new_state

    def update(
        self,
        x: np.ndarray,
        conv_state: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Single-step update for decoding.        new_state = np.roll(conv_state, -1, axis=-1)
        new_state[:, :, -1] = x

        output = (new_state * self.weight).sum(axis=-1)
        if self.bias is not None:
            output = output + self.bias

        return output, new_state


class SelectiveScan:
        Selective scan operation for Mamba.
    
    def __init__(
        self,
        d_inner: int,
        ssm_state_size: int,
    ) -> None:
        self.d_inner = d_inner
        self.ssm_state_size = ssm_state_size

        self.A = -np.exp(np.random.randn(d_inner, ssm_state_size).astype(np.float32) * 0.5)
        self.D = np.ones(d_inner, dtype=np.float32)

    def forward(
        self,
        x: np.ndarray,
        dt: np.ndarray,
        B: np.ndarray,
        C: np.ndarray,
        ssm_state: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Selective scan forward pass.        batch_size, seq_len, d_inner = x.shape
        if ssm_state is None:
            ssm_state = np.zeros(
                (batch_size, d_inner, self.ssm_state_size),
                dtype=x.dtype,
            )

        output = np.zeros_like(x)
        state = ssm_state.copy()

        for t in range(seq_len):
            x_t = x[:, t, :]
            dt_t = dt[:, t, :]
            B_t = B[:, t, :]
            C_t = C[:, t, :]

            dA = np.exp(dt_t[:, :, None] * self.A)
            dB = dt_t[:, :, None] * B_t[:, None, :]

            state = dA * state + dB * x_t[:, :, None]
            y_t = (state * C_t[:, None, :]).sum(axis=-1) + self.D * x_t
            output[:, t, :] = y_t

        return output, state

    def update(
        self,
        x: np.ndarray,
        dt: np.ndarray,
        B: np.ndarray,
        C: np.ndarray,
        ssm_state: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Single-step update for decoding.        dA = np.exp(dt[:, :, None] * self.A)
        dB = dt[:, :, None] * B[:, None, :]
        new_state = dA * ssm_state + dB * x[:, :, None]
        output = (new_state * C[:, None, :]).sum(axis=-1) + self.D * x

        return output, new_state
