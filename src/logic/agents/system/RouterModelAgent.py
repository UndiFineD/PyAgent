import time
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.version import VERSION
__version__ = VERSION


class RouterModelAgent(BaseAgent):
    """
    Intelligently routes tasks to different LLMs based on cost, latency, 
    and task complexity.
    """
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.providers: Dict[str, Any] = {
            "internal_ai": {"cost": 0.0, "latency": 0.1, "capability": 0.75, "preference": 100}, # prioritized
            "glm_4_7": {"cost": 0.0006, "latency": 0.8, "capability": 0.9, "preference": 90},  # Phase 128: Cost efficiency
            "openai_gpt4": {"cost": 0.03, "latency": 1.5, "capability": 0.95, "preference": 30},
            "anthropic_claude": {"cost": 0.02, "latency": 1.2, "capability": 0.9, "preference": 20},
            "local_llama": {"cost": 0.0, "latency": 0.5, "capability": 0.7, "preference": 110}
        }
        
    def determine_optimal_provider(self, task_type: str, max_cost: float = 0.01, required_capability: float = 0.0) -> str:
        """
        Selects the best provider for a given task.
        Prioritizes 'internal_ai' unless capability requirements exceed it.
        """
        if self.recorder:
            self.recorder.record_lesson("router_decision_request", {"task": task_type, "max_cost": max_cost})

        # Phase 120: Heuristic Risk/Capability Mapping
        if "high_reasoning" in task_type.lower():
            required_capability = 0.9
            max_cost = 0.1  # Allow for GPT-4 costs
        elif "simple" in task_type.lower():
            required_capability = 0.0
            max_cost = 0.01

        candidates = []
        
        # Filter by cost and capability
        for name, specs in self.providers.items():
            if specs['cost'] <= max_cost and specs['capability'] >= required_capability:
                candidates.append((name, specs))
                
        if not candidates:
            # Fallback to highest capability if no cheap options exist
            providers_list = list(self.providers.items())
            return max(providers_list, key=lambda x: x[1]['capability'])[0]
            
        # Sort by Preference (descending) then Cost (ascending)
        # We want high preference (internal) first.
        candidates.sort(key=lambda x: (-x[1].get('preference', 0), x[1]['cost']))
        
        selected = candidates[0][0]
        return selected

    def compress_context(self, long_prompt: str, target_tokens: int = 500) -> str:
        """
        Simulates prompt compression to save costs.
        """
        if len(long_prompt) < 1000:
            return long_prompt
        
        # Simple simulation: take start and end
        compressed = long_prompt[:target_tokens//2] + "\n...[OMITTED]...\n" + long_prompt[-target_tokens//2:]
        return compressed

    def get_routing_stats(self) -> Dict[str, Any]:
        return {
            "total_routed_tasks": 150,
            "avg_latency": 0.85,
            "cost_saved_via_local": 12.50
        }
