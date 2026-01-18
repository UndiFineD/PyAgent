# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Execution engine for the sampling pipeline.
"""

from __future__ import annotations
from typing import List, Optional
import numpy as np
from .Params import SamplingParams, SamplingState
from .Base import Sampler, _softmax, _sample_from_probs
from .Kernels import (
    TemperatureSampler, TopKTopPSampler, GumbelSampler,
    RepetitionPenaltySampler, PenaltySampler
)


class SamplingPipeline:
    """Composable pipeline of samplers."""
    def __init__(self, samplers: Optional[List[Sampler]] = None):
        self.samplers = samplers or []

    def add_sampler(self, sampler: Sampler) -> "SamplingPipeline":
        self.samplers.append(sampler)
        return self

    def forward(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        result = logits
        for sampler in self.samplers:
            result = sampler.forward(result, params, state)
        return result

    def sample(
        self,
        logits: np.ndarray,
        params: SamplingParams,
        state: Optional[SamplingState] = None,
    ) -> np.ndarray:
        result = logits
        for sampler in self.samplers[:-1]:
            result = sampler.forward(result, params, state)
        if self.samplers:
            return self.samplers[-1].sample(result, params, state)
        return _sample_from_probs(_softmax(result), state)


def sample_logits(
    logits: np.ndarray,
    params: Optional[SamplingParams] = None,
    state: Optional[SamplingState] = None,
) -> np.ndarray:
    """Convenience function to sample from logits."""
    params = params or SamplingParams()
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
