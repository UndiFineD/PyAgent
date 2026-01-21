# Inverse Reinforcement Learning (IRL)

In standard RL, we have the Reward Function and want to find the Policy.
In **Inverse RL**, we have the Expert's Policy (behavior) and want to find the **Reward Function** that explains it.

## 1. The Motivation

Why do we want the reward function?
- **Robustness**: A policy is specific to an environment. A reward function (the "goal") is often transferable.
- **Understanding**: We want to understand *what* the expert values (e.g., does the driver care more about speed or safety?).

## 2. The Ambiguity Problem

IRL is ill-posed because many reward functions can explain the same behavior.
- *Example*: A policy that does nothing is optimal if the reward is always zero.
- **Maximum Entropy IRL**: We choose the reward function that makes the expert's behavior optimal, but assumes the expert acts randomly (high entropy) when the reward doesn't distinguish between actions. This resolves ambiguity.

## 3. Cooperative Inverse Reinforcement Learning (CIRL)

A game where the Human knows the reward function, and the Robot wants to maximize it but doesn't know it.
- The Human performs actions to *teach* the Robot.
- The Robot observes and updates its belief about the reward function.
- This is the basis of **Value Alignment** in AI Safety.

## Summary

IRL is a key technique for AI Alignment, ensuring that AI systems optimize for what we *actually* want, not just what we say.
