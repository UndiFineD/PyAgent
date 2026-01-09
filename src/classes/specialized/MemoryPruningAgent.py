import time

class MemoryPruningAgent:
    """
    Optimizes Long-Term Memory (LTM) by ranking importance and 
    pruning low-utility or stale data slices.
    """
    def __init__(self, workspace_path) -> None:
        self.workspace_path = workspace_path
        
    def rank_memory_importance(self, memory_entry):
        """
        Ranks a memory entry based on recency, frequency of access, and logical density.
        """
        score = 0.0
        
        # Factor 1: Recency
        age = time.time() - memory_entry.get("timestamp", 0)
        recency_penalty = min(0.5, age / (3600 * 24)) # Max penalty 0.5 for >1 day
        score += (0.5 - recency_penalty)
        
        # Factor 2: Frequency
        access_count = memory_entry.get("access_count", 0)
        frequency_bonus = min(0.4, access_count * 0.1)
        score += frequency_bonus
        
        # Factor 3: Complexity/Density
        content = memory_entry.get("content", "")
        if "error" in content.lower() or "fix" in content.lower():
            score += 0.1 # Retain errors/fixes with higher priority
            
        return round(score, 3)

    def select_pruning_targets(self, memory_list, threshold=0.2):
        """
        Identifies entries that fall below the utility threshold.
        """
        targets = []
        for i, entry in enumerate(memory_list):
            rank = self.rank_memory_importance(entry)
            if rank < threshold:
                targets.append({"index": i, "rank": rank, "id": entry.get("id")})
        return targets

    def generate_archival_plan(self, memory_list):
        """
        Decides which memories to move to 'cold' storage vs 'delete'.
        """
        plan = {"cold_storage": [], "delete": []}
        for entry in memory_list:
            rank = self.rank_memory_importance(entry)
            if rank < 0.1:
                plan["delete"].append(entry.get("id"))
            elif rank < 0.3:
                plan["cold_storage"].append(entry.get("id"))
        return plan
