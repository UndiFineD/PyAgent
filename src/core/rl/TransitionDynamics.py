# Copyright 2026 PyAgent Authors
# Transition Dynamics for Markov Decision Processes - Phase 319 Enhanced

from __future__ import annotations
from typing import Any, Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
import random
import math
import logging

@dataclass
class TransitionRecord:
    """Records a single state transition with metadata."""
    state: Any
    action: Any
    next_state: Any
    reward: float = 0.0
    done: bool = False
    timestamp: int = 0

@dataclass
class StateActionStats:
    """Statistics for a state-action pair."""
    visit_count: int = 0
    total_reward: float = 0.0
    next_state_counts: Dict[Any, int] = field(default_factory=dict)
    
    @property
    def avg_reward(self) -> float:
        return self.total_reward / self.visit_count if self.visit_count > 0 else 0.0

class TransitionDynamics:
    """
    Models the probability of moving from state S to S' given action A.
    Supports empirical estimation, model learning, and uncertainty quantification.
    """

    def __init__(self, smoothing: float = 0.1):
        # (state, action) -> StateActionStats
        self._stats: Dict[Tuple[Any, Any], StateActionStats] = {}
        # All observed states and actions
        self._states: Set[Any] = set()
        self._actions: Set[Any] = set()
        # Transition history for replay
        self._history: List[TransitionRecord] = []
        self._smoothing = smoothing  # Laplace smoothing parameter
        self._step_counter = 0

    @property
    def state_space_size(self) -> int:
        return len(self._states)

    @property
    def action_space_size(self) -> int:
        return len(self._actions)

    @property
    def transition_count(self) -> int:
        return len(self._history)

    def record_transition(
        self, 
        state: Any, 
        action: Any, 
        next_state: Any,
        reward: float = 0.0,
        done: bool = False
    ) -> None:
        """Records a transition and updates statistics."""
        key = (state, action)
        
        # Update or create stats
        if key not in self._stats:
            self._stats[key] = StateActionStats()
        
        stats = self._stats[key]
        stats.visit_count += 1
        stats.total_reward += reward
        stats.next_state_counts[next_state] = stats.next_state_counts.get(next_state, 0) + 1
        
        # Track states and actions
        self._states.add(state)
        self._states.add(next_state)
        self._actions.add(action)
        
        # Record to history
        self._step_counter += 1
        self._history.append(TransitionRecord(
            state=state,
            action=action,
            next_state=next_state,
            reward=reward,
            done=done,
            timestamp=self._step_counter
        ))

    def get_transition_probability(self, state: Any, action: Any, next_state: Any) -> float:
        """Returns P(s'|s, a) with Laplace smoothing."""
        key = (state, action)
        
        if key not in self._stats:
            # Uniform if never observed
            return 1.0 / len(self._states) if self._states else 0.0
        
        stats = self._stats[key]
        count = stats.next_state_counts.get(next_state, 0)
        
        # Laplace smoothing
        num_next_states = len(stats.next_state_counts)
        smoothed_count = count + self._smoothing
        smoothed_total = stats.visit_count + self._smoothing * (num_next_states + 1)
        
        return smoothed_count / smoothed_total

    def get_transition_distribution(self, state: Any, action: Any) -> Dict[Any, float]:
        """Returns the full distribution over next states."""
        key = (state, action)
        
        if key not in self._stats:
            return {}
        
        stats = self._stats[key]
        total = stats.visit_count
        
        return {
            next_state: count / total
            for next_state, count in stats.next_state_counts.items()
        }

    def predict_next_state(self, state: Any, action: Any) -> Optional[Any]:
        """Stochastic prediction of the next state based on history."""
        key = (state, action)
        
        if key not in self._stats:
            return None
        
        stats = self._stats[key]
        candidates = stats.next_state_counts
        
        if not candidates:
            return None
        
        total = sum(candidates.values())
        r = random.uniform(0, total)
        upto = 0.0
        
        for s_prime, count in candidates.items():
            upto += count
            if upto >= r:
                return s_prime
        
        return list(candidates.keys())[-1]

    def predict_expected_reward(self, state: Any, action: Any) -> float:
        """Predicts the expected immediate reward for a state-action pair."""
        key = (state, action)
        
        if key not in self._stats:
            return 0.0
        
        return self._stats[key].avg_reward

    def get_reachable_states(self, state: Any, depth: int = 1) -> Set[Any]:
        """Returns states reachable from a given state within N steps."""
        reachable = {state}
        frontier = {state}
        
        for _ in range(depth):
            new_frontier = set()
            for s in frontier:
                for action in self._actions:
                    key = (s, action)
                    if key in self._stats:
                        new_frontier.update(self._stats[key].next_state_counts.keys())
            frontier = new_frontier - reachable
            reachable.update(frontier)
        
        return reachable

    def compute_entropy(self, state: Any, action: Any) -> float:
        """Computes the entropy of the transition distribution (uncertainty measure)."""
        key = (state, action)
        
        if key not in self._stats:
            return 0.0
        
        stats = self._stats[key]
        total = stats.visit_count
        
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for count in stats.next_state_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log(p)
        
        return entropy

    def get_uncertainty(self, state: Any, action: Any) -> float:
        """Returns uncertainty score (0=certain, 1=max uncertainty)."""
        key = (state, action)
        
        if key not in self._stats:
            return 1.0  # Maximum uncertainty if never observed
        
        # Combine visit count and entropy
        stats = self._stats[key]
        visit_uncertainty = 1.0 / (1.0 + stats.visit_count)
        entropy = self.compute_entropy(state, action)
        max_entropy = math.log(len(stats.next_state_counts) + 1) if stats.next_state_counts else 1.0
        entropy_normalized = entropy / max_entropy if max_entropy > 0 else 0.0
        
        return (visit_uncertainty + entropy_normalized) / 2.0

    def get_visit_count(self, state: Any, action: Any) -> int:
        """Returns the number of times a state-action pair was visited."""
        key = (state, action)
        return self._stats[key].visit_count if key in self._stats else 0

    def most_likely_next_state(self, state: Any, action: Any) -> Optional[Any]:
        """Returns the most likely next state deterministically."""
        key = (state, action)
        
        if key not in self._stats or not self._stats[key].next_state_counts:
            return None
        
        return max(
            self._stats[key].next_state_counts.items(),
            key=lambda x: x[1]
        )[0]

    def get_transition_matrix(self, states: List[Any], action: Any) -> List[List[float]]:
        """Builds a transition probability matrix for a given action."""
        n = len(states)
        state_to_idx = {s: i for i, s in enumerate(states)}
        
        matrix = [[0.0] * n for _ in range(n)]
        
        for i, state in enumerate(states):
            dist = self.get_transition_distribution(state, action)
            for next_state, prob in dist.items():
                if next_state in state_to_idx:
                    matrix[i][state_to_idx[next_state]] = prob
        
        return matrix

    def sample_trajectory(self, start_state: Any, steps: int = 10) -> List[TransitionRecord]:
        """Samples a trajectory from the learned dynamics."""
        trajectory = []
        state = start_state
        
        for step in range(steps):
            # Choose random action
            action = random.choice(list(self._actions)) if self._actions else None
            if action is None:
                break
            
            next_state = self.predict_next_state(state, action)
            if next_state is None:
                break
            
            reward = self.predict_expected_reward(state, action)
            
            trajectory.append(TransitionRecord(
                state=state,
                action=action,
                next_state=next_state,
                reward=reward,
                done=False,
                timestamp=step
            ))
            
            state = next_state
        
        return trajectory

    def get_stats_summary(self) -> Dict[str, Any]:
        """Returns a summary of the transition dynamics."""
        return {
            "state_space_size": self.state_space_size,
            "action_space_size": self.action_space_size,
            "total_transitions": self.transition_count,
            "unique_state_action_pairs": len(self._stats),
            "avg_transitions_per_pair": (
                self.transition_count / len(self._stats) if self._stats else 0
            )
        }

    def clear(self) -> None:
        """Clears all recorded transitions."""
        self._stats.clear()
        self._states.clear()
        self._actions.clear()
        self._history.clear()
        self._step_counter = 0
