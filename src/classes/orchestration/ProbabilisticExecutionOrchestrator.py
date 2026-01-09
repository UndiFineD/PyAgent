#!/usr/bin/env python3

from __future__ import annotations
import logging
import json
import random
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from src.classes.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.classes.fleet.FleetManager import FleetManager

class ProbabilisticExecutionOrchestrator:
    """
    Implements 'Wave-function collapse' execution for Phase 28.
    Runs multiple parallel task variations and selects the most stable/optimal outcome.
    """
    
    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet

    def execute_with_confidence(self, task: str, variations: int = 3) -> Dict[str, Any]:
        """
        Executes a task multiple times and collapses the results into a single high-confidence output.
        """
        logging.info(f"ProbabilisticExecutionOrchestrator: Executing task '{task}' with {variations} variations.")
        
        results = []
        for i in range(variations):
            try:
                # In a real scenario, we might pass different 'seed' or 'temperature' signals
                # For this implementation, we rely on the variability of the reasoning agent.
                # Use ReasoningAgent to process the task
                res = self.fleet.call_by_capability("analyze", input_text=task)
                results.append(res)
                logging.info(f"Variation {i+1} completed.")
            except Exception as e:
                logging.error(f"Variation {i+1} failed: {e}")

        if not results:
            return {"status": "error", "message": "All execution variations failed."}

        # Wave-function collapse: Select the best result
        collapsed_result = self._collapse(task, results)
        
        confidence = self._calculate_confidence(results, collapsed_result)
        
        logging.info(f"Probabilistic execution complete. Confidence: {confidence:.2f}")
        
        return {
            "status": "success",
            "final_result": collapsed_result,
            "variations_run": len(results),
            "confidence": confidence
        }

    def _collapse(self, task: str, results: List[Any]) -> Any:
        """
        Selects the most optimal result from the set of variations.
        If RealityAnchorAgent is available, it uses it for verification.
        """
        # Attempt to use RealityAnchorAgent for grounding if it exists in the fleet
        if hasattr(self.fleet, 'reality_anchor') and self.fleet.reality_anchor:
            best_result = None
            highest_score = -1.0
            
            for res in results:
                try:
                    verification = self.fleet.reality_anchor.verify_claim(str(res))
                    score = verification.get("confidence_score", 0.0)
                    if score > highest_score:
                        highest_score = score
                        best_result = res
                except Exception:
                    continue
            
            if best_result is not None:
                return best_result

        # Fallback: Pick the most frequent result (simplistic consensus)
        # For non-string objects, we convert to string for comparison
        from collections import Counter
        str_results = [str(r) for r in results]
        most_common_str = Counter(str_results).most_common(1)[0][0]
        
        # Find the original object corresponding to the most common string
        for r in results:
            if str(r) == most_common_str:
                return r

        return results[0]

    def _calculate_confidence(self, results: List[Any], winner: Any) -> float:
        """
        Calculates confidence score based on similarity between variations.
        """
        if not results:
            return 0.0
        # Percentage of results that match the winner string-wise
        matches = sum(1 for r in results if str(r) == str(winner))
        return matches / len(results)
