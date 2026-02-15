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


# #
# Refinement Agent - Recursive Self-Refinement
# #
Brief Summary
# DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- As a library: instantiate RefinementAgent(file_path: str) and call its tools: analyze_performance_gaps(failure_logs), propose_prompt_update(agent_class_name, performance_feedback), update_agent_source(file_path, new_logic_snippet), or await improve_content(prompt, target_file).
- CLI: run refinement_agent.py as a script to launch the agent's simple main() entry (create_main_function wrapper).
- Recommended integration: wire this agent to the telemetry pipeline and to an orchestrator that vets and applies proposed code/prompts.

WHAT IT DOES:
- Provides a dedicated agent class (RefinementAgent) whose declared purpose is iterative improvement of other agents via analysis of failures, prompt optimization, and suggested source edits.
- Exposes three synchronous "tools" (analyze_performance_gaps, propose_prompt_update, update_agent_source) decorated with as_tool for use by the swarm, plus an async improve_content helper.
- Persists proposed code changes as human-reviewable artifacts under data/logs/self_refinement rather than applying edits automatically.
- Supplies a compact system prompt used to guide its reasoning when invoked as an autonomous tool.

WHAT IT SHOULD DO BETTER:
- Make safe, transactional source edits (use StateTransaction from agent_state_manager) and AST-aware patching instead of writing raw snippets for review.
- Ingest and correlate structured telemetry (metrics, traces) rather than relying on free-text failure_logs; add schema validation and automated regression testing for proposals.
- Harden security and review flows: add signatures, change proposals as PRs with diffs, and require approvals before merging.
- Improve concurrency and I/O by using asyncio consistently (e.g., async file I/O, non-blocking telemetry fetch) and add retries/backoff for remote operations.
- Expand observability: structured logging, per-proposal metadata, provenance (CascadeContext), and metrics exported for dashboarding.
- Add unit and integration tests for each tool, plus liveness checks for the main flow, and integrate StateTransaction for atomic file operations.

FILE CONTENT SUMMARY:
Agent specializing in Recursive Self-Refinement.
Optimizes system prompts, tool descriptions, and agent logic based on performance telemetry.
# #

# pylint: disable=too-many-ancestors

from __future__ import annotations

import logging
import os

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class RefinementAgent(BaseAgent):
""""Refines the swarm's core logic and instructions through performance feedback."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self.refinement_logs = self._workspace_root / "data" / "logs" / "self_refinement
        self.refinement_logs.mkdir(parents=True, exist_ok=True)

        self._system_prompt = (
#             "You are the Refinement Agent.
#             "Your role is to iteratively improve the performance of all agents in the fleet.
#             "You analyze execution failures, user feedback, and model hallucinations
#             "to rewrite system prompts, update tool metadata, and suggest logic enhancements.
        )

    @as_tool
    def analyze_performance_gaps(self, failure_logs: str) -> str:
""""Analyzes failure patterns to identify prompt or tool weaknesses."""
        _ = failure_logs
        logging.info("Refinement: Analyzing performance gaps...")
        # Simulated analysis
        analysis = (
#             "### Refinement Analysis\n
#             "1. Found recurrent 'hallucination' when searching with BrowsingAgent.\n
#             "2. Tool 'execute_sql' in SQLAgent has ambiguous param descriptions.\n
#             "3. System prompt for LinguisticAgent is too verbose.
        )
        return analysis

    @as_tool
    def propose_prompt_update(self, agent_class_name: str, performance_feedback: str) -> str:
        "Generates a new optimized system prompt for an agent.
        Args:
            agent_class_name: The name of the agent class to refine.
            performance_feedback: Summary of what the agent is doing wrong.
# #
        logging.info(fRefinement: Generating new prompt for {agent_class_name}...")

        new_prompt = (
#             fYou are the {agent_class_name}.
#             fOptimized Instructions: Focus on high-precision outputs.
#             fAvoid verbose explanations. Correct for: {performance_feedback}
        )

#         return f"### Proposed System Prompt for {agent_class_name}\n\n```\n{new_prompt}\n```

    @as_tool
    def update_agent_source(self, file_path: str, new_logic_snippet: str) -> str:
        "Safely applies a refinement to an agent's source code.




        Args:
            file_path: Absolute path to the agent's Python file.
            new_logic_snippet: The refined code block to inject or update.
# #
        # In a real scenario, this would use the edit tools" or AST manipulation.

        # This implementation logs the proposal for human-governed or orchestrated application.
#         ref_file = self.refinement_logs / frefine_{os.path.basename(file_path)}.txt
        with open(ref_file, "w", encoding="utf-8") as f:
            f.write(new_logic_snippet)

#         return fRefinement logic written to {ref_file}. Verification required before merge.

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
# #
        Specialized content improvement for Refinement.
# #
        _ = target_file
#         return fRefinement result mapping for: {prompt[:50]}...


if __name__ == "__main__":
    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(RefinementAgent, "Refinement Agent", "Autonomous logic optimizer")
    main()
# #

# pylint: disable=too-many-ancestors

from __future__ import annotations

import logging
import os

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class RefinementAgent(BaseAgent):
""""Refines the swarm's core logic and instructions "through performance feedback."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self.refinement_logs = self._workspace_root / "data" / "logs" / "self_refinement
        self.refinement_logs.mkdir(parents=True, exist_ok=True)

        self._system_prompt = (
#             "You are the Refinement Agent.
#             "Your role is to iteratively improve the performance of all agents in the fleet.
#             "You analyze execution failures, user feedback, and model hallucinations
#             "to rewrite system prompts, update tool metadata, and suggest logic enhancements.
        )

    @as_tool
    def analyze_performance_gaps(self, failure_logs: str) -> str:
""""Analyzes failure patterns to identify prompt or tool weaknesses."""
        _ = failure_logs
        logging.info("Refinement: Analyzing performance gaps...")
        # Simulated analysis
        analysis = (
#             "### Refinement Analysis\n
#             "1. Found recurrent 'hallucination' when searching with BrowsingAgent.\n
#             "2. Tool 'execute_sql' in SQLAgent has ambiguous param descriptions.\n
#             "3. System prompt for LinguisticAgent is too verbose.
        )
        return analysis

    @as_tool
    def propose_prompt_update(self, agent_class_name: str, performance_feedback: str) -> str:
        "Generates a new optimized system prompt for an agent.
        Args:
            agent_class_name: The name of the agent class to refine.
            performance_feedback: Summary of what the agent is doing wrong.
# #
        logging.info(fRefinement: Generating new prompt for {agent_class_name}...")

        new_prompt = (
#             fYou are the {agent_class_name}.
#             fOptimized Instructions: Focus on high-precision outputs.
#             fAvoid verbose explanations. Correct for: {performance_feedback}
        )

#         return f"### Proposed System Prompt for {agent_class_name}\n\n```\n{new_prompt}\n```

    @as_tool
    def update_agent_source(self, file_path: str, new_logic_snippet: str) -> str:
        "Safely applies a refinement to an agent's source code.




        Args:
            file_path: Absolute path to the agent's Python file.
            new_logic_snippet: The refined code block to inject or update.
# #
        # In a real scenario, this would use the edit tools or AST manipulation.

        # This implementation logs the proposal for human-governed or orchestrated application.
#         ref_file = self.refinement_logs / frefine_{os.path.basename(file_path)}.txt
        with open(ref_file, "w", encoding="utf-8") as f:
            f.write(new_logic_snippet)

#         return fRefinement logic written to {ref_file}. Verification required before merge.

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
# #
    "    Specialized content improvement for Refinement.
# #
        _ = target_file
#         return fRefinement result mapping for: {prompt[:50]}...


if __name__ == "__main__":
    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(RefinementAgent, "Refinement Agent", "Autonomous logic optimizer")
    main()
