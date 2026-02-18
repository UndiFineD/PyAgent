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

import torch
import torch.nn as nn


class STEMScalingModule(nn.Module):
    """
    Dynamic Embedding Expansion for 1M+ contexts (arXiv:2601.10639).
    Activates additional transform layers as sequence length grows.
    """
    def __init__(self, d_model: int):
        super().__init__()
        self.base_transform = nn.Identity()
        self.aux_module_128k = nn.Linear(d_model, d_model)
        self.aux_module_1m = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor, seq_len: int) -> torch.Tensor:
        # Base representation
        h = self.base_transform(x)

        # Incremental parameter activation
        if seq_len > 128000:
            print("Activating 128k Auxiliary Embedding Module")
            h = h + 0.1 * self.aux_module_128k(h)

        if seq_len > 1000000:
            print("Activating 1M Auxiliary Embedding Module")
            h = h + 0.1 * self.aux_module_1m(h)

        return h

if __name__ == "__main__":
    module = STEMScalingModule(4096)
    x = torch.randn(1, 1, 4096)

    out_short = module(x, 1024)
    out_long = module(x, 2000000)

    print(f"Short context sum: {out_short.sum().item()}")
    print(f"1M+ context sum: {out_long.sum().item()}")
