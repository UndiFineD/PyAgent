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


"""Agent specializing in Bayesian inference and decision-making under uncertainty.
Applies Bayes' theorem to update beliefs based on new evidence.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Any
from src.core.base.base_agent import BaseAgent
from src.core.base.base_utilities import as_tool

__version__ = VERSION


class BayesianReasoningAgent(BaseAgent):
    """Integrates Bayesian methods for robust fleet decision-making."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Bayesian Reasoning Agent. "
            "Your role is to update fleet beliefs and optimize actions using Bayesian inference. "
            "You quantify uncertainty and provide probabilistic insights into task success or system health."
        )
        # Internal belief store: {concept: {"prior": float, "likelihoods": {evidence: float}}}
        self.beliefs: dict[str, Any] = {}

    @as_tool
    def update_belief(
        self, concept: str, evidence_observed: str, likelihood: float
    ) -> dict[str, float]:
        """
        Updates the posterior probability of a concept given new evidence.
        Formula: P(H|E) = (P(E|H) * P(H)) / P(E)
        """
        if concept not in self.beliefs:
            # Default prior: 0.5 (Uncertain)
            self.beliefs[concept] = {"prior": 0.5}

        prior = self.beliefs[concept]["prior"]

        # Marginal likelihood P(E) = P(E|H)P(H) + P(E|not H)P(not H)
        # We assume P(E|not H) is inverse of likelyhood or a baseline (e.g., 0.2)
        p_not_h = 1.0 - prior
        p_e_given_not_h = 0.2

        marginal_evidence = (likelihood * prior) + (p_e_given_not_h * p_not_h)

        posterior = (likelihood * prior) / marginal_evidence

        # Update internal state
        self.beliefs[concept]["prior"] = posterior

        logging.info(
            f"BayesianAgent: Updated belief for '{concept}' to {posterior:.4f} based on '{evidence_observed}'"
        )
        return {"concept": concept, "posterior": posterior, "prior_was": prior}

    @as_tool
    def calculate_expected_utility(self, actions: list[dict[str, Any]]) -> str:
        """
        Selects the action that maximizes expected utility.
        Input format: [{"name": str, "utility": float, "success_prob_concept": str}]
        """
        best_action = None
        max_utility = -1e9

        results = []
        for action in actions:
            concept = action.get("success_prob_concept")
            prob = self.beliefs.get(concept, {}).get("prior", 0.5) if concept else 1.0

            expected_utility = action["utility"] * prob
            results.append(f"{action['name']}: {expected_utility:.2f}")

            if expected_utility > max_utility:
                max_utility = expected_utility
                best_action = action["name"]

        return f"Policy Decision: Recommended '{best_action}'. Analysis: {', '.join(results)}"

    async def improve_content(self, input_text: str) -> str:
        """Analyzes text for uncertainty and provides Bayesian calibration."""
        prompt = (
            "Analyze the following report or code for potential uncertainties or failure points. "
            "Assign probabilistic confidence scores to different success paths and suggest a "
            "Bayesian strategy to mitigate risks.\n\n"
            f"Content:\n{input_text}"
        )
        return await self.think(prompt)


if __name__ == "__main__":
    from src.core.base.base_utilities import create_main_function

    main = create_main_function(
        BayesianReasoningAgent, "Bayesian Agent", "Belief store path"
    )
    main()
