import time
import json
import random
from pathlib import Path

class MemoryReplayAgent:
    """
    Simulates "sleep cycles" for agents where they replay episodic memories
    to consolidate knowledge, identify patterns, and prune low-utility data.
    """
    def __init__(self, workspace_path) -> None:
        self.workspace_path = Path(workspace_path)
        self.is_sleeping = False
        self.replay_buffer = []
        self.consolidated_insights = []

    def start_sleep_cycle(self, episodic_memories):
        """
        Begins a period of autonomous memory replay and consolidation.
        """
        self.is_sleeping = True
        results = {
            "start_ts": time.time(),
            "memories_processed": len(episodic_memories),
            "consolidated": 0,
            "pruned": 0
        }

        for memory in episodic_memories:
            # Simulate "dreaming" - re-evaluating memory importance
            utility_score = self._evaluate_utility(memory)
            
            if utility_score > 0.8:
                self.consolidated_insights.append({
                    "insight": f"Pattern found in {memory.get('action', 'task')}",
                    "confidence": utility_score,
                    "original_id": memory.get('id')
                })
                results["consolidated"] += 1
            elif utility_score < 0.2:
                results["pruned"] += 1
                
        self.is_sleeping = False
        results["end_ts"] = time.time()
        results["duration"] = results["end_ts"] - results["start_ts"]
        return results

    def _evaluate_utility(self, memory):
        """
        Assigns a utility score to a memory based on simulated heuristic.
        """
        # In real life, this might involve an LLM summarizing or looking for repetition
        score = random.uniform(0, 1)
        content = str(memory.get("content", "")).lower()
        
        # High value on errors and fixes
        if "error" in content or "fix" in content or "success" in content:
            score = min(1.0, score + 0.3)
            
        return score

    def get_dream_log(self):
        """
        Returns a log of patterns discovered during sleep cycles.
        """
        return {
            "insights_count": len(self.consolidated_insights),
            "latest_insights": self.consolidated_insights[-5:]
        }
