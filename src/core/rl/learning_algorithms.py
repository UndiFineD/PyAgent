# Copyright 2026 PyAgent Authors
# Reinforcement Learning Algorithms Implementation - Phase 319 Enhanced

from __future__ import annotations
import numpy as np
from typing import Any, List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import random
import logging

logger = logging.getLogger(__name__)

@dataclass
class PolicyGradientBuffer:
    """Stores trajectory data for policy gradient methods."""
    states: List[Any] = field(default_factory=list)
    actions: List[Any] = field(default_factory=list)
    rewards: List[float] = field(default_factory=list)
    log_probs: List[float] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    
    def clear(self):
        self.states.clear()
        self.actions.clear()
        self.rewards.clear()
        self.log_probs.clear()
        self.values.clear()
    
    def compute_returns(self, gamma: float = 0.99) -> List[float]:
        """Computes discounted returns."""
        returns = []
        G = 0
        for r in reversed(self.rewards):
            G = r + gamma * G
            returns.insert(0, G)
        return returns
    
    def compute_advantages(self, gamma: float = 0.99, lam: float = 0.95) -> List[float]:
        """Computes GAE (Generalized Advantage Estimation)."""
        advantages = []
        gae = 0
        values = self.values + [0]  # Bootstrap with 0
        for t in reversed(range(len(self.rewards))):
            delta = self.rewards[t] + gamma * values[t + 1] - values[t]
            gae = delta + gamma * lam * gae
            advantages.insert(0, gae)
        return advantages

class LearningAlgorithms:
    """Standard RL algorithms for agent policy improvement."""

    @staticmethod
    def q_learning_update(
        q_table: Dict[Tuple[str, str], float], 
        state: str, 
        action: str, 
        reward: float, 
        next_state: str, 
        actions: List[str],
        alpha: float = 0.1, 
        gamma: float = 0.99
    ) -> float:
        """Standard Q-Learning update: Q(s,a) <- Q(s,a) + α[r + γ max_a' Q(s',a') - Q(s,a)]"""
        old_val = q_table.get((state, action), 0.0)
        next_max = max([q_table.get((next_state, a), 0.0) for a in actions], default=0.0)
        new_val = old_val + alpha * (reward + gamma * next_max - old_val)
        q_table[(state, action)] = new_val
        return new_val

    @staticmethod
    def sarsa_update(
        q_table: Dict[Tuple[str, str], float],
        state: str,
        action: str,
        reward: float,
        next_state: str,
        next_action: str,
        alpha: float = 0.1,
        gamma: float = 0.99
    ) -> float:
        """SARSA update: Q(s,a) <- Q(s,a) + α[r + γ Q(s',a') - Q(s,a)]"""
        old_val = q_table.get((state, action), 0.0)
        next_val = q_table.get((next_state, next_action), 0.0)
        new_val = old_val + alpha * (reward + gamma * next_val - old_val)
        q_table[(state, action)] = new_val
        return new_val

    @staticmethod
    def double_q_learning_update(
        q1: Dict[Tuple[str, str], float],
        q2: Dict[Tuple[str, str], float],
        state: str,
        action: str,
        reward: float,
        next_state: str,
        actions: List[str],
        alpha: float = 0.1,
        gamma: float = 0.99
    ) -> Tuple[float, float]:
        """Double Q-Learning to reduce overestimation bias."""
        if random.random() < 0.5:
            # Update Q1 using Q2 for evaluation
            best_action = max(actions, key=lambda a: q1.get((next_state, a), 0.0))
            target = reward + gamma * q2.get((next_state, best_action), 0.0)
            old = q1.get((state, action), 0.0)
            q1[(state, action)] = old + alpha * (target - old)
        else:
            # Update Q2 using Q1 for evaluation
            best_action = max(actions, key=lambda a: q2.get((next_state, a), 0.0))
            target = reward + gamma * q1.get((next_state, best_action), 0.0)
            old = q2.get((state, action), 0.0)
            q2[(state, action)] = old + alpha * (target - old)
        return q1.get((state, action), 0.0), q2.get((state, action), 0.0)

    @staticmethod
    def epsilon_greedy(
        q_table: Dict[Tuple[str, str], float], 
        state: str, 
        actions: List[str], 
        epsilon: float
    ) -> str:
        """ε-greedy exploration strategy."""
        if random.random() < epsilon:
            return random.choice(actions)
        return max(actions, key=lambda a: q_table.get((state, a), 0.0))

    @staticmethod
    def softmax_policy(
        q_table: Dict[Tuple[str, str], float],
        state: str,
        actions: List[str],
        temperature: float = 1.0
    ) -> str:
        """Boltzmann/Softmax exploration."""
        q_values = np.array([q_table.get((state, a), 0.0) for a in actions])
        exp_q = np.exp((q_values - np.max(q_values)) / temperature)  # Stability trick
        probs = exp_q / np.sum(exp_q)
        return actions[np.random.choice(len(actions), p=probs)]

    @staticmethod
    def ucb_selection(
        q_table: Dict[Tuple[str, str], float],
        visit_counts: Dict[Tuple[str, str], int],
        state: str,
        actions: List[str],
        total_visits: int,
        c: float = 2.0
    ) -> str:
        """Upper Confidence Bound action selection."""
        ucb_values = []
        for a in actions:
            q = q_table.get((state, a), 0.0)
            n = visit_counts.get((state, a), 1)
            ucb = q + c * np.sqrt(np.log(total_visits + 1) / n)
            ucb_values.append(ucb)
        return actions[np.argmax(ucb_values)]

    @staticmethod
    def temporal_difference_lambda(
        eligibility_traces: Dict[Tuple[str, str], float],
        q_table: Dict[Tuple[str, str], float],
        state: str,
        action: str,
        reward: float,
        next_state: str,
        next_action: str,
        actions: List[str],
        alpha: float = 0.1,
        gamma: float = 0.99,
        lam: float = 0.9
    ) -> None:
        """TD(λ) with eligibility traces."""
        # Compute TD error
        delta = reward + gamma * q_table.get((next_state, next_action), 0.0) - q_table.get((state, action), 0.0)
        
        # Update eligibility trace
        eligibility_traces[(state, action)] = eligibility_traces.get((state, action), 0.0) + 1
        
        # Update all Q-values
        for (s, a), e in list(eligibility_traces.items()):
            q_table[(s, a)] = q_table.get((s, a), 0.0) + alpha * delta * e
            eligibility_traces[(s, a)] = gamma * lam * e
            if eligibility_traces[(s, a)] < 1e-6:
                del eligibility_traces[(s, a)]

class PolicyOptimizer:
    """High-level policy optimization utilities."""
    
    @staticmethod
    def decay_epsilon(epsilon: float, min_epsilon: float = 0.01, decay_rate: float = 0.995) -> float:
        """Exponential epsilon decay."""
        return max(min_epsilon, epsilon * decay_rate)
    
    @staticmethod
    def linear_epsilon_schedule(episode: int, total_episodes: int, start: float = 1.0, end: float = 0.01) -> float:
        """Linear epsilon schedule."""
        return start - (start - end) * min(1.0, episode / total_episodes)
    
    @staticmethod
    def cosine_annealing_lr(step: int, total_steps: int, lr_max: float, lr_min: float = 0.0) -> float:
        """Cosine annealing learning rate schedule."""
        return lr_min + 0.5 * (lr_max - lr_min) * (1 + np.cos(np.pi * step / total_steps))
