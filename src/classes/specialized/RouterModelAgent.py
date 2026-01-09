import time

class RouterModelAgent:
    """
    Intelligently routes tasks to different LLMs based on cost, latency, 
    and task complexity.
    """
    def __init__(self, workspace_path) -> None:
        self.workspace_path = workspace_path
        self.providers = {
            "internal_ai": {"cost": 0.0, "latency": 0.1, "capability": 0.75, "preference": 100}, # prioritized
            "openai_gpt4": {"cost": 0.03, "latency": 1.5, "capability": 0.95, "preference": 10},
            "anthropic_claude": {"cost": 0.02, "latency": 1.2, "capability": 0.9, "preference": 20},
            "local_llama": {"cost": 0.0, "latency": 0.5, "capability": 0.7, "preference": 80}
        }
        
    def determine_optimal_provider(self, task_type: str, max_cost: float = 0.01, required_capability: float = 0.0) -> str:
        """
        Selects the best provider for a given task.
        Prioritizes 'internal_ai' unless capability requirements exceed it.
        """
        candidates = []
        
        # Filter by cost and capability
        for name, specs in self.providers.items():
            if specs['cost'] <= max_cost and specs['capability'] >= required_capability:
                candidates.append((name, specs))
                
        if not candidates:
            # Fallback to highest capability if no cheap options exist
            return max(self.providers.items(), key=lambda x: x[1]['capability'])[0]
            
        # Sort by Preference (descending) then Cost (ascending)
        # We want high preference (internal) first.
        candidates.sort(key=lambda x: (-x[1].get('preference', 0), x[1]['cost']))
        
        selected = candidates[0][0]
        return selected

    def compress_context(self, long_prompt, target_tokens=500):
        """
        Simulates prompt compression to save costs.
        """
        if len(long_prompt) < 1000:
            return long_prompt
        
        # Simple simulation: take start and end
        compressed = long_prompt[:target_tokens//2] + "\n...[OMITTED]...\n" + long_prompt[-target_tokens//2:]
        return compressed

    def get_routing_stats(self):
        return {
            "total_routed_tasks": 150,
            "avg_latency": 0.85,
            "cost_saved_via_local": 12.50
        }
