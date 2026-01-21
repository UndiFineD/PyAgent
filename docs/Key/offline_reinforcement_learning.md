# Offline Reinforcement Learning

Standard RL is **Online**: The agent interacts with the environment, collects data, updates the policy, and repeats.
**Offline RL** (or Batch RL) learns a policy entirely from a fixed dataset of previously collected experiences (transitions), *without* any further interaction with the environment.

## 1. The Challenge: Distributional Shift

Why not just run Q-Learning on the dataset?
- **OOD Actions**: The learned policy might try to take an action that is not in the dataset.
- **Overestimation**: Standard Q-learning assumes it can query the Q-value of the optimal action. If that action is unseen, the Q-value might be erroneously high (hallucinated), leading the agent to choose a "doom" action that it thinks is good.

## 2. Conservative Q-Learning (CQL)

CQL fixes this by being pessimistic.
- It adds a regularization term to the loss function that **penalizes** the Q-values of actions that are not in the dataset.
- It only trusts actions it has seen.
- $$ L(\theta) = \text{Standard Bellman Error} + \alpha (\text{Q(unseen)} - \text{Q(seen)}) $$

## 3. Decision Transformer

Instead of using Bellman updates (Q-learning), we can treat RL as a **Sequence Modeling** problem.
- **Input**: Sequence of (State, Action, Reward).
- **Output**: The next Action.
- We train a Transformer (GPT) to predict the action that leads to the highest desired reward (Return-to-Go).
- This is purely supervised learning on the offline dataset.

## 4. Applications

- **Robotics**: Training robots using logs of human teleoperation.
- **Healthcare**: Suggesting treatments based on historical patient data (where we can't experiment on patients).
- **Recommender Systems**: Optimizing clicks based on past user logs.

## Summary

Offline RL turns Reinforcement Learning into a "Big Data" problem, allowing us to utilize massive static datasets.
