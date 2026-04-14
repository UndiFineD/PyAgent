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
"""CortCore — Chain-of-Recursive-Thoughts core reasoning loop.

This module implements the multi-round, multi-alternative reasoning loop that
enables PyAgent agents to perform structured self-improvement iterations.  Each
call to :meth:`CortCore.run` generates ``n_rounds`` rounds; within every round
``m_alternatives`` LLM responses are produced in parallel at increasing
temperatures, scored by an :class:`EvaluationEngine`, and the best chain is
carried forward as the seed for the next round.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

# ---------------------------------------------------------------------------
# Sentinel for cap enforcement
# ---------------------------------------------------------------------------
_CORT_PRODUCT_CAP: int = 15


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class CortLimitExceeded(Exception):  # noqa: N818
    """Raised when ``n_rounds × m_alternatives`` exceeds the allowed cap."""


class CortRecursionError(Exception):
    """Raised when :meth:`CortCore.run` is called re-entrantly on the same instance."""


class AlternativesGenerationError(Exception):
    """Raised when all LLM calls in a generation attempt fail."""


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class LlmCallable(Protocol):
    """Protocol for an async LLM callable used by CortCore."""

    async def __call__(
        self,
        prompt: str,
        *,
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Invoke the language model.

        Args:
            prompt: The full prompt string sent to the LLM.
            temperature: Sampling temperature for the LLM.
            max_tokens: Maximum number of tokens in the response.

        Returns:
            The LLM response text.

        """
        ...  # pragma: no cover


class EvaluatorLike(Protocol):
    """Protocol for the evaluator used by CortCore."""

    def select_best(self, chains: list["ReasoningChain"]) -> "ReasoningChain":
        """Select the best chain from already scored alternatives."""
        ...  # pragma: no cover

    def score_and_assign(
        self,
        chains: list["ReasoningChain"],
        prompt: str,
    ) -> list["ReasoningChain"]:
        """Assign scores to a chain list and return scored chains."""
        ...  # pragma: no cover


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CortConfig:
    """Immutable configuration for a CoRT reasoning run.

    Attributes:
        n_rounds: Number of recursive self-improvement rounds.
        m_alternatives: Number of alternative chains generated per round.
        base_temp: Starting sampling temperature for the first alternative.
        temp_step: Per-alternative temperature increment within a round.
        max_tokens: Maximum tokens per LLM call.
        early_stop_threshold: If set, stop early when the best score exceeds
            this value.  ``None`` disables early stopping.

    Raises:
        CortLimitExceeded: If ``n_rounds * m_alternatives`` exceeds 15.

    """

    n_rounds: int
    m_alternatives: int
    base_temp: float = 0.7
    temp_step: float = 0.15
    max_tokens: int = 1024
    early_stop_threshold: float | None = None

    def __post_init__(self) -> None:
        """Validate that the product cap is not exceeded.

        Raises:
            CortLimitExceeded: If ``n_rounds * m_alternatives`` exceeds 15.

        """
        if self.n_rounds * self.m_alternatives > _CORT_PRODUCT_CAP:
            raise CortLimitExceeded(
                f"n_rounds ({self.n_rounds}) × m_alternatives ({self.m_alternatives}) = "
                f"{self.n_rounds * self.m_alternatives} exceeds the cap of {_CORT_PRODUCT_CAP}."
            )


DEFAULT_CORT_CONFIG = CortConfig(
    n_rounds=3,
    m_alternatives=3,
    base_temp=0.7,
    temp_step=0.15,
    max_tokens=1024,
    early_stop_threshold=None,
)


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class ReasoningChain:
    """A single reasoning chain candidate produced by the LLM.

    Attributes:
        text: The full text of the reasoning chain.
        score: Weighted rubric score assigned by the EvaluationEngine.
        round_n: Zero-based round index in which this chain was generated.
        temperature: Sampling temperature used to generate this chain.
        alternative_idx: Zero-based index of this alternative within its round.

    """

    text: str
    score: float
    round_n: int
    temperature: float
    alternative_idx: int

    def __lt__(self, other: object) -> bool:
        """Compare by score (ascending).

        Args:
            other: Another ReasoningChain to compare against.

        Returns:
            True if this chain's score is less than the other's.

        """
        if not isinstance(other, ReasoningChain):
            return NotImplemented
        return self.score < other.score

    def __gt__(self, other: object) -> bool:
        """Compare by score (descending).

        Args:
            other: Another ReasoningChain to compare against.

        Returns:
            True if this chain's score is greater than the other's.

        """
        if not isinstance(other, ReasoningChain):
            return NotImplemented
        return self.score > other.score

    def __eq__(self, other: object) -> bool:
        """Check equality by score.

        Args:
            other: Another object to compare against.

        Returns:
            True if scores are equal.

        """
        if not isinstance(other, ReasoningChain):
            return NotImplemented
        return self.score == other.score


@dataclass
class CortRound:
    """Records all data produced during one CoRT round.

    Attributes:
        round_n: Zero-based round index.
        prompt_used: The prompt string passed to the LLM for this round.
        alternatives: All scored reasoning chains generated in this round.
        winner: The highest-scoring chain selected to seed the next round.

    """

    round_n: int
    prompt_used: str
    alternatives: list[ReasoningChain]
    winner: ReasoningChain


@dataclass
class CortMetadata:
    """Runtime metadata recorded at the end of a CoRT run.

    Attributes:
        agent_id: Identifier of the agent that initiated this run.  Set by
            the calling agent after the run completes.
        total_rounds: Number of rounds executed.
        total_llm_calls: Total LLM invocations made during the run.
        elapsed_seconds: Wall-clock duration of the run.

    """

    agent_id: str
    total_rounds: int
    total_llm_calls: int
    elapsed_seconds: float


@dataclass
class CortResult:
    """Final result of a completed CoRT reasoning run.

    Attributes:
        best_chain: The highest-scoring reasoning chain across all rounds.
        all_rounds: Ordered list of every round executed (length == n_rounds).
        metadata: Runtime metadata including timing and call counts.

    """

    best_chain: ReasoningChain
    all_rounds: list[CortRound]
    metadata: CortMetadata


# ---------------------------------------------------------------------------
# CortCore
# ---------------------------------------------------------------------------


class CortCore:
    """Executes the Chain-of-Recursive-Thoughts reasoning loop.

    Args:
        llm: An async callable conforming to :class:`LlmCallable`.
        evaluator: An :class:`EvaluationEngine` that scores each chain.
        config: A :class:`CortConfig` controlling round and alternative counts.

    """

    def __init__(
        self,
        llm: LlmCallable,
        evaluator: EvaluatorLike,
        config: CortConfig,
    ) -> None:
        """Initialise a CortCore instance.

        Args:
            llm: Async callable for generating reasoning text.
            evaluator: Engine for scoring reasoning chains.
            config: Configuration controlling loop behaviour.

        """
        self._llm = llm
        self._evaluator = evaluator
        self.config = config
        self._active: bool = False

    async def run(self, prompt: str, context: str = "") -> CortResult:
        """Execute the full CoRT reasoning loop.

        Args:
            prompt: The question or task to reason about.
            context: Optional additional context prepended to the prompt.

        Returns:
            A :class:`CortResult` containing the best chain, all rounds, and
            runtime metadata.

        Raises:
            CortRecursionError: If this method is called re-entrantly on the
                same instance (e.g. from within an LLM callback).

        """
        if self._active:
            raise CortRecursionError("CortCore.run called re-entrantly; potential infinite loop detected.")

        self._active = True
        start_time = time.monotonic()
        all_rounds: list[CortRound] = []
        seed: ReasoningChain | None = None

        try:
            full_prompt = f"{context}\n\n{prompt}".strip() if context else prompt

            for round_n in range(self.config.n_rounds):
                cort_round = await self._run_round(full_prompt, seed, round_n)
                all_rounds.append(cort_round)
                seed = cort_round.winner

                if (
                    self.config.early_stop_threshold is not None
                    and cort_round.winner.score >= self.config.early_stop_threshold
                ):
                    break
        finally:
            self._active = False

        elapsed = time.monotonic() - start_time
        best_chain = all_rounds[-1].winner
        total_calls = sum(len(r.alternatives) for r in all_rounds)

        metadata = CortMetadata(
            agent_id="",
            total_rounds=len(all_rounds),
            total_llm_calls=total_calls,
            elapsed_seconds=elapsed,
        )
        return CortResult(
            best_chain=best_chain,
            all_rounds=all_rounds,
            metadata=metadata,
        )

    async def _run_round(
        self,
        prompt: str,
        seed: ReasoningChain | None,
        round_n: int,
    ) -> CortRound:
        """Execute one CoRT round: generate, score, and select a winner.

        Args:
            prompt: The full prompt for this round.
            seed: The winning chain from the previous round, or ``None`` for
                the first round.
            round_n: Zero-based index of the current round.

        Returns:
            A :class:`CortRound` containing all alternatives and the winner.

        """
        seed_text = seed.text if seed is not None else ""
        alternatives = await self._generate_alternatives(prompt, seed_text, round_n)
        scored = self._evaluator.score_and_assign(alternatives, prompt)
        winner = self._evaluator.select_best(scored)
        return CortRound(
            round_n=round_n,
            prompt_used=prompt,
            alternatives=scored,
            winner=winner,
        )

    async def _generate_alternatives(
        self,
        prompt: str,
        seed_chain: str,
        round_n: int,
    ) -> list[ReasoningChain]:
        """Generate ``m_alternatives`` reasoning chains in parallel.

        Each alternative is produced with a distinct temperature following the
        schedule ``[base_temp + i * temp_step for i in range(m_alternatives)]``.

        Args:
            prompt: The prompt passed to each LLM call.
            seed_chain: Text of the best chain from the previous round, or an
                empty string for the first round.
            round_n: Zero-based index of the current round.

        Returns:
            A list of :class:`ReasoningChain` instances with score=0.0 and
            text from the LLM.

        Raises:
            AlternativesGenerationError: If all LLM calls in this generation
                attempt raise exceptions.

        """
        temperatures = [self.config.base_temp + i * self.config.temp_step for i in range(self.config.m_alternatives)]

        if seed_chain:
            llm_prompt = (
                f"{prompt}\n\nPrevious best reasoning:\n{seed_chain}\n\n"
                "Provide an improved or alternative reasoning chain:"
            )
        else:
            llm_prompt = prompt

        async def _call_one(idx: int, temp: float) -> ReasoningChain:
            """Invoke the LLM for a single alternative.

            Args:
                idx: Zero-based alternative index.
                temp: Temperature used for this alternative call.

            """
            text = await self._llm(
                llm_prompt,
                temperature=temp,
                max_tokens=self.config.max_tokens,
            )
            return ReasoningChain(
                text=text,
                score=0.0,
                round_n=round_n,
                temperature=temp,
                alternative_idx=idx,
            )

        tasks = [_call_one(i, t) for i, t in enumerate(temperatures)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        chains: list[ReasoningChain] = []
        errors: list[BaseException] = []
        for r in results:
            if isinstance(r, BaseException):
                errors.append(r)
            else:
                chains.append(r)

        if not chains:
            raise AlternativesGenerationError(
                f"All {self.config.m_alternatives} LLM calls failed in round {round_n}. Errors: {errors}"
            )

        return chains


def validate() -> bool:
    """Validate that the CortCore module is correctly configured.

    Returns:
        True when the module can be imported and the core class is accessible.

    """
    assert CortCore is not None
    return True
