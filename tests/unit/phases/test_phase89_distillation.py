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
Test Phase89 Distillation module.
"""

import numpy as np
from src.infrastructure.swarm.orchestration.swarm.context_distillation import ContextDistiller

def test_context_distillation():
    distiller = ContextDistiller(target_reduction=0.75) # 4x compression

    # Mock KV data: 128 tokens, 16 features
    kv_data = np.random.randn(128, 16)

    # Distill
    distilled, metadata = distiller.distill_shard(kv_data)

    assert distilled.shape == (32, 16)
    assert metadata["original_len"] == 128

    # Reconstruct
    reconstructed = distiller.reconstruct_placeholder(distilled, metadata)
    assert reconstructed.shape == (128, 16)

    # Most values will be zero, but exact indices should match original
    idx = metadata["indices"][0]
    assert np.allclose(reconstructed[idx], kv_data[idx])

    print("\n[Phase 89] Context distillation reduced 128 tokens to 32 tokens successfully.")

def test_attention_aware_distillation():
    distiller = ContextDistiller(target_reduction=0.5)

    kv_data = np.arange(10).reshape(10, 1) # tokens 0..9
    # Favor the last two tokens
    scores = np.array([0,0,0,0,0,0,0,0,10,10])

    distilled, metadata = distiller.distill_shard(kv_data, attention_scores=scores)

    # Should have 5 tokens
    assert 9 in metadata["indices"]
    assert 8 in metadata["indices"]
    print("[Phase 89] Attention-aware distillation correctly prioritized high-score tokens.")