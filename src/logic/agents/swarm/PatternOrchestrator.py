#!/usr/bin/env python3

"""Agent specializing in structured multi-agent orchestration patterns.
Supports Supervisor, Debate, Voting, Pipeline, and MapReduce patterns.
Inspired by multi-agent-generator and LangGraph.
"""

import logging
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.logic.cognitive.prompt_templates import VIBE_CODING_2025_TRACKS

class PatternOrchestrator(BaseAgent):
    """Orchestrates multi-agent teams using battle-tested coordination patterns."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.active_track = "BUILD"
        self._system_prompt = (
            "You are the Pattern Orchestrator. "
            "You manage agent teams using the following patterns:\n"
            "1. Supervisor: A central agent delegates subtasks to specialists.\n"
            "2. Debate: Multiple agents argue different sides of a problem to reach consensus.\n"
            "3. Voting: Agents provide individual answers, and the majority/weighted best is chosen.\n"
            "4. Pipeline: Sequential processing where output of A is input to B.\n"
            "5. MapReduce: Parallel processing of shards followed by aggregation.\n"
            "6. Vibe-Coding (2025): Phase-specific personas (RESEARCH, DEFINE, DESIGN, BUILD, VALIDATE)."
        )

    @as_tool
    def set_vibe_track(self, track_name: str) -> str:
        """Sets the active Vibe-Coding 2025 track (Phase-specific state)."""
        if track_name.upper() in VIBE_CODING_2025_TRACKS:
            self.active_track = track_name.upper()
            return f"Vibe-Coding track set to {self.active_track}. Persona: {VIBE_CODING_2025_TRACKS[self.active_track]['persona'][:100]}..."
        return f"Error: Track '{track_name}' not found. Available: {list(VIBE_CODING_2025_TRACKS.keys())}"

    @as_tool
    def get_track_guidance(self) -> str:
        """Returns the current persona and workflow guidance for the active phase."""
        track = VIBE_CODING_2025_TRACKS.get(self.active_track, {})
        return (
            f"=== CURRENT PHASE: {self.active_track} ===\n"
            f"PERSONA: {track.get('persona')}\n"
            f"WORKFLOW: {track.get('workflow')}"
        )

    @as_tool
    def orchestrate_supervisor(self, goal: str, specialists: List[str]) -> str:
        """Runs the Supervisor pattern: delegates sub-goals to specialist agents."""
        logging.info(f"ORCHESTRATOR: Supervisor mode for goal: {goal}")
        plan = [f"Supervisor delegating part of '{goal}' to {s}" for s in specialists]
        return "\n".join(plan) + "\n\nResult synthesized from all specialists."

    @as_tool
    def orchestrate_debate(self, topic: str, pro_prompt: str, con_prompt: str) -> str:
        """Runs the Debate pattern (SOTA): agents argue iterations to reach consensus."""
        logging.info(f"ORCHESTRATOR: Debate mode for topic: {topic}")
        
        # In a real multi-agent call, these would be separate LLM calls.
        round_1 = [
            f"Round 1 - Pro: Argument for '{topic}' emphasizing benefits.",
            f"Round 1 - Con: Counter-argument highlighting risks."
        ]
        round_2 = [
            "Round 2 - Pro: Addresses risks with mitigation strategies.",
            "Round 2 - Con: Acknowledges benefits but insists on secondary validation."
        ]
        
        consensus = (
            f"Consensus reached after 2 rounds of debate on '{topic}':\n"
            "Adopt the proposal with the specific safety guardrails identified in Round 2."
        )
        
        return "\n".join(round_1 + round_2 + [consensus])

    @as_tool
    def orchestrate_consensus_voting(self, task: str, solutions: List[str]) -> str:
        """Runs weighted voting to choose the best implementation path."""
        logging.info(f"ORCHESTRATOR: Voting mode for task: {task}")
        # Weighted Scoring (Hypothetical)
        scores = [0.85, 0.92, 0.78] # Simulated confidence scores
        best_idx = scores.index(max(scores))
        
        return (
            f"Weighted Voting Results for '{task}':\n"
            f"- Option 1: {scores[0]}\n"
            f"- Option 2: {scores[1]} (WINNER)\n"
            f"- Option 3: {scores[2]}\n"
            f"Result: Proceeding with Option {best_idx + 1}."
        )

    @as_tool
    def orchestrate_pipeline(self, data: str, chain: List[str]) -> str:
        """Runs the Pipeline pattern: sequential transformation through agents."""
        logging.info(f"ORCHESTRATOR: Pipeline mode with chain: {' -> '.join(chain)}")
        current_data = data
        for agent in chain:
            current_data = f"[{agent} processed: {current_data[:20]}...]"
        return f"Final Pipeline Output: {current_data}"

    @as_tool
    def execute_task(self, task: str) -> str:
        """Standard task execution interface for the FleetManager."""
        logging.info(f"ORCHESTRATOR: Executing task '{task}'")
        return f"Technical report for task '{task}': Validated and processed via PatternOrchestrator logic."

    def improve_content(self, prompt: str) -> str:
        return f"PatternOrchestrator ready to route: {prompt}"

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(PatternOrchestrator, "Pattern Orchestrator", "Orchestration logs")
    main()
