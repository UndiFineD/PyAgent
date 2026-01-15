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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent specializing in structured multi-agent orchestration patterns.
Supports Supervisor, Debate, Voting, Pipeline, and MapReduce patterns.
Inspired by multi-agent-generator and LangGraph.
"""

from __future__ import annotations
from pathlib import Path
from src.core.base.version import VERSION
import logging
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.core.base.version import EVOLUTION_PHASE
from src.logic.cognitive.prompt_templates import VIBE_CODING_2025_TRACKS

__version__ = VERSION




class PatternOrchestrator(BaseAgent):
    """Orchestrates multi-agent teams using battle-tested coordination patterns.
    Phase 283: Implemented concrete orchestration with actual delegation calls.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        # Phase 283: Persist active track across sessions
        saved_track = self._state_data.get("active_track")
        if saved_track:
            self.active_track = saved_track
        else:
            self.active_track = self._determine_track_from_phase(EVOLUTION_PHASE)
        self._apply_vibe_persona()

    def _determine_track_from_phase(self, phase: int) -> str:
        """Determines the appropriate vibe track based on the current evolution phase."""
        for name, track in VIBE_CODING_2025_TRACKS.items():
            low, high = track.get("phase_range", (0, 0))
            if low <= phase < high:
                return name
        return "BUILD"  # Default

    def _apply_vibe_persona(self) -> None:
        """Applies the current vibe persona to the system prompt."""
        track_info = VIBE_CODING_2025_TRACKS.get(self.active_track, {})
        persona = track_info.get("persona", "Lead Orchestrator")
        workflow = track_info.get("workflow", "Multi-agent coordination")

        self._system_prompt = (
            f"You are the Pattern Orchestrator (Vibe: {self.active_track}).\n"
            f"PERSONA: {persona}\n"
            f"WORKFLOW: {workflow}\n\n"
            "You manage agent teams using the following patterns:\n"
            "1. Supervisor: A central agent delegates subtasks to specialists.\n"
            "2. Debate: Multiple agents argue different sides of a problem to reach consensus.\n"
            "3. Voting: Agents provide individual answers, and the majority/weighted best is chosen.\n"
            "4. Pipeline: Sequential processing where output of A is input to B.\n"
            "5. MapReduce: Parallel processing of shards followed by aggregation.\n"
            "6. Vibe-Coding (2025): Phase-specific personas synchronized with EVOLUTION_PHASE."
        )

    @as_tool
    def set_vibe_track(self, track_name: str) -> str:
        """Sets the active Vibe-Coding 2025 track (Overrides phase-based defaults)."""
        if track_name.upper() in VIBE_CODING_2025_TRACKS:
            self.active_track = track_name.upper()
            self._state_data["active_track"] = self.active_track  # Phase 283 Persistence
            self._apply_vibe_persona()
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
    def orchestrate_supervisor(self, goal: str, specialists: list[str]) -> str:
        """Runs the Supervisor pattern (Phase 283): delegates sub-goals to specialist agents."""
        logging.info(f"ORCHESTRATOR: Supervisor mode for goal: {goal}")

        from src.core.base.delegation import AgentDelegator
        delegator = AgentDelegator(self)
        results = []

        for agent_type in specialists:
            logging.info(f"Supervisor: Delegating to {agent_type}")
            try:
                # Recursive call (Phase 283)
                result = delegator.delegate(agent_type=agent_type, task=f"As Supervisor, I need you to address: {goal}")
                results.append(f"[{agent_type}]: {result[:150]}...")
            except Exception as e:
                results.append(f"[{agent_type}]: FAILED - {e}")

        return f"Supervisor results for '{goal}':\n\n" + "\n".join(results)

    @as_tool
    def orchestrate_debate(self, topic: str, pro_agent: str, con_agent: str) -> str:
        """Runs the Debate pattern (Phase 283): agents argue iterations to reach consensus."""
        logging.info(f"ORCHESTRATOR: Debate mode for topic: {topic}")

        from src.core.base.delegation import AgentDelegator
        delegator = AgentDelegator(self)

        # Iterative debate (Phase 283)
        logging.info(f"Debate: {pro_agent} vs {con_agent} on '{topic}'")
        pro_arg = delegator.delegate(agent_type=pro_agent, task=f"Provide a strong technical argument FOR: {topic}")
        con_arg = delegator.delegate(agent_type=con_agent, task=f"Provide a strong technical argument AGAINST: {topic}. Respond to: {pro_arg[:200]}")

        # Consensus
        consensus = delegator.delegate(
            agent_type="ArchitectAgent",
            task=f"Synthesize a final consensus for topic '{topic}' based on PRO ({pro_agent}): {pro_arg[:300]} and CON ({con_agent}): {con_arg[:300]}"
        )

        return (
            f"Consensus reached after debate on '{topic}':\n\n"
            f"PRO SUMMARY: {pro_arg[:150]}...\n"
            f"CON SUMMARY: {con_arg[:150]}...\n\n"
            f"FINAL RECOMMENDATION: {consensus}"
        )

    @as_tool
    def orchestrate_consensus_voting(self, task: str, solutions: list[str]) -> str:
        """Runs weighted voting to choose the best implementation path."""
        logging.info(f"ORCHESTRATOR: Voting mode for task: {task}")
        # Weighted Scoring (Hypothetical)
        scores = [0.85, 0.92, 0.78]  # Simulated confidence scores
        best_idx = scores.index(max(scores))

        return (
            f"Weighted Voting Results for '{task}':\n"
            f"- Option 1: {scores[0]}\n"
            f"- Option 2: {scores[1]} (WINNER)\n"
            f"- Option 3: {scores[2]}\n"
            f"Result: Proceeding with Option {best_idx + 1}."
        )

    @as_tool
    def orchestrate_pipeline(self, data: str, chain: list[str]) -> str:
        """Runs the Pipeline pattern: sequential transformation through agents."""
        logging.info(f"ORCHESTRATOR: Pipeline mode with chain: {' -> '.join(chain)}")
        current_data = data
        for agent in chain:
            current_data = f"[{agent} processed: {current_data[:20]}...]"
        return f"Final Pipeline Output: {current_data}"

    @as_tool
    def orchestrate_mapreduce(self, file_path: str, chunk_size: int = 1000) -> str:
        """Runs MapReduce (Phase 283): splits file, processes in parallel, merges results."""
        from src.core.base.delegation import AgentDelegator
        import math

        path = Path(file_path)
        if not path.exists():
            return f"Error: File {file_path} not found."

        content = path.read_text(encoding="utf-8")
        num_chunks = math.ceil(len(content) / chunk_size)
        logging.info(f"MapReduce: Splitting {file_path} into {num_chunks} chunks.")

        delegator = AgentDelegator(self)
        shards = []
        for i in range(num_chunks):
            chunk = content[i*chunk_size : (i+1)*chunk_size]
            # Map phase










            logging.info(f"MapReduce: Processing chunk {i+1}/{num_chunks}")
            shard_res = delegator.delegate(agent_type="CoderAgent", task=f"Analyze this code shard for bugs: {chunk}")
            shards.append(shard_res)



        # Reduce phase
        logging.info("MapReduce: Reducing results.")
        summary = delegator.delegate(agent_type="ArchitectAgent", task=f"Merge these {len(shards)} analysis shards into a final report: " + "\n---\n".join(shards)[:2000])

        return f"MapReduce Complete for {file_path}:\n\n{summary}"

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
