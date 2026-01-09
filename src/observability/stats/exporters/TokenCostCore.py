from typing import Dict, Any, List

# Constants for common models (Jan 2026 estimates)
MODEL_COSTS = {
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "claude-3-5-sonnet": {"input": 0.003, "output": 0.015},
    "claude-3-opus": {"input": 0.015, "output": 0.075},
    "gemini-1-5-pro": {"input": 0.0035, "output": 0.0105},
    "gemini-2-0-flash": {"input": 0.0001, "output": 0.0004},
    "default": {"input": 0.002, "output": 0.002}
}

class TokenCostCore:
    """
    Pure logic for cost calculations.
    No I/O or state management.
    """

    def compute_usd(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Returns the estimated cost in USD."""
        model_key = model.lower()
        pricing = self._find_pricing(model_key)
        
        # Cost per 1k tokens
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return round(input_cost + output_cost, 6)

    def _find_pricing(self, model_key: str) -> Dict[str, float]:
        """Heuristic for finding model pricing."""
        pricing = MODEL_COSTS.get(model_key)
        if not pricing:
            for key in MODEL_COSTS:
                if key != "default" and key in model_key:
                    return MODEL_COSTS[key]
        return pricing or MODEL_COSTS["default"]

    def list_models(self) -> List[str]:
        return list(MODEL_COSTS.keys())
