# LearningAlgorithms

**File**: `src\core\rl\LearningAlgorithms.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 13 imports  
**Lines**: 203  
**Complexity**: 13 (moderate)

## Overview

Python module containing implementation for LearningAlgorithms.

## Classes (3)

### `PolicyGradientBuffer`

Stores trajectory data for policy gradient methods.

**Methods** (3):
- `clear(self)`
- `compute_returns(self, gamma)`
- `compute_advantages(self, gamma, lam)`

### `LearningAlgorithms`

Standard RL algorithms for agent policy improvement.

**Methods** (7):
- `q_learning_update(q_table, state, action, reward, next_state, actions, alpha, gamma)`
- `sarsa_update(q_table, state, action, reward, next_state, next_action, alpha, gamma)`
- `double_q_learning_update(q1, q2, state, action, reward, next_state, actions, alpha, gamma)`
- `epsilon_greedy(q_table, state, actions, epsilon)`
- `softmax_policy(q_table, state, actions, temperature)`
- `ucb_selection(q_table, visit_counts, state, actions, total_visits, c)`
- `temporal_difference_lambda(eligibility_traces, q_table, state, action, reward, next_state, next_action, actions, alpha, gamma, lam)`

### `PolicyOptimizer`

High-level policy optimization utilities.

**Methods** (3):
- `decay_epsilon(epsilon, min_epsilon, decay_rate)`
- `linear_epsilon_schedule(episode, total_episodes, start, end)`
- `cosine_annealing_lr(step, total_steps, lr_max, lr_min)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `collections.defaultdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `numpy`
- `random`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
