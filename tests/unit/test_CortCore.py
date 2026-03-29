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
"""Unit tests for CortCore: config validation, data models, loop logic, and recursion guard.

All tests in this module are RED-phase: they fail at collection time because
``src.core.reasoning`` does not yet exist.  The correct failure reason is
``ModuleNotFoundError``, NOT an assertion error.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from src.core.reasoning import (
    DEFAULT_CORT_CONFIG,
    CortConfig,
    CortCore,
    CortResult,
    EvaluationEngine,
)
from src.core.reasoning.CortCore import (
    AlternativesGenerationError,
    CortLimitExceeded,
    CortRecursionError,
    CortRound,
    ReasoningChain,
)

# ---------------------------------------------------------------------------
# TC-CC-01  CortConfig defaults
# ---------------------------------------------------------------------------


def test_cort_config_defaults() -> None:
    """DEFAULT_CORT_CONFIG uses n_rounds=3 and m_alternatives=3."""
    assert DEFAULT_CORT_CONFIG.n_rounds == 3
    assert DEFAULT_CORT_CONFIG.m_alternatives == 3


# ---------------------------------------------------------------------------
# TC-CC-02  CortConfig cap enforcement (5 × 4 = 20 > 15)
# ---------------------------------------------------------------------------


def test_cort_config_cap_enforcement() -> None:
    """CortConfig(n_rounds=5, m_alternatives=4) raises CortLimitExceeded (5×4=20>15)."""
    with pytest.raises(CortLimitExceeded):
        CortConfig(n_rounds=5, m_alternatives=4)


# ---------------------------------------------------------------------------
# TC-CC-03  CortConfig valid boundary (3 × 5 = 15, exactly on cap)
# ---------------------------------------------------------------------------


def test_cort_config_valid_cap() -> None:
    """CortConfig(n_rounds=3, m_alternatives=5) is valid because 3×5=15 equals the cap."""
    cfg = CortConfig(n_rounds=3, m_alternatives=5)
    assert cfg.n_rounds == 3
    assert cfg.m_alternatives == 5


# ---------------------------------------------------------------------------
# TC-CC-04  ReasoningChain ordering via .score field
# ---------------------------------------------------------------------------


def test_reasoning_chain_ordering() -> None:
    """A ReasoningChain with a higher .score value compares as greater than one with a lower value."""
    chain_low = ReasoningChain(
        text="low quality answer",
        score=3.0,
        round_n=0,
        temperature=0.7,
        alternative_idx=0,
    )
    chain_high = ReasoningChain(
        text="high quality answer",
        score=8.0,
        round_n=0,
        temperature=0.85,
        alternative_idx=1,
    )
    assert chain_high.score > chain_low.score
    assert chain_low.score < chain_high.score


# ---------------------------------------------------------------------------
# TC-CC-05  CortResult.best_chain is the highest-scoring chain
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_result_has_best_chain() -> None:
    """CortResult.best_chain is a ReasoningChain whose score is >= all alternatives in the final round."""
    llm_mock = AsyncMock(return_value="some answer text")
    evaluator = EvaluationEngine()
    cfg = CortConfig(n_rounds=1, m_alternatives=3)
    core = CortCore(llm=llm_mock, evaluator=evaluator, config=cfg)

    result = await core.run("What is the capital of France?")

    assert isinstance(result, CortResult)
    assert isinstance(result.best_chain, ReasoningChain)
    final_round: CortRound = result.all_rounds[-1]
    max_alt_score = max(chain.score for chain in final_round.alternatives)
    assert result.best_chain.score >= max_alt_score - 1e-9


# ---------------------------------------------------------------------------
# TC-CC-06  CortResult.all_rounds length equals n_rounds
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_result_round_count() -> None:
    """CortResult.all_rounds has exactly n_rounds entries after a successful run."""
    llm_mock = AsyncMock(return_value="answer text")
    evaluator = EvaluationEngine()
    cfg = CortConfig(n_rounds=2, m_alternatives=2)
    core = CortCore(llm=llm_mock, evaluator=evaluator, config=cfg)

    result = await core.run("test prompt")

    assert len(result.all_rounds) == 2


# ---------------------------------------------------------------------------
# TC-CC-07  CortCore.run returns a CortResult instance
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_core_run_returns_cort_result() -> None:
    """CortCore.run with a mock LLM returns a CortResult instance."""
    llm_mock = AsyncMock(return_value="mock response")
    evaluator = EvaluationEngine()
    cfg = CortConfig(n_rounds=1, m_alternatives=1)
    core = CortCore(llm=llm_mock, evaluator=evaluator, config=cfg)

    result = await core.run("Solve this problem")

    assert isinstance(result, CortResult)


# ---------------------------------------------------------------------------
# TC-CC-08  LLM is called exactly n_rounds × m_alternatives times
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_core_calls_llm_n_times_m_alternatives() -> None:
    """With n_rounds=2 and m_alternatives=2, CortCore.run makes exactly 4 LLM calls."""
    llm_mock = AsyncMock(return_value="response text")
    evaluator = EvaluationEngine()
    cfg = CortConfig(n_rounds=2, m_alternatives=2)
    core = CortCore(llm=llm_mock, evaluator=evaluator, config=cfg)

    await core.run("prompt")

    assert llm_mock.call_count == 4


# ---------------------------------------------------------------------------
# TC-CC-09  Temperature schedule is monotonically non-decreasing per round
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_core_temperature_schedule() -> None:
    """LLM is called with increasing temperatures for each alternative within a round."""
    call_temps: list[float] = []

    async def recording_llm(prompt: str, *, temperature: float, max_tokens: int) -> str:
        """Record the temperature parameter and return a stub response."""
        call_temps.append(temperature)
        return "answer"

    evaluator = EvaluationEngine()
    cfg = CortConfig(n_rounds=1, m_alternatives=3, base_temp=0.7, temp_step=0.15)
    core = CortCore(llm=recording_llm, evaluator=evaluator, config=cfg)

    await core.run("prompt")

    assert len(call_temps) == 3
    for i in range(len(call_temps) - 1):
        assert call_temps[i + 1] >= call_temps[i], (
            f"Temperature must not decrease: temps[{i}]={call_temps[i]} > temps[{i + 1}]={call_temps[i + 1]}"
        )


# ---------------------------------------------------------------------------
# TC-CC-10  Recursion guard: nested CortCore.run raises CortRecursionError
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_recursion_guard() -> None:
    """Calling CortCore.run from within an active CortCore.run raises CortRecursionError."""
    evaluator = EvaluationEngine()
    cfg = CortConfig(n_rounds=1, m_alternatives=1)
    core: CortCore | None = None
    nested_raised: list[bool] = [False]

    async def reentrant_llm(prompt: str, *, temperature: float, max_tokens: int) -> str:
        """Attempt a nested core.run() call to trigger the recursion guard."""
        try:
            assert core is not None  # noqa: S101
            await core.run("nested prompt")
        except CortRecursionError:
            nested_raised[0] = True
        except Exception:  # noqa: BLE001
            pass
        return "outer response"

    core = CortCore(llm=reentrant_llm, evaluator=evaluator, config=cfg)
    await core.run("outer prompt")

    assert nested_raised[0], "CortRecursionError must be raised when CortCore.run is called re-entrantly"


# ---------------------------------------------------------------------------
# TC-CC-11  CortLimitExceeded at init (4 × 4 = 16 > 15)
# ---------------------------------------------------------------------------


def test_cort_limit_exceeded() -> None:
    """CortConfig(n_rounds=4, m_alternatives=4) raises CortLimitExceeded because 4×4=16>15."""
    with pytest.raises(CortLimitExceeded):
        CortConfig(n_rounds=4, m_alternatives=4)


# ---------------------------------------------------------------------------
# TC-CC-12  ReasoningChain.__lt__ returns NotImplemented for non-chain operand
# ---------------------------------------------------------------------------


def test_reasoning_chain_lt_notimplemented() -> None:
    """ReasoningChain.__lt__ returns NotImplemented when the operand is not a ReasoningChain."""
    chain = ReasoningChain(
        text="test chain",
        score=5.0,
        round_n=0,
        temperature=0.7,
        alternative_idx=0,
    )
    result = chain.__lt__("not_a_chain")
    assert result is NotImplemented


# ---------------------------------------------------------------------------
# TC-CC-13  ReasoningChain.__gt__ returns NotImplemented for non-chain operand
# ---------------------------------------------------------------------------


def test_reasoning_chain_gt_notimplemented() -> None:
    """ReasoningChain.__gt__ returns NotImplemented when the operand is not a ReasoningChain."""
    chain = ReasoningChain(
        text="test chain",
        score=5.0,
        round_n=0,
        temperature=0.7,
        alternative_idx=0,
    )
    result = chain.__gt__(42)
    assert result is NotImplemented


# ---------------------------------------------------------------------------
# TC-CC-14  ReasoningChain.__eq__ returns NotImplemented for non-chain operand
# ---------------------------------------------------------------------------


def test_reasoning_chain_eq_notimplemented() -> None:
    """ReasoningChain.__eq__ returns NotImplemented when the operand is not a ReasoningChain."""
    chain = ReasoningChain(
        text="test chain",
        score=5.0,
        round_n=0,
        temperature=0.7,
        alternative_idx=0,
    )
    result = chain.__eq__(None)
    assert result is NotImplemented


# ---------------------------------------------------------------------------
# TC-CC-15  Early-stop threshold halts the loop after the first passing round
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_core_early_stop_skips_remaining_rounds() -> None:
    """With early_stop_threshold=0.99, CortCore stops after the first round whose winner scores ≥ 0.99."""
    # Response with all 8 known connectives → depth=1.0; no contradiction markers → correctness=1.0
    # Prompt "ab" has no words ≥ 4 chars → completeness=1.0.  Total = 0.5+0.3+0.2 = 1.0 ≥ 0.99.
    high_score_response = (
        "therefore because however thus hence moreover furthermore consequently the conclusion is definitive"
    )
    llm_mock = AsyncMock(return_value=high_score_response)
    evaluator = EvaluationEngine()
    cfg = CortConfig(n_rounds=3, m_alternatives=2, early_stop_threshold=0.99)
    core = CortCore(llm=llm_mock, evaluator=evaluator, config=cfg)

    result = await core.run("ab")

    assert len(result.all_rounds) == 1, f"Expected early stop after round 0 but got {len(result.all_rounds)} rounds"


# ---------------------------------------------------------------------------
# TC-CC-16  AlternativesGenerationError raised when all LLM calls fail
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_all_alternatives_fail_raises_alternatives_generation_error() -> None:
    """When all LLM calls fail in a round, CortCore.run propagates AlternativesGenerationError."""

    async def failing_llm(prompt: str, *, temperature: float, max_tokens: int) -> str:
        """Always raise to simulate a total API outage."""
        raise RuntimeError("API error")

    evaluator = EvaluationEngine()
    cfg = CortConfig(n_rounds=1, m_alternatives=2)
    core = CortCore(llm=failing_llm, evaluator=evaluator, config=cfg)

    with pytest.raises(AlternativesGenerationError):
        await core.run("test prompt")
