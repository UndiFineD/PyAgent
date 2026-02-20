#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Mdp.py module.
"""

"""

# Markov Decision Process (MDP) Implementation - Phase 319 Enhanced

try:
    import logging
except ImportError:
    import logging

try:
    import random
except ImportError:
    import random

try:
    from collections import defaultdict
except ImportError:
    from collections import defaultdict

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import Any, Dict, List, Tuple
except ImportError:
    from typing import Any, Dict, List, Tuple


logger = logging.getLogger(__name__)


@dataclass
class Transition:
"""
Represents a state transition with optional metadata.""
state: Any
    action: Any
    next_state: Any
    reward: float
    done: bool
    timestamp: float = 0.0
    priority: float = 1.0  # For prioritized experience replay


@dataclass
class ExperienceReplayBuffer:
"""
Circular buffer for storing and sampling transitions.""
capacity: int = 10000
    buffer: List[Transition] = field(default_factory=list)
    position: int = 0

    def push(self, transition: Transition) -> None:
"""
Adds a transition to the buffer.""
if len(self.buffer) < self.capacity:
            self.buffer.append(transition)
        else:
            self.buffer[self.position] = transition
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size: int) -> List[Transition]:
"""
Randomly samples a batch of transitions.""
return random.sample(self.buffer, min(batch_size, len(self.buffer)))

    def prioritized_sample(self, batch_size: int, alpha: float = 0.6) -> List[Transition]:
"""
Samples with priority weighting.""
priorities = [t.priority**alpha for t in self.buffer]
        total = sum(priorities)
        probs = [p / total for p in priorities]
        indices = random.choices(range(len(self.buffer)), weights=probs, k=min(batch_size, len(self.buffer)))
        return [self.buffer[i] for i in indices]



class MDP:
"""
Models the decision-making process for agents.
    Implements: S (States), A (Actions), P(s'|s,a) (Transition Dynamics), R(s,a) (Rewards)'    Enhanced with value iteration, policy extraction, and model-based planning.
"""
def __init__(self, gamma: float = 0.99) -> None:
        self.transitions: List[Transition] = []
        self.states: List[Any] = []
        self.actions: List[Any] = []
        self.gamma = gamma  # Discount factor
        self.value_function: Dict[Any, float] = defaultdict(float)
        self.policy: Dict[Any, Any] = {}
        self.transition_model: Dict[Tuple[Any, Any], Dict[Any, int]] = defaultdict(lambda: defaultdict(int))
        self.reward_model: Dict[Tuple[Any, Any], List[float]] = defaultdict(list)
        self.replay_buffer = ExperienceReplayBuffer()

    def add_transition(
        self, state: Any, action: Any, next_state: Any, reward: float, done: bool, timestamp: float = 0.0
    ) -> None:
"""
Records a transition and updates internal models.""
import time

        t = Transition(state, action, next_state, reward, done, timestamp or time.time())
        self.transitions.append(t)
        self.replay_buffer.push(t)

        if state not in self.states:
            self.states.append(state)
        if next_state not in self.states:
            self.states.append(next_state)
        if action not in self.actions:
            self.actions.append(action)

        # Update transition model P(s'|s,a)
        self.transition_model[(state, action)][next_state] += 1
        # Update reward model R(s,a)
        self.reward_model[(state, action)].append(reward)

    def get_transition_probability(self, state: Any, action: Any, next_state: Any) -> float:
"""
Returns P(s'|s,a) based on observed transitions.""
transitions = self.transition_model[(state, action)]
        total = sum(transitions.values())
        if total == 0:
            return 0.0
        return transitions[next_state] / total

    def get_expected_reward(self, state: Any, action: Any) -> float:
"""
Returns E[R(s,a)] based on observed rewards.""
rewards = self.reward_model[(state, action)]
        return sum(rewards) / len(rewards) if rewards else 0.0

    def value_iteration(self, theta: float = 1e-6, max_iterations: int = 1000) -> int:
"""
Computes optimal value function using dynamic programming.""
for iteration in range(max_iterations):
            delta = 0.0
            for state in self.states:
                v = self.value_function[state]
                # Bellman optimality equation
                action_values = []
                for action in self.actions:
                    expected_value = 0.0
                    for next_state in self.states:
                        p = self.get_transition_probability(state, action, next_state)
                        r = self.get_expected_reward(state, action)
                        expected_value += p * (r + self.gamma * self.value_function[next_state])
                    action_values.append(expected_value)

                self.value_function[state] = max(action_values) if action_values else 0.0
                delta = max(delta, abs(v - self.value_function[state]))

            if delta < theta:
                logger.info(f"MDP: Value iteration converged in {iteration + 1} iterations.")
                return iteration + 1

        logger.warning(f"MDP: Value iteration did not converge within {max_iterations} iterations.")
        return max_iterations

    def extract_policy(self) -> Dict[Any, Any]:
"""
Extracts greedy policy from value function.""
for state in self.states:
            best_action = None
            best_value = -float("inf")
            for action in self.actions:
                expected_value = 0.0
                for next_state in self.states:
                    p = self.get_transition_probability(state, action, next_state)
                    r = self.get_expected_reward(state, action)
                    expected_value += p * (r + self.gamma * self.value_function[next_state])
                if expected_value > best_value:
                    best_value = expected_value
                    best_action = action
            self.policy[state] = best_action
        return self.policy

    def get_reward_sum(self) -> float:
"""
Returns the sum of all rewards in transitions.""
return sum(t.reward for t in self.transitions)

    def get_discounted_return(self) -> float:
"""
Computes discounted cumulative return.""
total = 0.0
        for i, t in enumerate(self.transitions):
            total += (self.gamma**i) * t.reward
        return total

    def to_dict(self) -> Dict[str, Any]:
        ""
Returns a dictionary representation of the MDP.""
return {
            "state_count": len(self.states),
            "action_count": len(self.actions),
            "transition_count": len(self.transitions),
            "total_reward": self.get_reward_sum(),
            "discounted_return": self.get_discounted_return(),
            "gamma": self.gamma,
            "replay_buffer_size": len(self.replay_buffer.buffer),
        }
