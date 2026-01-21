# Q-Learning

## Overview
**Q-Learning** is a model-free reinforcement learning algorithm to learn the value of an action in a particular state. It does not require a model of the environment (hence "model-free"), and it can handle problems with stochastic transitions and rewards.

## The Core Concept: The Q-Function
The goal is to learn a function $Q(s, a)$, which represents the **Quality** (expected future reward) of taking action $a$ in state $s$.

## The Bellman Equation
The heart of Q-Learning is the Bellman Optimality Equation. It updates the Q-value based on the immediate reward plus the discounted value of the best possible next state.

$$Q^{new}(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \cdot \left( r_t + \gamma \cdot \max_{a} Q(s_{t+1}, a) - Q(s_t, a_t) \right)$$

Where:
*   $Q(s_t, a_t)$: Current Q-value.
*   $\alpha$: Learning rate (how much we override old information).
*   $r_t$: Reward received for taking action $a_t$.
*   $\gamma$: Discount factor (importance of future rewards vs. immediate rewards).
*   $\max_{a} Q(s_{t+1}, a)$: The maximum predicted reward for the next state (the "greedy" choice).

## Q-Tables
For simple environments with a small number of states and actions (like a grid world), we can store the Q-values in a table (a **Q-Table**).
*   **Rows**: States.
*   **Columns**: Actions.
*   **Cells**: The Q-value.

## Exploration vs. Exploitation
*   **Exploitation**: Choosing the action with the highest Q-value (using what we know).
*   **Exploration**: Choosing a random action to discover new possibilities.
*   **Epsilon-Greedy Strategy**: A common method where the agent chooses a random action with probability $\epsilon$ and the best action with probability $1-\epsilon$.

## Limitations
Q-Learning struggles when the state space is massive (e.g., pixels on a screen) because the Q-Table becomes too large to store or visit every state. This led to the development of **Deep Q-Networks (DQN)**.
