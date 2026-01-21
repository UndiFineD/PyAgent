# Reinforcement Learning (RL)

A type of Machine Learning where an **Agent** learns to make decisions by performing actions in an **Environment** and receiving **Rewards** (or penalties).

## 1. Core Components

*   **Agent**: The learner (e.g., the Mario player).
*   **Environment**: The world (e.g., the Super Mario game level).
*   **State ($S$)**: The current situation (e.g., Mario's position, enemies on screen).
*   **Action ($A$)**: What the agent does (e.g., Jump, Run Right).
*   **Reward ($R$)**: Feedback (e.g., +100 points for a coin, -1000 for dying).
*   **Policy ($\pi$)**: The strategy. A mapping from State to Action ($S \rightarrow A$).

## 2. Algorithms

*   **Q-Learning**: A value-based method. The agent learns a "Q-Table" (Quality Table) that estimates the future reward of taking action $A$ in state $S$.
    *   **DQN (Deep Q-Network)**: Uses a Neural Network instead of a table to approximate Q-values (essential for complex states like pixels).
*   **Policy Gradients**: The agent directly learns the Policy function (probabilities of actions) using gradient ascent on the expected reward.
    *   **PPO (Proximal Policy Optimization)**: The standard for modern RL (used in RLHF for ChatGPT). It limits how much the policy can change in one step to ensure stability.

## 3. Challenges

*   **Exploration vs. Exploitation**: Should the agent try a random move to see what happens (Explore) or do what it thinks is best (Exploit)?
*   **Sparse Rewards**: In Chess, you only get a reward (+1/-1) at the very end. How do you know which move 50 turns ago was good? (Credit Assignment Problem).
