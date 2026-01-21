# Hierarchical Reinforcement Learning (HRL)

Standard Reinforcement Learning (RL) struggles with **long-horizon tasks** (e.g., "Cook a meal") because the reward is delayed by thousands of steps.
**Hierarchical RL** solves this by decomposing the task into a hierarchy of sub-tasks (e.g., "Cut vegetables", "Boil water").

## 1. The Options Framework

The most common formalism for HRL.
- **Primitive Actions**: Atomic moves (Up, Down, Left, Right).
- **Options (Macro-actions)**: A policy that runs for multiple steps until a termination condition is met.
    - *Example*: `GoToDoor` is an option. Once invoked, it executes primitive actions until the agent is at the door.
- **Policy over Options**: The "Manager" chooses which Option to execute.

## 2. Feudal Networks

Inspired by feudal management hierarchies.
- **Manager (Lord)**: Sets abstract goals (e.g., "Move to coordinate (10, 10)"). It operates at a lower temporal resolution.
- **Worker**: Takes the goal and executes primitive actions to achieve it. It receives rewards from the Manager (intrinsic reward) for achieving the goal, not just from the environment.

## 3. Benefits

1.  **Temporal Abstraction**: The Manager only makes decisions every $N$ steps, effectively shortening the horizon.
2.  **Transfer Learning**: Learned skills (Options) like "Open Door" can be reused in different tasks.
3.  **Sparse Rewards**: The Manager provides dense intrinsic rewards to the Worker, helping it learn even if the environment reward is zero.

## Summary

HRL is essential for scaling RL to complex, real-world problems where planning requires thinking at multiple levels of abstraction.
