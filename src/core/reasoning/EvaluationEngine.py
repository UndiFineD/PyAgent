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
"""EvaluationEngine — rubric-based scoring for CoRT reasoning chains.

Scoring is purely heuristic and works without any external NLP libraries.  The
three rubric axes are:

* **Correctness** (weight 0.5): penalises self-contradiction markers.
* **Completeness** (weight 0.3): measures keyword recall from the prompt.
* **Reasoning depth** (weight 0.2): counts logical connectives and structural
  elements.

The combined :class:`RubricScore` is used by :class:`CortCore` to rank
alternative chains and select the best one to carry forward.
"""

from __future__ import annotations

import dataclasses
import re
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_CONTRADICTION_MARKERS: tuple[str, ...] = (
    "actually, that's wrong",
    "i was incorrect",
    "wait,",
    "let me reconsider",
)

_LOGICAL_CONNECTIVES: tuple[str, ...] = (
    "therefore",
    "because",
    "however",
    "thus",
    "hence",
    "moreover",
    "furthermore",
    "consequently",
)

_CONNECTIVES_FOR_FULL_SCORE: int = 4
_STRUCTURE_BONUS: float = 0.2

# Pre-compiled patterns
_NUMBERED_LIST_RE = re.compile(r"^\s*\d+\.", re.MULTILINE)
_CODE_BLOCK_RE = re.compile(r"```")


# ---------------------------------------------------------------------------
# RubricScore
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RubricScore:
    """Immutable rubric score for a single reasoning chain.

    ``weighted_total`` is automatically computed in ``__post_init__`` and is
    **not** an initialiser argument.

    Attributes:
        correctness: 0.0–1.0 absence-of-contradiction score (weight 0.5).
        completeness: 0.0–1.0 prompt-keyword recall score (weight 0.3).
        reasoning_depth: 0.0–1.0 logical-connective density score (weight 0.2).
        weighted_total: 0.5·correctness + 0.3·completeness + 0.2·reasoning_depth
            (auto-computed, cannot be provided by caller).

    """

    correctness: float
    completeness: float
    reasoning_depth: float
    weighted_total: float = field(init=False)

    def __post_init__(self) -> None:
        """Compute the weighted total from the three axis scores.

        Uses ``object.__setattr__`` because the dataclass is frozen.
        """
        total = 0.5 * self.correctness + 0.3 * self.completeness + 0.2 * self.reasoning_depth
        object.__setattr__(self, "weighted_total", total)


# ---------------------------------------------------------------------------
# EvaluationEngine
# ---------------------------------------------------------------------------


class EvaluationEngine:
    """Heuristic rubric-based evaluator for CoRT reasoning chains.

    Args:
        use_llm_judge: Reserved for future LLM-based evaluation; currently
            unused (heuristic scoring is always applied).
        llm: Optional LLM callable; reserved for ``use_llm_judge`` mode.

    """

    def __init__(
        self,
        use_llm_judge: bool = False,
        llm: Any | None = None,
    ) -> None:
        """Initialise the EvaluationEngine.

        Args:
            use_llm_judge: If True, LLM-based judging will be used in a future
                implementation.  Currently has no effect.
            llm: Optional async LLM callable for judge mode (reserved).

        """
        self._use_llm_judge = use_llm_judge
        self._llm = llm

    def score(self, chain: str, prompt: str) -> RubricScore:
        """Compute the full rubric score for a single reasoning chain.

        Args:
            chain: The reasoning chain text to evaluate.
            prompt: The original prompt the chain is responding to.

        Returns:
            A :class:`RubricScore` with all three axes computed and
            ``weighted_total`` auto-filled.

        """
        correctness = self._score_correctness(chain)
        completeness = self._score_completeness(chain, prompt)
        reasoning_depth = self._score_reasoning_depth(chain)
        return RubricScore(
            correctness=correctness,
            completeness=completeness,
            reasoning_depth=reasoning_depth,
        )

    def _score_correctness(self, chain: str) -> float:
        """Score correctness by penalising self-contradiction markers.

        Starts from 1.0 and subtracts 0.2 for each recognised contradiction
        marker found in the text (case-insensitive).  The score is floored at
        0.0.

        Args:
            chain: The reasoning chain text to evaluate.

        Returns:
            A float in [0.0, 1.0] representing absence of contradictions.

        """
        text_lower = chain.lower()
        penalty = sum(1 for marker in _CONTRADICTION_MARKERS if marker in text_lower)
        return max(0.0, 1.0 - 0.2 * penalty)

    def _score_completeness(self, chain: str, prompt: str) -> float:
        """Score completeness via keyword recall from the prompt.

        Extracts all words of four or more characters from the prompt
        (lowercased) and counts how many appear anywhere in the chain.
        Returns the recall ratio (0.0 if the prompt has no long words).

        Args:
            chain: The reasoning chain text to evaluate.
            prompt: The prompt that the chain responds to.

        Returns:
            A float in [0.0, 1.0] representing keyword recall.

        """
        prompt_words = re.findall(r"\b\w{4,}\b", prompt.lower())
        if not prompt_words:
            return 1.0

        chain_lower = chain.lower()
        unique_keywords = set(prompt_words)
        found = sum(1 for kw in unique_keywords if kw in chain_lower)
        return found / len(unique_keywords)

    def _score_reasoning_depth(self, chain: str) -> float:
        """Score reasoning depth via logical connective count and structure.

        Counts the number of logical connectives from a fixed vocabulary and
        normalises to [0.0, 1.0] (4+ connectives = 1.0).  An additional bonus
        of 0.2 is added if a numbered list or a fenced code block is detected,
        with the final score capped at 1.0.

        Args:
            chain: The reasoning chain text to evaluate.

        Returns:
            A float in [0.0, 1.0] representing logical depth.

        """
        text_lower = chain.lower()
        connective_count = sum(1 for connective in _LOGICAL_CONNECTIVES if connective in text_lower)

        base_score = min(1.0, connective_count / _CONNECTIVES_FOR_FULL_SCORE)

        has_structure = bool(_NUMBERED_LIST_RE.search(chain) or _CODE_BLOCK_RE.search(chain))
        if has_structure:
            base_score = min(1.0, base_score + _STRUCTURE_BONUS)

        return base_score

    def select_best(self, chains: list[Any]) -> Any:
        """Return the highest-scoring chain; tie-break by lowest alternative_idx.

        Args:
            chains: A non-empty list of scored :class:`ReasoningChain` objects.

        Returns:
            The chain with the highest ``score``.  If two chains share the same
            score, the one with the lower ``alternative_idx`` is returned.

        Raises:
            ValueError: If ``chains`` is empty.

        """
        if not chains:
            raise ValueError("select_best requires a non-empty list of chains.")
        return max(chains, key=lambda c: (c.score, -c.alternative_idx))

    def score_and_assign(
        self,
        chains: list[Any],
        prompt: str,
    ) -> list[Any]:
        """Score each chain and return new instances with scores assigned.

        Args:
            chains: A list of :class:`ReasoningChain` objects to score.
            prompt: The prompt used to evaluate completeness.

        Returns:
            A new list of :class:`ReasoningChain` instances with their
            ``score`` field set to the computed ``weighted_total``.

        """
        return [dataclasses.replace(chain, score=self.score(chain.text, prompt).weighted_total) for chain in chains]


def validate() -> bool:
    """Validate that the EvaluationEngine module is correctly configured.

    Returns:
        True when the module can be imported and the engine class is accessible.

    """
    assert EvaluationEngine is not None
    return True
