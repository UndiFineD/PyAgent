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

"""
RL Selector for tool and agent routing.
Uses MDP history to select the most reliable candidate for a given goal.
"""

import logging
import random
from typing import List
from src.core.rl.mdp import MDP

logger = logging.getLogger(__name__)

class RLSelector:
    """
    Selects the best agent or tool using Reinforcement Learning.
    Tracks success/failure rates per (goal, candidate) pair.
    """

    def __init__(self, epsilon: float = 0.1):
        self.mdp = MDP()
        self.epsilon = epsilon  # Exploration rate

    def select_best_tool(self, goal: str, candidates: List[str]) -> str:
        """
        Selects the best tool among candidates for the given goal.
        Implements Epsilon-Greedy approach.
        """
        if not candidates:
            raise ValueError("No candidates provided for RL selection.")

        # Exploration phase
        if random.random() < self.epsilon:
            choice = random.choice(candidates)
            logger.info("RLSelector: Exploring random candidate '%s' for goal '%s'", choice, goal)
            return choice

        # Exploitation phase: Find candidate with highest expected reward
        best_candidate = candidates[0]
        max_reward = -float('inf')

        for candidate in candidates:
            # We treat (goal) as state and (candidate) as action
            reward = self.mdp.get_expected_reward(goal, candidate)
            if reward > max_reward:
                max_reward = reward
                best_candidate = candidate

        logger.info("RLSelector: Selected best candidate '%s' (Reward: %.2f) for goal '%s'", 
                    best_candidate, max_reward if max_reward != -float('inf') else 0.0, goal)
        return best_candidate

    def record_feedback(self, goal: str, candidate: str, success: bool, latency: float = 0.0):
        """Records the outcome of a selection to update the MDP models."""
        # Calculate reward: 1.0 for success, -1.0 for failure, with latency penalty
        reward = 1.0 if success else -1.0
        if success and latency > 0:
            reward -= min(0.5, latency / 10.0) # Penalty for slow success
            
        self.mdp.add_transition(
            state=goal,
            action=candidate,
            next_state="done",
            reward=reward,
            done=True
        )
        logger.debug("RLSelector: Recorded feedback for (%s, %s): Reward=%.2f", goal, candidate, reward)
