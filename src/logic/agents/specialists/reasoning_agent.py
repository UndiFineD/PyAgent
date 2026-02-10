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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Reasoning agent.py module.
"""
# ReasoningAgent: Recursive and Deep Thinking Agent - Phase 319 Enhanced

from __future__ import annotations

import contextlib
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.core.base.common.sharding_core import ShardingCore
from src.core.base.common.config_core import ConfigCore

__version__ = VERSION


class ReasoningStrategy(Enum):
    """Strategies for deep reasoning and logical deduction."""
    CHAIN_OF_THOUGHT = "cot"
    TREE_OF_THOUGHT = "tot"
    SELF_CONSISTENCY = "sc"
    REFLECTION = "reflection"
    DEBATE = "debate"


@dataclass
class ThoughtNode:
    """Represents a single thought in the reasoning tree."""

    content: str
    depth: int
    score: float = 0.0
    children: List["ThoughtNode"] = field(default_factory=list)
    parent: Optional["ThoughtNode"] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# pylint: disable=too-many-ancestors
class ReasoningAgent(BaseAgent):
    """
    Agent specializing in long-context reasoning, recursive chain-of-thought,
    and multi-step logical deduction with self-verification.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.config_manager = ConfigCore()
        shard_config = self.config_manager.load_config("sharding")
        self.sharding_engine = ShardingCore(cluster_size=shard_config.get("shard_count", 1))

        self._system_prompt = (
            "You are the Reasoning Agent. Your goal is to provide deep, recursive thoughts "
            "on complex problems. Use <thought> blocks to explore multiple hypotheses "
            "before arriving at a conclusion. Never settle for the first answer. "
            "Challenge your own assumptions and verify your logic."
        )
        self._reasoning_history: List[Dict[str, Any]] = []

    @as_tool
    async def distribute_reasoning_shard(self, task_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Splits a reasoning task across the cluster based on shard load.
        """
        node_id = self.sharding_engine.assign_workload([0.1, 0.5, 0.2]) # Mock loads
        logging.info(f"ReasoningAgent: Assigning shard task to Node {node_id}")
        return {"assigned_node": node_id, "status": "SHARD_ACTIVE"}

    @as_tool
    async def think_deeply(self, prompt: str, depth: int = 3, strategy: str = "cot") -> Dict[str, Any]:
        """Performs recursive reasoning on a given prompt with multiple strategies."""
        start_time = time.time()

        if strategy == "tot":
            result = await self._tree_of_thought(prompt, depth)
        elif strategy == "sc":
            result = await self._self_consistency(prompt, num_samples=depth)
        elif strategy == "reflection":
            result = await self._reflective_reasoning(prompt, depth)
        elif strategy == "debate":
            result = await self._internal_debate(prompt, rounds=depth)
        else:
            result = await self._chain_of_thought(prompt, depth)

        elapsed = time.time() - start_time
        self._reasoning_history.append(
            {"prompt": prompt[:100], "strategy": strategy, "depth": depth, "elapsed_s": elapsed}
        )

        return result

    async def _chain_of_thought(self, prompt: str, depth: int) -> Dict[str, Any]:
        """Standard recursive chain-of-thought reasoning."""
        current_context = prompt
        thought_chain = []

        for i in range(depth):
            logging.info(f"ReasoningAgent: Chain depth {i + 1}/{depth}...")

            if i == 0:
                step_prompt = f"Problem: {current_context}\n\nLet me think through this step-by-step:"
            else:
                step_prompt = (
                    f"Building on my previous analysis:\n{current_context}\n\nLet me refine and extend this reasoning:"
                )

            response = await self.improve_content(step_prompt)
            thought_chain.append({"depth": i + 1, "thought": response})
            current_context = response

        # Final synthesis
        synthesis_prompt = (
            f"Based on my chain of reasoning:\n{current_context}\n\nProvide a clear, concise final answer:"
        )
        final_answer = await self.improve_content(synthesis_prompt)

        return {
            "strategy": "chain_of_thought",
            "depth": depth,
            "thought_chain": thought_chain,
            "final_answer": final_answer,
        }

    async def _tree_of_thought(self, prompt: str, breadth: int = 3) -> Dict[str, Any]:
        """Tree-of-Thought: explores multiple reasoning paths."""
        root = ThoughtNode(content=prompt, depth=0)

        # Generate initial thoughts
        branch_prompt = (
            f"Problem: {prompt}\n\nGenerate {breadth} distinct approaches to "
            "solve this problem. Format each as a separate paragraph."
        )
        branches_response = await self.improve_content(branch_prompt)
        branches = [b.strip() for b in branches_response.split("\n\n") if b.strip()][:breadth]

        for branch in branches:
            child = ThoughtNode(content=branch, depth=1, parent=root)
            root.children.append(child)

            # Evaluate each branch
            eval_prompt = f"Evaluate this approach:\n{branch}\n\nRate its promise (1-10) and explain briefly."
            eval_response = await self.improve_content(eval_prompt)
            child.score = 5.0
            with contextlib.suppress(Exception):
                import re

                score_match = re.search(r"\b(\d+)\b", eval_response)
                if score_match:
                    child.score = float(score_match.group(1))
            child.metadata["evaluation"] = eval_response

        # Select best branch
        best_child = max(root.children, key=lambda c: c.score) if root.children else None

        if best_child:
            # Develop best branch further
            develop_prompt = (
                f"Develop this promising approach further:\n{best_child.content}\n\n"
                "Provide detailed reasoning and solution."
            )
            developed = await self.improve_content(develop_prompt)
            best_child.metadata["developed"] = developed

        return {
            "strategy": "tree_of_thought",
            "branches": [{"content": c.content, "score": c.score} for c in root.children],
            "best_path": best_child.content if best_child else "",
            "final_answer": best_child.metadata.get("developed", "") if best_child else "",
        }

    async def _self_consistency(self, prompt: str, num_samples: int = 5) -> Dict[str, Any]:
        """Self-Consistency: generate multiple solutions and vote."""
        solutions = []

        for i in range(num_samples):
            logging.info(
                "ReasoningAgent: Self-consistency sample %d/%d...",
                i + 1,
                num_samples,
            )
            solve_prompt = (
                f"Problem: {prompt}\n\n"
                "Provide a complete solution with final answer clearly marked."
            )
            solution = await self.improve_content(solve_prompt)
            solutions.append(solution)

        # Voting/consensus
        vote_prompt = (
            f"Given these {num_samples} solutions to the same problem:\n\n"
            + "\n---\n".join([f"Solution {i + 1}: {s[:500]}" for i, s in enumerate(solutions)])
            + "\n\nDetermine the most common/correct answer by majority consensus."
        )
        consensus = await self.improve_content(vote_prompt)

        return {
            "strategy": "self_consistency",
            "num_samples": num_samples,
            "solutions": solutions,
            "consensus_answer": consensus,
        }

    async def _reflective_reasoning(self, prompt: str, iterations: int = 3) -> Dict[str, Any]:
        """Reflection: generate, critique, and refine."""
        current_solution = ""
        reflections = []

        for i in range(iterations):
            if i == 0:
                gen_prompt = f"Problem: {prompt}\n\nProvide your initial solution:"
            else:
                gen_prompt = f"Based on this critique:\n{reflections[-1]}\n\nRevise and improve your solution:"

            current_solution = await self.improve_content(gen_prompt)

            if i < iterations - 1:
                critique_prompt = (
                    f"Critically analyze this solution:\n{current_solution}\n\n"
                    "Identify flaws, gaps, or improvements needed."
                )
                critique = await self.improve_content(critique_prompt)
                reflections.append(critique)

        return {
            "strategy": "reflection",
            "iterations": iterations,
            "reflections": reflections,
            "final_solution": current_solution,
        }

    async def _internal_debate(self, prompt: str, rounds: int = 3) -> Dict[str, Any]:
        """Internal Debate: argue for and against."""
        debate_log = []

        pro_prompt = f"Problem: {prompt}\n\nArgue FOR the most obvious solution. Make your case strongly."
        pro_position = await self.improve_content(pro_prompt)
        debate_log.append({"side": "pro", "argument": pro_position})

        for r in range(rounds):
            con_prompt = f"Counter this argument:\n{debate_log[-1]['argument']}\n\nProvide a strong rebuttal."
            rebuttal = await self.improve_content(con_prompt)
            debate_log.append({"side": "con" if r % 2 == 0 else "pro", "argument": rebuttal})

        synthesis_prompt = (
            f"Given this debate:\n{debate_log}\n\nSynthesize the best conclusion considering all arguments."
        )
        synthesis = await self.improve_content(synthesis_prompt)

        return {"strategy": "debate", "rounds": rounds, "debate_log": debate_log, "synthesis": synthesis}

    @as_tool
    async def verify_reasoning(self, claim: str, reasoning: str) -> Dict[str, Any]:
        """Verifies if the reasoning correctly supports the claim."""
        verify_prompt = (
            f"Claim: {claim}\n\n"
            f"Reasoning: {reasoning}\n\n"
            "Does this reasoning logically support the claim? "
            "Identify any logical fallacies or gaps. Rate validity 1-10."
        )
        verification = await self.improve_content(verify_prompt)

        import re

        score_match = re.search(r"\b(\d+)\b", verification)
        validity_score = float(score_match.group(1)) if score_match else 5.0

        return {
            "claim": claim,
            "validity_score": validity_score,
            "analysis": verification,
            "is_valid": validity_score >= 7.0,
        }
