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
Speculative Async Output Pipeline (Phase 60).
Streams hybrid (draft + verified) tokens with support for low-latency rollbacks.
"""

import logging
import asyncio
import time
from typing import AsyncGenerator, List, Dict, Any, Union
from src.core.base.common.models.communication_models import (
    AsyncSpeculativeToken, PipelineCorrection
)

logger = logging.getLogger(__name__)

class SpeculativeAsyncPipeline:
    """
    Manages hybrid token generation streaming.
    Utilizes speculative swarm to 'guess' next tokens and correct them asynchronously.
    """

    def __init__(self, orchestrator: Any):
        self.orchestrator = orchestrator
        self.stream_history: List[str] = []

    async def generate_stream(
        self,
        task: str,
        draft_agent: str,
        target_agent: str
    ) -> AsyncGenerator[Union[AsyncSpeculativeToken, PipelineCorrection], None]:
        """
        Main entry point for speculative async streaming.
        """
        self.stream_history = []

        # 1. Trigger the speculative orchestrator
        # In a real async engine, we'd start the draft and yield its chunks as they arrive.
        # Here we simulate the hybrid flow.

        logger.info(f"Pipeline: Starting speculative stream for {task}")

        # Start drafting
        draft_task = asyncio.create_task(self.orchestrator.execute_speculative_task(
            task, draft_agent, target_agent
        ))

        # Simulate 'optimistic' yielding of a draft prefix if available immediately
        # (Usually from a fast look-up or small model)
        draft_chunks = ["Sure, ", "here ", "is ", "the ", "answer: "]
        for i, chunk in enumerate(draft_chunks):
            self.stream_history.append(chunk)
            yield AsyncSpeculativeToken(
                token=chunk,
                is_draft=True,
                sequence_index=i
            )
            await asyncio.sleep(0.01) # Low latency simulation

        # 2. Wait for orchestrator verification result
        outcome = await draft_task

        if outcome.accepted:
            # Continue streaming the remainder of the verified content
            # We skip the prefix we already optimistically sent
            verified_content = outcome.final_content
            # Simple simulation: just send the rest
            remaining = verified_content.replace("".join(draft_chunks), "", 1)
            for i, chunk in enumerate(remaining.split(" "), start=len(draft_chunks)):
                token = chunk + " "
                self.stream_history.append(token)
                yield AsyncSpeculativeToken(
                    token=token,
                    is_draft=False,
                    sequence_index=i
                )
        else:
            # 3. Handle Rollback
            logger.warning(f"Pipeline: Speculative mismatch detected. Issuing rollback.")

            # Simple logic: rollback everything and send the correct content
            # In production, we'd rollback only the divergent tokens.
            correction = PipelineCorrection(
                rollback_to_index=0,
                correct_tokens=outcome.final_content.split(" ")
            )
            yield correction

            # Update history
            self.stream_history = correction.correct_tokens

    def get_latency_report(self) -> Dict[str, Any]:
        """Calculates 'Perceptual Latency' vs 'Standard Latency'."""
        # Simulation
        return {
            "perceptual_ttft_ms": 12.0, # Time to first draft token
            "actual_ttft_ms": 45.0,     # Time to first verified token
            "reduction_factor": 3.75
        }
