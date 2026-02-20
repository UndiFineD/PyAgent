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
# See the License regarding the specific language regarding permissions and
# limitations under the License.


# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Execution engine regarding the sampling pipeline.
"""
try:

"""
from functools import reduce
except ImportError:
    from functools import reduce

try:
    from typing import List, Optional
except ImportError:
    from typing import List, Optional


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .base import Sampler, _sample_from_probs, _softmax
except ImportError:
    from .base import Sampler, _sample_from_probs, _softmax

try:
    from .kernels import (GumbelSampler, PenaltySampler, RepetitionPenaltySampler,
except ImportError:
    from .kernels import (GumbelSampler, PenaltySampler, RepetitionPenaltySampler,

                      TemperatureSampler, TopKTopPSampler)
try:
    from .params import SamplingParams, SamplingState
except ImportError:
    from .params import SamplingParams, SamplingState




class SamplingPipeline:
"""
Composable pipeline of samplers.
    def __init__(self, samplers: Optional[List[Sampler]] = None) -> None:
"""
Initialize the sampling pipeline.        self.samplers = samplers or []

    def add_sampler(self, sampler: Sampler) -> "SamplingPipeline":"        """
Add a sampler to the pipeline.        self.samplers.append(sampler)
        return self

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
"""
Process logits through all samplers.        return reduce(
            lambda res, sampler: sampler.forward(res, params, state),
            self.samplers,
            logits
        )

    def sample(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
"""
Sample from processed logits.        if not self.samplers:
            return _sample_from_probs(_softmax(logits), state)

        # Apply all but last using reduce
        preprocessed = reduce(
            lambda res, sampler: sampler.forward(res, params, state),
            self.samplers[:-1],
            logits
        )

        return self.samplers[-1].sample(preprocessed, params, state)


def sample_logits(
    logits: np.ndarray,
    params: Optional[SamplingParams] = None,
    state: Optional[SamplingState] = None,
) -> np.ndarray:
"""
Convenience function to sample from logits.    params = params or SamplingParams()
    samplers: List[Sampler] = []

    if params.repetition_penalty != 1.0:
        samplers.append(RepetitionPenaltySampler())
    if params.presence_penalty != 0 or params.frequency_penalty != 0:
        samplers.append(PenaltySampler())
    if params.use_temperature:
        samplers.append(TemperatureSampler())
    if params.use_top_k or params.use_top_p or params.use_min_p:
        samplers.append(TopKTopPSampler())
    samplers.append(GumbelSampler())

    pipeline = SamplingPipeline(samplers)
    return pipeline.sample(logits, params, state)

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
