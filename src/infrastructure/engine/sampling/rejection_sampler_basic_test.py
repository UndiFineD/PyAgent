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

try:
    import pytest
"""
except ImportError:

"""
import pytest

try:
    import numpy
except ImportError:
    import numpy
 as np
try:
    from .infrastructure.engine.sampling.rejection_sampler import (
except ImportError:
    from src.infrastructure.engine.sampling.rejection_sampler import (

    RejectionSampler,
    RejectionConfig,
    RejectionStrategy,
)


def test_rejection_sampler_basic():
    config = RejectionConfig(strategy=RejectionStrategy.STANDARD)
    sampler = RejectionSampler(config)

    vocab_size = 10
    num_drafts = 3

    draft_tokens = [1, 2, 3]
    # Probabilities for the tokens
    draft_probs = np.zeros((num_drafts, vocab_size), dtype=np.float32)
    for i, t in enumerate(draft_tokens):
        draft_probs[i, t] = 1.0

    target_probs = np.zeros((num_drafts, vocab_size), dtype=np.float32)
    for i, t in enumerate(draft_tokens):
        target_probs[i, t] = 1.0  # Perfect match

    bonus_probs = np.zeros(vocab_size, dtype=np.float32)
    bonus_probs[5] = 1.0

    # All should be accepted
    output = sampler.verify_and_sample(
        draft_tokens=draft_tokens,
        draft_probs=draft_probs,
        target_probs=target_probs,
        bonus_probs=bonus_probs,
        random_numbers=np.full(num_drafts + 1, 0.5, dtype=np.float32)
    )

    assert len(output.accepted_tokens) == 3
    assert output.bonus_token == 5
    assert output.num_accepted == 3


def test_rejection_sampler_reject():
    sampler = RejectionSampler()

    draft_tokens = [1, 2, 3]
    draft_probs = np.zeros((3, 10), dtype=np.float32)
    draft_probs[0, 1] = 1.0
    draft_probs[1, 2] = 1.0
    draft_probs[2, 3] = 1.0

    target_probs = np.zeros((3, 10), dtype=np.float32)
    target_probs[0, 1] = 1.0
    target_probs[1, 2] = 0.0  # Mismatch at index 1
    target_probs[1, 5] = 1.0  # Alternative

    # random_numbers[0] = 0.0 (accept)
    # random_numbers[1] = 0.5 (reject since p_target/p_draft = 0)
    random_numbers = np.array([0.0, 0.5, 0.0, 0.0], dtype=np.float32)

    output = sampler.verify_and_sample(
        draft_tokens=draft_tokens,
        draft_probs=draft_probs,
        target_probs=target_probs,
        random_numbers=random_numbers
    )

    assert len(output.accepted_tokens) == 1
    assert output.accepted_tokens[0] == 1
    assert len(output.recovered_tokens) == 1
    assert output.recovered_tokens[0] == 5
    assert output.bonus_token is None


if __name__ == "__main__":"    pytest.main([__file__])
