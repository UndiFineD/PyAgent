#!/usr/bin/env python3

"""Agent specializing in Bayesian inference and decision-making under uncertainty.
Applies Bayes' theorem to update beliefs based on new evidence.
"""

from __future__ import annotations

import logging
import json
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

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
        self.beliefs: Dict[str, Any] = {}

    @as_tool
    def update_belief(self, concept: str, evidence_observed: str, likelihood: float) -> Dict[str, float]:
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
        
        logging.info(f"BayesianAgent: Updated belief for '{concept}' to {posterior:.4f} based on '{evidence_observed}'")
        return {"concept": concept, "posterior": posterior, "prior_was": prior}

    @as_tool
    def calculate_expected_utility(self, actions: List[Dict[str, Any]]) -> str:
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
            
            if expected_utility > max_utility :
                max_utility = expected_utility
                best_action = action["name"]
                
        return f"Policy Decision: Recommended '{best_action}'. Analysis: {', '.join(results)}"

    def improve_content(self, input_text: str) -> str:
        """Analyzes text for uncertainty and provides Bayesian calibration."""
        prompt = (
            "Analyze the following report or code for potential uncertainties or failure points. "
            "Assign probabilistic confidence scores to different success paths and suggest a "
            "Bayesian strategy to mitigate risks.\n\n"
            f"Content:\n{input_text}"
        )
        return self.think(prompt)

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(BayesianReasoningAgent, "Bayesian Agent", "Belief store path")
    main()
