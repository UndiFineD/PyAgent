import time
import logging
from typing import Dict, List, Any

class IntelligenceOrchestrator:
    """
    Swarm Collective Intelligence: Analyzes actions and insights from 
    multiple agents to find emerging patterns and synthesize "meta-knowledge".
    Optimized for Phase 108 with high-performance local AI (vLLM) integration.
    """
    def __init__(self, fleet_manager: Any) -> None:
        self.fleet_manager = fleet_manager
        self.insight_pool = []
        self.patterns = []
        # Phase 108: Native AI for collective synthesis
        import requests
        from src.classes.backend.LLMClient import LLMClient
        self.ai = LLMClient(requests, workspace_root=str(fleet_manager.workspace_root))

    def contribute_insight(self, agent_name: str, insight: str, confidence: float) -> None:
        """Contributes a single agent's insight to the swarm pool."""
        self.insight_pool.append({
            "agent": agent_name,
            "insight": insight,
            "confidence": confidence,
            "timestamp": time.time()
        })

    def synthesize_collective_intelligence(self) -> List[str]:
        """Analyzes the pool and recent SQL lessons using local AI to find shared patterns."""
        combined_insights = [f"- {i['agent']}: {i['insight']}" for i in self.insight_pool[-20:]]
        
        # Phase 108: Ingest lessons from Relational Metadata
        if hasattr(self.fleet_manager, 'sql_metadata'):
            try:
                sql_lessons = self.fleet_manager.sql_metadata.get_intelligence_summary()
                for lesson in sql_lessons[:5]:
                    combined_insights.append(f"- RELATIONAL_LESSON: {lesson.get('sample_lesson')} (Category: {lesson.get('category')})")
            except Exception as e:
                logging.debug(f"Intelligence: Failed to ingest SQL lessons: {e}")

        if not combined_insights:
            return []

        # If we have a small pool, use fast term frequency
        if len(combined_insights) < 3:
            return ["Insufficient data for deep synthesis."]

        # Phase 108: Deep AI Synthesis (Synthesize trillion-parameter scale insights)
        pool_text = "\n".join(combined_insights)
        prompt = f"Analyze these swarm insights and relational lessons. Synthesize the top 3 high-level patterns or warnings:\n{pool_text}"
        
        try:
            summary = self.ai.smart_chat(prompt, system_prompt="You are a Swarm Intelligence Synthesizer. Be concise and technical.")
            if summary:
                emerging_insights = [s.strip() for s in summary.split("\n") if s.strip() and len(s) > 10]
                self.patterns = emerging_insights
                
                # Record the synthesis to SQL Metadata (Phase 108)
                if hasattr(self.fleet_manager, 'sql_metadata'):
                    self.fleet_manager.sql_metadata.record_lesson(
                        interaction_id=f"swarm_{int(time.time())}",
                        text=summary,
                        category="Collective Intelligence"
                    )
                return emerging_insights
        except Exception as e:
            logging.error(f"Intelligence: AI Synthesis failed: {e}")

        return []

    def get_intelligence_report(self) -> Dict[str, Any]:
        """Summarizes the current state of collective knowledge."""
        return {
            "insights_collected": len(self.insight_pool),
            "patterns_identified": len(self.patterns),
            "top_patterns": self.patterns[:3]
        }

    def get_actionable_improvement_tasks(self) -> List[Dict[str, Any]]:
        """
        Extracts specific, actionable coding tasks from the synthesized intelligence.
        Designed for the SelfImprovementOrchestrator to ingest (Phase 108).
        """
        tasks = []
        for pattern in self.patterns:
            # Look for keywords that suggest code changes
            if any(k in pattern.lower() for k in ["error", "failure", "bottleneck", "reinitialize", "missing"]):
                # Use AI to turn a general pattern into a specific coding goal
                prompt = f"Given this swarm intelligence pattern: '{pattern}', suggest a single technical improvement task (e.g., 'Add validation for X in Y.py'). Respond only with the task description."
                task_desc = self.ai.smart_chat(prompt, system_prompt="You are a Technical Lead. Convert patterns into actionable Jira-style tasks.")
                if task_desc and len(task_desc) > 10:
                    tasks.append({
                        "id": f"TASK_{int(time.time())}_{len(tasks)}",
                        "description": task_desc,
                        "origin_pattern": pattern,
                        "severity": "High" if "error" in pattern.lower() else "Medium"
                    })
        return tasks
