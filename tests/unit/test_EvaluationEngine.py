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
"""Unit tests for EvaluationEngine: rubric scoring, keyword recall, depth heuristics, selection.

All tests in this module are RED-phase: they fail at collection time because
``src.core.reasoning`` does not yet exist.  The correct failure reason is
``ModuleNotFoundError``, NOT an assertion error.
"""

from __future__ import annotations

import pytest

from src.core.reasoning import EvaluationEngine
from src.core.reasoning.CortCore import ReasoningChain
from src.core.reasoning.EvaluationEngine import RubricScore

# ---------------------------------------------------------------------------
# TC-EE-01  RubricScore weighted total when all axes are 1.0
# ---------------------------------------------------------------------------


def test_rubric_score_weighted_total() -> None:
    """RubricScore with all axes at 1.0 has a weighted_total of exactly 1.0 (0.5+0.3+0.2=1.0)."""
    score = RubricScore(correctness=1.0, completeness=1.0, reasoning_depth=1.0)
    assert abs(score.weighted_total - 1.0) < 1e-9


# ---------------------------------------------------------------------------
# TC-EE-02  Individual weight verification: 0.5 / 0.3 / 0.2
# ---------------------------------------------------------------------------


def test_rubric_score_weights() -> None:
    """Each axis contribution to weighted_total matches its expected weight coefficient."""
    score_c = RubricScore(correctness=10.0, completeness=0.0, reasoning_depth=0.0)
    assert abs(score_c.weighted_total - 5.0) < 1e-6, f"Correctness weight should be 0.5; got {score_c.weighted_total}"

    score_p = RubricScore(correctness=0.0, completeness=10.0, reasoning_depth=0.0)
    assert abs(score_p.weighted_total - 3.0) < 1e-6, f"Completeness weight should be 0.3; got {score_p.weighted_total}"

    score_r = RubricScore(correctness=0.0, completeness=0.0, reasoning_depth=10.0)
    assert abs(score_r.weighted_total - 2.0) < 1e-6, (
        f"Reasoning depth weight should be 0.2; got {score_r.weighted_total}"
    )


# ---------------------------------------------------------------------------
# TC-EE-03  Correctness penalises self-correction markers
# ---------------------------------------------------------------------------


def test_correctness_penalizes_contradictions() -> None:
    """Text containing self-correction markers scores lower correctness than clean reasoning."""
    engine = EvaluationEngine()
    clean_text = (
        "The capital of France is Paris. It has been the recognised capital "
        "since 987 AD and hosts the national government."
    )
    contradicting_text = (
        "Actually, that's wrong. I was wrong earlier. Wait, let me reconsider. Actually no, that is not correct at all."
    )
    clean_score = engine._score_correctness(clean_text)
    bad_score = engine._score_correctness(contradicting_text)
    assert clean_score > bad_score, (
        f"Clean text ({clean_score:.3f}) must score higher correctness than self-correcting text ({bad_score:.3f})"
    )


# ---------------------------------------------------------------------------
# TC-EE-04  Completeness rewards prompt-keyword recall
# ---------------------------------------------------------------------------


def test_completeness_rewards_keyword_recall() -> None:
    """Text containing all prompt keywords scores higher completeness than text with none."""
    engine = EvaluationEngine()
    prompt = "explain machine learning algorithms neural networks"
    text_with_keywords = "Machine learning algorithms use neural networks for pattern recognition."
    text_without_keywords = "This generic response does not touch on the subject at all and stays vague."
    score_with = engine._score_completeness(text_with_keywords, prompt)
    score_without = engine._score_completeness(text_without_keywords, prompt)
    assert score_with > score_without, (
        f"Keyword-rich text ({score_with:.3f}) must outscore keyword-absent text ({score_without:.3f})"
    )


# ---------------------------------------------------------------------------
# TC-EE-05  Reasoning depth rewards logical connectives
# ---------------------------------------------------------------------------


def test_reasoning_depth_rewards_connectives() -> None:
    """Text using logical connectives (therefore, because) scores higher reasoning depth."""
    engine = EvaluationEngine()
    deep_reasoning = (
        "Because the algorithm converges monotonically, therefore we can conclude "
        "the result is optimal. Since the loss function is convex, however, "
        "local minima are globally optimal."
    )
    shallow_text = "The algorithm works. The result is good. It is correct."
    deep_score = engine._score_reasoning_depth(deep_reasoning)
    shallow_score = engine._score_reasoning_depth(shallow_text)
    assert deep_score > shallow_score, (
        f"Connective-rich text ({deep_score:.3f}) must outscore flat text ({shallow_score:.3f})"
    )


# ---------------------------------------------------------------------------
# TC-EE-06  Reasoning depth rewards structured lists
# ---------------------------------------------------------------------------


def test_reasoning_depth_rewards_structure() -> None:
    """A numbered list scores higher reasoning depth than equivalent unstructured prose."""
    engine = EvaluationEngine()
    structured_text = (
        "1. First, initialise the weights.\n2. Second, compute the forward pass.\n3. Third, backpropagate the gradient."
    )
    unstructured_text = "Initialise the weights then compute the forward pass then backpropagate the gradient."
    structured_score = engine._score_reasoning_depth(structured_text)
    unstructured_score = engine._score_reasoning_depth(unstructured_text)
    assert structured_score > unstructured_score, (
        f"Structured text ({structured_score:.3f}) must outscore unstructured text ({unstructured_score:.3f})"
    )


# ---------------------------------------------------------------------------
# TC-EE-07  select_best returns the chain with the highest score
# ---------------------------------------------------------------------------


def test_select_best_returns_highest_score() -> None:
    """EvaluationEngine.select_best returns the ReasoningChain with the highest score."""
    engine = EvaluationEngine()
    chain_low = ReasoningChain(text="low quality", score=2.0, round_n=0, temperature=0.7, alternative_idx=0)
    chain_high = ReasoningChain(text="high quality", score=9.0, round_n=0, temperature=0.85, alternative_idx=1)
    chain_mid = ReasoningChain(text="medium quality", score=5.0, round_n=0, temperature=1.0, alternative_idx=2)
    best = engine.select_best([chain_low, chain_high, chain_mid])
    assert best is chain_high, f"Expected chain_high (score=9.0) but got score={best.score}"


# ---------------------------------------------------------------------------
# TC-EE-08  select_best tie-breaks by alternative_idx (ascending)
# ---------------------------------------------------------------------------


def test_select_best_tie_breaks_by_depth() -> None:
    """When two chains have equal scores, select_best picks the one with the lower alternative_idx."""
    engine = EvaluationEngine()
    chain_first = ReasoningChain(
        text="because therefore since", score=5.0, round_n=0, temperature=0.7, alternative_idx=0
    )
    chain_second = ReasoningChain(
        text="because therefore since hence", score=5.0, round_n=0, temperature=0.85, alternative_idx=1
    )
    # Deliberately pass chain_second first to confirm ordering is not list-order dependent
    best = engine.select_best([chain_second, chain_first])
    assert best is chain_first, "On equal score, select_best must return the chain with the lower alternative_idx"


# ---------------------------------------------------------------------------
# TC-EE-09  Completeness returns 1.0 when prompt has no keywords ≥ 4 chars
# ---------------------------------------------------------------------------


def test_completeness_empty_prompt_keywords() -> None:
    """_score_completeness returns 1.0 when the prompt contains no words of 4+ characters."""
    engine = EvaluationEngine()
    # "do" (2 chars) and "it" (2 chars) are both below the 4-char threshold.
    score = engine._score_completeness(
        "some detailed answer covering the topic comprehensively",
        "do it",
    )
    assert score == 1.0, f"Expected 1.0 for empty keyword set but got {score}"


# ---------------------------------------------------------------------------
# TC-EE-10  Reasoning depth caps at 1.0 when all connectives present with structure
# ---------------------------------------------------------------------------


def test_reasoning_depth_caps_at_one() -> None:
    """_score_reasoning_depth returns exactly 1.0 when all connectives are present alongside a numbered list."""
    engine = EvaluationEngine()
    # Contains all 8 logical connectives (base_score already 1.0) AND a numbered list.
    # The structure bonus path (min(1.0, 1.0 + 0.2)) must cap at 1.0.
    fully_saturated_text = (
        "1. therefore because however thus hence moreover furthermore consequently\n"
        "2. the analysis demonstrates the result is valid and complete"
    )
    score = engine._score_reasoning_depth(fully_saturated_text)
    assert score == 1.0, f"Expected capped score of 1.0 but got {score}"


# ---------------------------------------------------------------------------
# TC-EE-11  select_best raises ValueError on empty chain list
# ---------------------------------------------------------------------------


def test_select_best_raises_value_error_on_empty_list() -> None:
    """EvaluationEngine.select_best raises ValueError when given an empty list."""
    engine = EvaluationEngine()
    with pytest.raises(ValueError, match="non-empty"):
        engine.select_best([])
